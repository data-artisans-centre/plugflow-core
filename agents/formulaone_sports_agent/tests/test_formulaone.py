import pytest
import json
from unittest.mock import patch, MagicMock
from agents.formulaone_sports_agent import SportsAgent


@pytest.fixture
def sports_agent():
    """Fixture to initialize the SportsAgent."""
    return SportsAgent()


@patch("agents.formulaone_sports_agent.requests.get")
def test_health_check_success(mock_get, sports_agent):
    """Test health check returns a healthy status."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"api": {"code": 200}}  # Fixed API response
    mock_get.return_value = mock_response

    result = sports_agent.health_check(apikey="test_api_key")
    assert result["status"] == "healthy"


@patch("agents.formulaone_sports_agent.requests.get")
def test_health_check_failure(mock_get, sports_agent):
    """Test health check returns an unhealthy status on failure."""
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.json.return_value = {"api": {"error": "Invalid API key"}}  # Fixed API response
    mock_get.return_value = mock_response

    result = sports_agent.health_check(apikey="invalid_key")
    assert result["status"] == "unhealthy"
    assert "Invalid API key" in result["error"]


@patch("agents.formulaone_sports_agent.requests.get")
def test_execute_success(mock_get, sports_agent):
    """Test successful execution of API call."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": "Test API Response"}
    mock_get.return_value = mock_response

    with patch("builtins.input", side_effect=["1", "done"]):
        sports_agent.execute(apikey="test_api_key")

    mock_get.assert_called()


@patch("agents.formulaone_sports_agent.requests.get")
def test_execute_invalid_category(mock_get, sports_agent):
    """Test execution with invalid category input."""
    with patch("builtins.input", side_effect=["100"]):
        with pytest.raises(IndexError):
            sports_agent.execute(apikey="test_api_key")


@patch("agents.formulaone_sports_agent.requests.get")
def test_execute_invalid_api_key(mock_get, sports_agent):
    """Test execution with an invalid API key."""
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {"message": "Invalid API Key"}
    mock_get.return_value = mock_response

    with patch("builtins.input", side_effect=["1", "done"]):
        with pytest.raises(Exception):
            sports_agent.execute(apikey="invalid_key")
