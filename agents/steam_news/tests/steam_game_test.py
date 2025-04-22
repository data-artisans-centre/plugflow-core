import pytest
import json
from unittest.mock import MagicMock, patch
from agents.steam_news import GameNewsAgent  # Changed from game_news to steam_news


@pytest.fixture
def mock_response():
    """Create a mock response object."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {
        "success": True,
        "news": [
            {
                "title": "Test News Title",
                "url": "https://example.com/news/1",
                "contents": "This is a test news article",
                "date": "2024-01-01T12:00:00Z",
            }
        ]
    }
    return mock_resp


@pytest.fixture
def game_news_agent():
    """Fixture to initialize the GameNewsAgent."""
    return GameNewsAgent()


@pytest.mark.parametrize(
    "api_key,limit,offset",
    [
        ("test_api_key", 10, 0),
        ("test_api_key", 5, 10),
    ],
)
def test_execute_success(game_news_agent, mock_response, api_key, limit, offset):
    """Test successful execution of the GameNewsAgent."""
    with patch("agents.steam_news.requests.get", return_value=mock_response): 
        result = game_news_agent.execute(api_key=api_key, limit=limit, offset=offset)
        
        assert "success" in result, "Expected success field in response"
        assert "news" in result, "Expected news array in response"
        assert len(result["news"]) > 0, "Expected at least one news item"
        assert result["news"][0]["title"] == "Test News Title", "Expected correct news title"


def test_execute_empty_api_key(game_news_agent):
    """Test execution with an empty API key."""
    result = game_news_agent.execute(api_key="")
    assert "error" in result, "Expected error in response"
    assert "Failed to fetch game news" in result["error"], "Expected error message about fetching game news"


def test_execute_api_error(game_news_agent):
    """Test execution when API returns an error."""
    mock_error_response = MagicMock()
    mock_error_response.json.side_effect = Exception("API error")
    
    with patch("agents.steam_news.requests.get", return_value=mock_error_response): 
        result = game_news_agent.execute(api_key="test_api_key")
        
        assert "error" in result, "Expected error in response"
        assert "Failed to fetch game news" in result["error"], "Expected appropriate error message"


def test_health_check_success(game_news_agent, mock_response):
    """Test health check success."""
    with patch("agents.steam_news.requests.get", return_value=mock_response):  
        health = game_news_agent.health_check(api_key="test_api_key")
        
        assert health["status"] == "healthy", "Expected health status to be 'healthy'"
        assert "Games Details API is operational" in health["message"], "Expected success message in health check"


def test_health_check_api_error(game_news_agent):
    """Test health check when API returns an error."""
    mock_error_response = MagicMock()
    mock_error_response.status_code = 500
    
    with patch("agents.steam_news.requests.get", return_value=mock_error_response): 
        health = game_news_agent.health_check(api_key="test_api_key")
        
        assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'"
        assert "test request failed with status code: 500" in health["message"], "Expected status code in error message"


def test_health_check_empty_api_key(game_news_agent):
    """Test health check with an empty API key."""
    health = game_news_agent.health_check(api_key="")
    assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'"
    assert "API key cannot be empty" in health["message"], "Expected error message about empty API key"


def test_health_check_exception(game_news_agent):
    """Test health check when an exception occurs."""
    with patch("agents.steam_news.requests.get", side_effect=Exception("Connection error")):  
        health = game_news_agent.health_check(api_key="test_api_key")
        
        assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'"
        assert "Connection error" in health["message"], "Expected exception message in health check"