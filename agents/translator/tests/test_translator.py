import pytest
from agents.translator import TranslatorAgent


class MockTranslator:
    """Mock class for Translator to simulate translation behavior."""
    def translate(self, text, dest):
        supported_languages = ['en', 'es', 'fr', 'de', 'zh-cn', 'ja', 'ar', 'ru', 'pt', 'it']
        
        # Predefined translations
        translations = {
            "Hello": {"text": "Hola", "src": "en", "dest": "es"},
            "Bonjour": {"text": "Hello", "src": "fr", "dest": "en"}
        }
        
        # Check if destination language is supported
        if dest not in supported_languages:
            raise ValueError("Unsupported or invalid target language")
        
        # Check if text has a predefined translation
        if text not in translations:
            raise ValueError("Translation not found")
        
        # Create mock translation object
        mock_translation = type('MockTranslation', (), {
            'text': translations[text]["text"],
            'src': translations[text]["src"],
            'dest': translations[text]["dest"]
        })()
        return mock_translation


@pytest.fixture
def translator_agent(monkeypatch):
    """Fixture to initialize TranslatorAgent with a mock translator."""
    agent = TranslatorAgent()
    monkeypatch.setattr("agents.translator.Translator", MockTranslator)
    return agent


def test_execute_success(translator_agent):
    """Test successful translation execution."""
    result = translator_agent.execute(text="Hello", target_language="es")
    assert result['original_text'] == "Hello"
    assert result['translated_text'] == "Hola"
    assert result['source_language'] == "en"
    assert result['target_language'] == "es"


def test_execute_missing_text(translator_agent):
    """Test handling of missing input text."""
    with pytest.raises(ValueError, match="Text cannot be empty."):
        translator_agent.execute(target_language="es")


def test_health_check_success(translator_agent):
    """Test health check success status."""
    result = translator_agent.health_check()
    assert result["status"] == "healthy"
    assert result["message"] == "Translation service is operational"


def test_health_check_failure(monkeypatch):
    """Test health check failure status."""
    def mock_translate(*args, **kwargs):
        raise Exception("Service unavailable")

    monkeypatch.setattr("agents.translator.Translator.translate", mock_translate)
    agent = TranslatorAgent()
    result = agent.health_check()
    assert result["status"] == "unhealthy"
    assert "Service unavailable" in result["message"]


def test_list_supported_languages(translator_agent):
    """Test listing supported languages."""
    supported_languages = translator_agent.list_supported_languages()
    expected_languages = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Chinese': 'zh-cn',
        'Japanese': 'ja',
        'Arabic': 'ar',
        'Russian': 'ru',
        'Portuguese': 'pt',
        'Italian': 'it'
    }
    assert supported_languages == expected_languages