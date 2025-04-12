import pytest
import requests
from unittest.mock import Mock
from agents.lyricist import LyricsAgent

@pytest.fixture
def mock_response():
    """Fixture to create a mock response object."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"lyrics": "Test lyrics content"}
    return mock

@pytest.fixture
def lyrics_agent(monkeypatch, mock_response):
    """Fixture to initialize LyricsAgent with mocked requests."""
    agent = LyricsAgent()
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_response))
    return agent

def test_execute_success(lyrics_agent):
    """Test successful lyrics fetching."""
    result = lyrics_agent.execute(artist="TestArtist", title="TestSong")
    assert result["artist"] == "TestArtist"
    assert result["title"] == "TestSong"
    assert result["lyrics"] == "Test lyrics content"

def test_execute_empty_input(lyrics_agent):
    """Test execution with empty artist/title."""
    result = lyrics_agent.execute(artist="", title="TestSong")
    assert "error" in result
    assert "Artist and song title cannot be empty" in result["error"]

def test_execute_api_error(lyrics_agent, monkeypatch):
    """Test execution when API returns an error."""
    mock_error_response = Mock()
    mock_error_response.status_code = 404
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_error_response))
    
    result = lyrics_agent.execute(artist="TestArtist", title="TestSong")
    assert "error" in result
    assert "Unable to fetch lyrics" in result["error"]

def test_execute_no_lyrics(lyrics_agent, monkeypatch):
    """Test execution when no lyrics are found."""
    mock_empty_response = Mock()
    mock_empty_response.status_code = 200
    mock_empty_response.json.return_value = {"lyrics": ""}
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_empty_response))
    
    result = lyrics_agent.execute(artist="TestArtist", title="TestSong")
    assert "error" in result
    assert "No lyrics found" in result["error"]

def test_execute_request_exception(lyrics_agent, monkeypatch):
    """Test execution when request raises an exception."""
    def mock_request(*args, **kwargs):
        raise requests.RequestException("Connection error")
    monkeypatch.setattr(requests, "get", mock_request)
    
    result = lyrics_agent.execute(artist="TestArtist", title="TestSong")
    assert "error" in result
    assert "Failed to fetch lyrics" in result["error"]

def test_health_check_success(lyrics_agent):
    """Test successful health check."""
    health = lyrics_agent.health_check()
    assert health["status"] == "healthy"
    assert "operational" in health["message"]

def test_health_check_failure(lyrics_agent, monkeypatch):
    """Test health check failure."""
    def mock_request(*args, **kwargs):
        raise requests.RequestException("Service unavailable")
    monkeypatch.setattr(requests, "get", mock_request)
    
    health = lyrics_agent.health_check()
    assert health["status"] == "unhealthy"
    assert "Service unavailable" in health["message"]