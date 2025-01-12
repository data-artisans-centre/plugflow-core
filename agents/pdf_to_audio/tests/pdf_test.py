import pytest
from unittest.mock import MagicMock, patch, mock_open
from agents.pdf_to_audio import PdfToAudioAgent
import pypdf
import pyttsx3
import io

class MockPdfReader:
    """Mock class for pypdf.PdfReader to simulate PDF reading behavior."""
    def __init__(self, file):
        self.pages = [
            type('MockPage', (), {'extract_text': lambda: "This is page 1"}),
            type('MockPage', (), {'extract_text': lambda: "This is page 2"})
        ]

class MockPyttsx3Engine:
    """Mock class for pyttsx3.Engine to simulate text-to-speech behavior."""
    def __init__(self):
        self.properties = {
            'voices': [
                type('MockVoice', (), {'id': 'voice1'}),
                type('MockVoice', (), {'id': 'voice2'})
            ],
            'rate': 150,
            'volume': 0.9
        }

    def getProperty(self, property_name):
        return self.properties.get(property_name)

    def setProperty(self, property_name, value):
        self.properties[property_name] = value

    def say(self, text):
        pass

    def runAndWait(self):
        pass

@pytest.fixture
def pdf_audio_agent(monkeypatch):
    """Fixture to initialize PdfToAudioAgent with mocked dependencies."""
    monkeypatch.setattr("pypdf.PdfReader", MockPdfReader)
    monkeypatch.setattr("pyttsx3.init", lambda: MockPyttsx3Engine())
    agent = PdfToAudioAgent()
    return agent

def test_read_pdf_success(pdf_audio_agent):
    """Test successful PDF text extraction."""
    with patch("builtins.open", mock_open(read_data="dummy pdf content")):
        text = pdf_audio_agent.read_pdf("test.pdf")
        assert text == "This is page 1This is page 2"

def test_read_pdf_file_not_found(pdf_audio_agent):
    """Test handling of non-existent PDF file."""
    with pytest.raises(FileNotFoundError):
        pdf_audio_agent.read_pdf("nonexistent.pdf")

def test_play_audio_success(pdf_audio_agent):
    """Test successful audio playback."""
    test_text = "Test audio content"
    pdf_audio_agent.play_audio(test_text)
    # Since we can't actually verify audio output, we just ensure no exceptions are raised
    assert True

def test_play_audio_configuration(pdf_audio_agent):
    """Test audio configuration settings."""
    test_text = "Test configuration"
    pdf_audio_agent.play_audio(test_text)
    
    engine = pdf_audio_agent.engine
    assert engine.getProperty('rate') == 150
    assert engine.getProperty('volume') == 0.9
    assert engine.getProperty('voice') == engine.getProperty('voices')[1].id

def test_execute_success(pdf_audio_agent):
    """Test successful execution of PDF to audio conversion."""
    with patch("builtins.open", mock_open(read_data="dummy pdf content")):
        result = pdf_audio_agent.execute(pdf_path="test.pdf")
        
        assert result["status"] == "success"
        assert result["message"] == "PDF text has been converted to speech and played"
        assert result["full_text"] == "This is page 1This is page 2"

def test_execute_missing_pdf_path(pdf_audio_agent):
    """Test handling of missing PDF path."""
    result = pdf_audio_agent.execute()  # Calling without pdf_path
    assert result["status"] == "error"
    assert "'pdf_path' must be provided." in result["message"]

def test_execute_invalid_pdf(pdf_audio_agent):
    """Test handling of invalid PDF file."""
    def mock_pdf_error(*args, **kwargs):
        raise Exception("Invalid PDF format")
    
    # Mock both the file open and PdfReader
    with patch("builtins.open", mock_open(read_data="dummy content")), \
         patch("pypdf.PdfReader", side_effect=mock_pdf_error):
        result = pdf_audio_agent.execute(pdf_path="invalid.pdf")
        assert result["status"] == "error"
        assert "Invalid PDF format" in str(result["message"])

def test_health_check_success(pdf_audio_agent):
    """Test health check success status."""
    result = pdf_audio_agent.health_check()
    assert result["status"] == "healthy"
    assert result["message"] == "PDF to audio conversion service is operational"

def test_health_check_failure(monkeypatch):
    """Test health check failure status."""
    def mock_say(*args):
        raise Exception("TTS engine error")
    
    monkeypatch.setattr("pyttsx3.Engine.say", mock_say)
    agent = PdfToAudioAgent()
    result = agent.health_check()
    
    assert result["status"] == "unhealthy"
    assert "TTS engine error" in result["message"]