import json
import re
import pytest
from unittest.mock import patch, MagicMock
from requests import HTTPError
from agents.bin_checker import BINCheckerAgent

# Mock response for a valid BIN check
def mock_valid_bin_check_response(*args, **kwargs):
    """Mock the valid BIN check response."""
    return {
        "status": "success",
        "bank_name": "Diners Club International",
        "bin": "302596",
        "country": "United States Of America",
        "scheme": "Discover",
        "type": "Credit",
        "url": "www.dinersclub.com",
    }

@pytest.fixture
def bin_checker_agent():
    """Fixture to initialize the BINCheckerAgent."""
    return BINCheckerAgent()

@patch("requests.get")
def test_execute_success(mock_get, bin_checker_agent):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json = MagicMock(return_value=mock_valid_bin_check_response())

    response = bin_checker_agent.execute("302596", "valid-api-key")
    assert response["status"] == "success"
    assert response["bank_name"] == "Diners Club International"

@patch("requests.get")
def test_execute_bin_not_found(mock_get, bin_checker_agent):
    # Mock the API response for BIN not found
    mock_get.return_value.status_code = 404
    mock_get.return_value.json = MagicMock(return_value={
        "status": "not_found",
        "message": "The BIN code does not exist in the database.",
    })

    response = bin_checker_agent.execute("123456", "valid-api-key")

    assert response["status"] == "not_found"
    assert response["message"] == "The BIN code does not exist in the database."

@patch("requests.get")
def test_execute_missing_status_key(mock_get, bin_checker_agent):
    """Test execution when the 'status' key is missing in the API response."""
    # Mock the API response with a valid status code but missing 'status' key
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}  # Missing 'status' key
    mock_get.return_value = mock_response

    # Execute and verify no exception is raised
    result = bin_checker_agent.execute("123456", "valid_api_key")
    assert result == {}, "The response should be returned as-is when no 'status' key is present."

@patch("requests.post")
def test_execute_invalid_bin_code(mock_post, bin_checker_agent):
    bin_code = "ABC123"
    api_key = "valid-api-key"

    with pytest.raises(ValueError, match="BIN code must be a 6-digit number."):
        bin_checker_agent.execute(bin_code, api_key)

@patch("requests.get")
def test_execute_invalid_api_key(mock_get, bin_checker_agent):
    """Test execution with an invalid API key."""
    # Mock the API response for an invalid API key
    mock_response = MagicMock()
    mock_response.status_code = 401  # Simulate unauthorized access
    mock_response.json.return_value = {"message": "Invalid API key."}  # Example response body
    mock_get.return_value = mock_response

    # Verify the exception is raised with the correct message
    with pytest.raises(ValueError, match=r"Invalid API key provided."):
        bin_checker_agent.execute("123456", "invalid_api_key")

@patch("requests.post")
def test_health_check_success(mock_post, bin_checker_agent):
    # Mock the API response for health check
    mock_post.return_value.status_code = 200
    mock_post.return_value.json = MagicMock(return_value={"status": "healthy"})

    health_status = bin_checker_agent.health_check("valid-api-key")
    assert health_status["status"] == "healthy"

@patch("requests.post")
def test_health_check_failure(mock_post, bin_checker_agent):
    # Mock the API response for health check failure
    mock_post.return_value.status_code = 500
    mock_post.return_value.json = MagicMock(return_value={"status": "unhealthy"})

    with pytest.raises(ValueError):
        bin_checker_agent.health_check("invalid-api-key")

@patch("requests.get")
def test_execute_unexpected_response(mock_get, bin_checker_agent):
    """Test execution with an unexpected response from the API."""
    # Mock the API response for an unexpected status code
    mock_response = MagicMock()
    mock_response.status_code = 500  # Simulate server error
    mock_response.text = "Internal Server Error"
    mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "", 0)  # Simulate invalid JSON
    mock_get.return_value = mock_response

    # Execute and verify the exception message
    with pytest.raises(ValueError, match=r"Unexpected server error: 500"):
        bin_checker_agent.execute("123456", "test_api_key")
