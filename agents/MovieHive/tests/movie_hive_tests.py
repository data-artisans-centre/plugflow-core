import pytest
import requests
from unittest.mock import Mock
from agents.MovieHive import MovieHiveAgent

@pytest.fixture
def mock_response():
    """Fixture to create a mock response object."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "Title": "Inception",
        "Year": "2010",
        "Response": "True"
    }
    return mock

@pytest.fixture
def movie_hive_agent(monkeypatch, mock_response):
    """Fixture to initialize MovieHiveAgent with mocked requests."""
    agent = MovieHiveAgent()
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_response))
    return agent

def test_execute_success(movie_hive_agent):
    """Test successful movie information fetching."""
    result = movie_hive_agent.execute(title="Inception", api_key="test_key")
    assert result["Title"] == "Inception"
    assert result["Year"] == "2010"

def test_execute_empty_title(movie_hive_agent):
    """Test execution with empty movie title."""
    result = movie_hive_agent.execute(title="", api_key="test_key")
    assert "error" in result
    assert "Movie title cannot be empty." in result["error"]

def test_execute_empty_api_key(movie_hive_agent):
    """Test execution with empty API key."""
    result = movie_hive_agent.execute(title="Inception", api_key="")
    assert "error" in result
    assert "API key cannot be empty." in result["error"]

def test_execute_api_error(movie_hive_agent, monkeypatch):
    """Test execution when API returns an error."""
    mock_error_response = Mock()
    mock_error_response.status_code = 200
    mock_error_response.json.return_value = {"Response": "False", "Error": "Movie not found!"}
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_error_response))
    result = movie_hive_agent.execute(title="Unknown Movie", api_key="test_key")
    assert "error" in result
    assert "Movie not found!" in result["error"]

def test_execute_request_exception(movie_hive_agent, monkeypatch):
    """Test execution when request raises an exception."""
    def mock_request(*args, **kwargs):
        raise requests.RequestException("Connection error")
    monkeypatch.setattr(requests, "get", mock_request)
    
    result = movie_hive_agent.execute(title="Inception", api_key="test_key")
    assert "error" in result
    assert "Failed to fetch movie information" in result["error"]

def test_health_check_success(movie_hive_agent):
    """Test successful health check."""
    health = movie_hive_agent.health_check(api_key="test_key")
    assert health["status"] == "healthy"
    assert "operational" in health["message"]

def test_health_check_failure(movie_hive_agent, monkeypatch):
    """Test health check failure."""
    def mock_request(*args, **kwargs):
        raise requests.RequestException("Service unavailable")
    monkeypatch.setattr(requests, "get", mock_request)
    
    health = movie_hive_agent.health_check(api_key="test_key")
    assert health["status"] == "unhealthy"
    assert "Service unavailable" in health["message"]
