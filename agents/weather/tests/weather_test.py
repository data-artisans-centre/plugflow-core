import pytest
from unittest.mock import MagicMock, patch
import requests
from agents.weather import WeatherAgent  # Adjust import based on your project structure

class MockResponse:
    """Mock response class to simulate API responses."""
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


@pytest.fixture
def weather_agent():
    """Fixture to create a WeatherAgent instance with a mock API key."""
    return WeatherAgent("mock_api_key")


def test_execute_by_city_success(weather_agent):
    """Test successful weather fetch by city name."""
    # Mock API response
    mock_response = {
        "data": [{
            "city_name": "New York",
            "country_code": "US",
            "lat": 40.7128,
            "lon": -74.0060,
            "temp": 22.5,
            "app_temp": 25.0,
            "weather": {
                "description": "Partly cloudy",
                "code": 802,
                "icon": "c02d"
            },
            "wind_spd": 3.1,
            "wind_dir": 180,
            "wind_cdir_full": "South",
            "rh": 65,
            "pres": 1015.2,
            "slp": 1016.5,
            "clouds": 40,
            "vis": 10,
            "solar_rad": 500,
            "uv": 5,
            "aqi": 50
        }]
    }

    with patch('requests.get', return_value=MockResponse(mock_response)) as mock_get:
        result = weather_agent.execute(location="New York")
        
        # Verify API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params']['city'] == "New York"
        
        # Verify result structure and values
        assert result['location']['name'] == "New York"
        assert result['location']['country'] == "US"
        assert result['temperature']['current'] == 22.5
        assert result['weather']['description'] == "Partly cloudy"


def test_execute_by_coordinates_success(weather_agent):
    """Test successful weather fetch by latitude and longitude."""
    mock_response = {
        "data": [{
            "city_name": "Mountain View",
            "country_code": "US",
            "lat": 37.3861,
            "lon": -122.0839,
            "temp": 20.5,
            "app_temp": 22.0,
            "weather": {
                "description": "Clear sky",
                "code": 800,
                "icon": "01d"
            },
            "wind_spd": 2.5,
            "wind_dir": 270,
            "wind_cdir_full": "West",
            "rh": 55,
            "pres": 1010.1,
            "slp": 1011.3,
            "clouds": 0,
            "vis": 16,
            "solar_rad": 800,
            "uv": 7,
            "aqi": 35
        }]
    }

    with patch('requests.get', return_value=MockResponse(mock_response)) as mock_get:
        result = weather_agent.execute(lat=37.3861, lon=-122.0839)
        
        # Verify API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs['params']['lat'] == 37.3861
        assert kwargs['params']['lon'] == -122.0839
        
        # Verify result structure and values
        assert result['location']['latitude'] == 37.3861
        assert result['location']['longitude'] == -122.0839
        assert result['weather']['description'] == "Clear sky"

def test_execute_api_error(weather_agent):
    """Test handling of API request failure."""
    with patch('requests.get', return_value=MockResponse({}, status_code=401)) as mock_get:
        result = weather_agent.execute(location="New York")
        
        assert result['status'] == 'failed'
        assert 'error' in result

def test_execute_extreme_weather(weather_agent):
    """Test handling of extreme weather data."""
    mock_response = {
        "data": [{
            "city_name": "Extreme City",
            "temp": -50.0,  # Extremely low temperature
            "wind_spd": 100.0,  # Extremely high wind speed
            "weather": {
                "description": "Extreme conditions",
                "code": 900  # Hypothetical extreme weather code
            }
        }]
    }

    with patch('requests.get', return_value=MockResponse(mock_response)) as mock_get:
        result = weather_agent.execute(location="Extreme City")
        
        assert result['location']['name'] == "Extreme City"
        assert result['temperature']['current'] == -50.0
        assert result['weather']['description'] == "Extreme conditions"


def test_execute_no_data(weather_agent):
    """Test handling of API response with no data or empty response."""
    # Scenario 1: Empty data list
    mock_response_empty = {"data": []}
    
    with patch('requests.get', return_value=MockResponse(mock_response_empty)) as mock_get:
        result = weather_agent.execute(location="Non-existent City")
        assert result['status'] == 'failed'
        assert 'No weather data found' in result['error']

    # Scenario 2: Completely empty response
    mock_response_none = {}
    
    with patch('requests.get', return_value=MockResponse(mock_response_none)) as mock_get:
        result = weather_agent.execute(location="Another Non-existent City")
        assert result['status'] == 'failed'
        assert 'No weather data found' in result['error']

    # Scenario 3: Simulating connection error or None response
    with patch('requests.get', side_effect=requests.exceptions.RequestException("Connection error")) as mock_get:
        result = weather_agent.execute(location="Yet Another City")
        assert result['status'] == 'failed'
        assert 'Connection error' in result['error']


def test_health_check_success(weather_agent):
    """Test health check functionality."""
    # Create a successful mock response
    mock_response = {
        "data": [{
            "city_name": "New York",
            "temp": 22.5
        }]
    }

    with patch('requests.get', return_value=MockResponse(mock_response)) as mock_get:
        result = weather_agent.health_check()
        
        # Verify API call was made
        mock_get.assert_called_once()
        
        # Verify health check result
        assert result['status'] == "healthy"
        assert result['message'] == "Weatherbit API service is available"


def test_health_check_failure(weather_agent):
    """Test health check failure scenario."""
    with patch('requests.get', side_effect=Exception("Connection error")) as mock_get:
        result = weather_agent.health_check()
        
        # Verify health check result for failure
        assert result['status'] == "unhealthy"
        assert "Connection error" in result['message']


@pytest.mark.parametrize("units,language", [
    ('M', 'en'),   # Metric units, English
    ('I', 'es'),   # Imperial units, Spanish
    ('M', 'fr')    # Metric units, French
])
def test_execute_units_and_language(weather_agent, units, language):
    """Test different unit and language configurations."""
    mock_response = {
        "data": [{
            "city_name": "Test City",
            "temp": 22.5,
            "weather": {"description": "Test description"}
        }]
    }

    with patch('requests.get', return_value=MockResponse(mock_response)) as mock_get:
        result = weather_agent.execute(location="Test City", units=units, language=language)
        
        # Verify API call parameters
        args, kwargs = mock_get.call_args
        assert kwargs['params']['units'] == units
        assert kwargs['params']['lang'] == language
        
        # Basic result validation
        assert result['location']['name'] == "Test City"