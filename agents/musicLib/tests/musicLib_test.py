import pytest
import json
from unittest.mock import MagicMock, patch
from core.base import AgentBase
from agents.musicLib import SpotifySearchAgent

class MockResponse:
    """Mock class for http.client.HTTPResponse"""
    def __init__(self, status, data):
        self.status = status
        self._data = data

    def read(self):
        return json.dumps(self._data).encode('utf-8')

class MockConnection:
    """Mock class for http.client.HTTPSConnection"""
    def __init__(self, response):
        self.response = response
        self.request_args = None

    def request(self, method, endpoint, headers=None):
        self.request_args = (method, endpoint, headers)

    def getresponse(self):
        return self.response

    def close(self):
        pass

@pytest.fixture
def mock_successful_response():
    """Fixture providing successful API response data"""
    return {
        "albums": {
            "totalCount": 1,
            "items": [{
                "data": {
                    "uri": "spotify:album:123",
                    "name": "Test Album",
                    "artists": {
                        "items": [{
                            "profile": {
                                "name": "Test Artist"
                            }
                        }]
                    },
                    "date": {
                        "year": 2024
                    }
                }
            }]
        }
    }

@pytest.fixture
def spotify_agent():
    """Fixture to initialize SpotifySearchAgent with test API key"""
    return SpotifySearchAgent(api_key="test_api_key")

def test_init():
    """Test SpotifySearchAgent initialization"""
    agent = SpotifySearchAgent(api_key="test_key")
    assert agent.rapid_api_key == "test_key"
    assert agent.rapid_api_host == "spotify23.p.rapidapi.com"
    assert agent.base_url == "spotify23.p.rapidapi.com"
    assert isinstance(agent, AgentBase)

def test_filter_album_data(spotify_agent):
    """Test album data filtering"""
    input_data = {
        "uri": "spotify:album:123",
        "name": "Test Album",
        "artists": {
            "items": [{
                "profile": {
                    "name": "Test Artist"
                }
            }]
        },
        "date": {
            "year": 2024
        }
    }
    
    filtered = spotify_agent._filter_album_data(input_data)
    assert filtered == {
        "uri": "spotify:album:123",
        "name": "Test Album",
        "artist": "Test Artist",
        "year": 2024
    }

@patch('http.client.HTTPSConnection')
def test_execute_success(mock_connection, spotify_agent, mock_successful_response):
    """Test successful API request execution"""
    mock_conn = MockConnection(MockResponse(200, mock_successful_response))
    mock_connection.return_value = mock_conn

    result = spotify_agent.execute(
        query="test query",
        api_key="test_api_key"
    )

    assert result["total_count"] == 1
    assert len(result["albums"]) == 1
    assert result["albums"][0]["name"] == "Test Album"
    assert result["albums"][0]["artist"] == "Test Artist"
    assert result["albums"][0]["year"] == 2024

@patch('http.client.HTTPSConnection')
def test_execute_api_error(mock_connection, spotify_agent):
    """Test handling of API error response"""
    error_response = {"message": "API Error"}
    mock_conn = MockConnection(MockResponse(400, error_response))
    mock_connection.return_value = mock_conn

    result = spotify_agent.execute(
        query="test query",
        api_key="test_api_key"
    )

    assert "error" in result
    assert result["status"] == "failed"
    assert "API request failed with status 400" in result["error"]

def test_execute_missing_query(spotify_agent):
    """Test handling of missing query parameter"""
    result = spotify_agent.execute(api_key="test_api_key")
    assert "error" in result
    assert result["status"] == "failed"
    assert "Search query is required" in result["error"]

def test_execute_missing_api_key(spotify_agent):
    """Test handling of missing API key"""
    agent = SpotifySearchAgent()  # Initialize without API key
    result = agent.execute(query="test")
    assert "error" in result
    assert result["status"] == "failed"
    assert "API key must be provided" in result["error"]

@patch('http.client.HTTPSConnection')
def test_health_check_success(mock_connection, spotify_agent, mock_successful_response):
    """Test successful health check"""
    mock_conn = MockConnection(MockResponse(200, mock_successful_response))
    mock_connection.return_value = mock_conn

    result = spotify_agent.health_check()
    assert result["status"] == "healthy"
    assert result["message"] == "Spotify API service is available"

@patch('http.client.HTTPSConnection')
def test_health_check_failure(mock_connection, spotify_agent):
    """Test failed health check"""
    error_response = {"message": "Service unavailable"}
    mock_conn = MockConnection(MockResponse(500, error_response))
    mock_connection.return_value = mock_conn

    result = spotify_agent.health_check()
    assert result["status"] == "unhealthy"
    assert "API request failed with status 500" in result["message"]

def test_health_check_no_api_key():
    """Test health check without API key"""
    agent = SpotifySearchAgent()
    result = agent.health_check()
    assert result["status"] == "unknown"
    assert result["message"] == "API key not provided"