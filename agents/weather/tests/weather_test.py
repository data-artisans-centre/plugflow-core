import pytest
import requests
from unittest.mock import Mock, patch
from agents.weather import WeatherAgent

@pytest.fixture
def mock_weather_response():
    """Fixture to create a mock weather response object."""
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "main": {
            "temp": 20.5,
            "feels_like": 19.8,
            "temp_min": 18.9,
            "temp_max": 22.1,
            "humidity": 65,
            "pressure": 1012
        },
        "weather": [
            {
                "main": "Clouds",
                "description": "scattered clouds",
                "icon": "03d"
            }
        ],
        "wind": {
            "speed": 3.1,
            "deg": 240
        },
        "clouds": {
            "all": 40
        },
        "visibility": 10000,
        "sys": {
            "country": "GB"
        }
    }
    return mock

@pytest.fixture
def weather_agent(monkeypatch, mock_weather_response):
    """Fixture to initialize WeatherAgent with mocked requests."""
    agent = WeatherAgent(api_key="test_api_key")
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_weather_response))
    return agent

def test_execute_success(weather_agent):
    """Test successful weather fetching."""
    result = weather_agent.execute(city="London", country_code="GB")
    
    assert result["location"]["name"] == "London"
    assert result["location"]["country"] == "GB"
    assert result["temperature"]["current"] == 20.5
    assert result["weather"]["description"] == "scattered clouds"
    assert result["humidity"] == 65

def test_execute_empty_city(weather_agent):
    """Test execution with empty city."""
    result = weather_agent.execute(city="", country_code="GB")
    
    assert "error" in result
    assert "City name cannot be empty" in result["error"]
    assert result["status"] == "failed"

def test_execute_missing_api_key(monkeypatch, mock_weather_response):
    """Test execution with missing API key."""
    agent = WeatherAgent()  # No API key provided
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_weather_response))
    
    result = agent.execute(city="London", country_code="GB")
    
    assert "error" in result
    assert "API key must be provided" in result["error"]
    assert result["status"] == "failed"

def test_execute_api_error(weather_agent, monkeypatch):
    """Test execution when API returns an error."""
    mock_error_response = Mock()
    mock_error_response.status_code = 404
    mock_error_response.json.return_value = {"message": "City not found"}
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_error_response))
    
    result = weather_agent.execute(city="NonExistentCity", country_code="XX")
    
    assert "error" in result
    assert "API error: City not found" in result["error"] or "API request failed with status code 404" in result["error"]
    assert result["status"] == "failed"

def test_execute_request_exception(weather_agent, monkeypatch):
    """Test execution when request raises an exception."""
    def mock_request(*args, **kwargs):
        raise requests.RequestException("Connection error")
    
    monkeypatch.setattr(requests, "get", mock_request)
    
    result = weather_agent.execute(city="London", country_code="GB")
    
    assert "error" in result
    assert "Connection error" in result["error"]
    assert result["status"] == "failed"

def test_health_check_success(weather_agent):
    """Test successful health check."""
    health = weather_agent.health_check()
    
    assert health["status"] == "healthy"
    assert "Open Weather API service is available" in health["message"]

def test_health_check_failure(weather_agent, monkeypatch):
    """Test health check failure."""
    def mock_request(*args, **kwargs):
        raise requests.RequestException("Service unavailable")
    
    monkeypatch.setattr(requests, "get", mock_request)
    
    health = weather_agent.health_check()
    
    assert health["status"] == "unhealthy"
    assert "Service unavailable" in health["message"]

def test_health_check_api_error(weather_agent, monkeypatch):
    """Test health check when API returns an error."""
    mock_error_response = Mock()
    mock_error_response.status_code = 401
    mock_error_response.json.return_value = {"message": "Invalid API key"}
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_error_response))
    
    health = weather_agent.health_check()
    
    assert health["status"] == "unhealthy"
    assert "Health check failed" in health["message"]


def test_execute_invalid_location(weather_agent, monkeypatch):
    """Test weather fetching with invalid location or country code."""
    # Mock an error response for invalid location
    mock_error_response = Mock()
    mock_error_response.status_code = 404
    mock_error_response.json.return_value = {"message": "City not found"}
    monkeypatch.setattr(requests, "get", Mock(return_value=mock_error_response))
    
    # Test with invalid city
    result = weather_agent.execute(city="NonExistentCity", country_code="IN")
    
    assert result["status"] == "failed"
    assert "error" in result
    assert "not found" in result["error"].lower() or "404" in result["error"]
    
    # Test with invalid country code
    result = weather_agent.execute(city="Coimbatore", country_code="XX")
    
    assert result["status"] == "failed"
    assert "error" in result