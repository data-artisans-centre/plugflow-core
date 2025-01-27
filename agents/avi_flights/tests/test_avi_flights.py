import json
import pytest
import requests
from unittest.mock import patch
from agents.avi_flights import FlightDetailsAgent
import re

# Constants for test cases
VALID_API_KEY = "test_valid_api_key"
INVALID_API_KEY = "test_invalid_api_key"
BASE_URL = "https://api.aviationstack.com/v1/flights"


@pytest.fixture
def agent():
    """Fixture to create an instance of the FlightDetailsAgent."""
    return FlightDetailsAgent()


@patch("requests.get")
def test_execute_valid_request(mock_get, agent):
    """
    Test a valid request with the required and optional parameters.
    """
    mock_response = {
        "data": [
            {
                "flight_date": "2025-01-27",
                "departure_airport": "Los Angeles International",
                "arrival_airport": "John F. Kennedy International",
                "airline_name": "Delta Airlines",
                "flight_number": "2557",
                "flight_status": "landed",
                "departure_time": "2025-01-27T10:00:00Z",
                "arrival_time": "2025-01-27T18:00:00Z",
            }
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = agent.execute(
        api_key=VALID_API_KEY,
        flight_date="2025-01-27",
        dep_iata="LAX",
        arr_iata="JFK",
    )

    mock_get.assert_called_once_with(
        BASE_URL,
        params={
            "access_key": VALID_API_KEY,
            "flight_date": "2025-01-27",
            "dep_iata": "LAX",
            "arr_iata": "JFK",
        },
    )
    assert result["data"][0]["flight_number"] == "2557"
    assert result["data"][0]["flight_status"] == "landed"


@patch("requests.get")
def test_execute_invalid_api_key(mock_get, agent):
    """
    Test the behavior when an invalid API key is used.
    """
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = {"error": {"message": "Invalid API key"}}

    with pytest.raises(ValueError, match="Invalid API key provided."):
        agent.execute(api_key=INVALID_API_KEY)


@patch("requests.get")
def test_execute_missing_required_params(mock_get, agent):
    """
    Test behavior when required parameters are missing.
    """
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = {"error": {"message": "Bad request"}}

    with pytest.raises(ValueError, match="Bad request: Invalid or missing parameters."):
        agent.execute(api_key=VALID_API_KEY)


@patch("requests.get")
def test_execute_rate_limit_exceeded(mock_get, agent):
    """
    Test the behavior when the API rate limit is exceeded.
    """
    mock_get.return_value.status_code = 429
    mock_get.return_value.json.return_value = {"error": {"message": "Rate limit exceeded"}}

    with pytest.raises(ValueError, match="Rate limit exceeded: Try again later."):
        agent.execute(api_key=VALID_API_KEY)


@patch("requests.get")
def test_execute_server_error(mock_get, agent):
    """
    Test the behavior when the API returns a 500 server error.
    """
    mock_get.return_value.status_code = 500
    mock_get.return_value.text = "Internal Server Error"

    with pytest.raises(ValueError, match="Unexpected server error: 500"):
        agent.execute(api_key=VALID_API_KEY)


@patch("requests.get")
def test_execute_optional_parameters(mock_get, agent):
    """
    Test behavior with additional optional parameters.
    """
    mock_response = {
        "data": [
            {
                "flight_date": "2025-01-27",
                "departure_airport": "Los Angeles International",
                "arrival_airport": "John F. Kennedy International",
                "airline_name": "Delta Airlines",
                "flight_number": "2557",
                "flight_status": "landed",
                "departure_time": "2025-01-27T10:00:00Z",
                "arrival_time": "2025-01-27T18:00:00Z",
            }
        ]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = agent.execute(
        api_key=VALID_API_KEY,
        flight_date="2025-01-27",
        dep_iata="LAX",
        arr_iata="JFK",
        flight_status="landed",
        limit=10,
        offset=5,
    )

    mock_get.assert_called_once_with(
        BASE_URL,
        params={
            "access_key": VALID_API_KEY,
            "flight_date": "2025-01-27",
            "dep_iata": "LAX",
            "arr_iata": "JFK",
            "flight_status": "landed",
            "limit": 10,
            "offset": 5,
        },
    )
    assert result["data"][0]["flight_status"] == "landed"


@patch("requests.get")
def test_health_check_healthy(mock_get, agent):
    """
    Test the health check method when the API is reachable.
    """
    mock_get.return_value.status_code = 200

    result = agent.health_check(api_key=VALID_API_KEY)
    assert result["status"] == "healthy"
    assert result["message"] == "AviationStack API is reachable."


@patch("requests.get")
def test_health_check_unhealthy(mock_get, agent):
    """
    Test the health check method when the API is unreachable.
    """
    mock_get.return_value.status_code = 500

    result = agent.health_check(api_key=VALID_API_KEY)
    assert result["status"] == "unhealthy"
    assert "error" in result



@patch("requests.get")
def test_invalid_json_response(mock_get, agent):
    """
    Test the behavior when the API returns an invalid JSON response.
    """
    # Simulate a response with invalid JSON
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "Invalid JSON Response"

    # Make the .json() method raise a JSONDecodeError
    mock_get.return_value.json.side_effect = json.JSONDecodeError("Expecting value", "Invalid JSON Response", 0)

    with pytest.raises(ValueError, match="Invalid JSON response from the API: Invalid JSON Response"):
        agent.execute(api_key="test_valid_api_key")
        agent.execute(api_key=VALID_API_KEY)



@patch("requests.get")
def test_missing_api_key(mock_get, agent):
    """
    Test the behavior when no API key is provided.
    """
    result = agent.execute(api_key="")
    expected_result = {
        "error": {
            "code": "missing_access_key",
            "message": "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"
        }
    }
    assert result == expected_result
    mock_get.assert_not_called() 
