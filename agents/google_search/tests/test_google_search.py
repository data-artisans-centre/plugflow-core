import pytest
import requests
from unittest.mock import patch, Mock
from agents.google_search import Search  # Replace with your actual agent class path

@pytest.fixture
def google_search_agent():
    """
    Fixture to provide an instance of the Google Search agent.
    This allows for reusable setup in tests.
    """
    return Search()


@patch("agents.google_search.requests.get")  # Patching the requests.get method used in the Search module
def test_execute_success(mock_get, google_search_agent):
    """
    Test successful execution of the Google Search agent.
    Ensures the execute method fetches search results correctly when valid inputs are provided.
    """
    apikey = '<KEY>'
    query = "Rameshwaram Cafe"
    location = "Bangalore"
    gl = "IN"
    hl = "en"

    # Mock API response with dummy search results
    mock_response = {
        "search_metadata": {
            "status": "Success"
        },
        "search_results": [
            {"title": "Rameshwaram Cafe - Official Site", "link": "https://example.com"},
            {"title": "Rameshwaram Cafe Reviews", "link": "https://example.com/reviews"}
        ]
    }
    mock_get.return_value.json.return_value = mock_response  # Configure mock to return the fake response
    mock_get.return_value.status_code = 200  # Set a successful HTTP status code

    # Call the execute method and validate the response
    result = google_search_agent.execute(query=query, location=location, gl=gl, hl=hl, apikey=apikey)
    assert '"Rameshwaram Cafe - Official Site"' in result  # Check if the first search result title is in the result
    assert '"Rameshwaram Cafe Reviews"' in result  # Check if the second search result title is in the result


def test_execute_failure(google_search_agent):
    """
    Test execution failure due to invalid inputs.
    Ensures the execute method raises a ValueError for invalid inputs.
    """
    apikey = '<KEY>'
    query = ""
    location = "Bangalore"

    # Mock the input validation failure
    with patch("agents.google_search.SearchRequestModel") as mock_model:
        mock_model.side_effect = ValueError("Input validation failed")

        with pytest.raises(ValueError, match="Input validation failed"):
            google_search_agent.execute(query=query, location=location, gl="IN", hl="en", apikey=apikey)

def test_health_check_success(google_search_agent):
    """
    Test successful health check.
    Ensures the health_check method reports the service as healthy when the API is reachable.
    """
    apikey = '<KEY>'

    # Mock a valid health check response
    mock_response = {
        "search_metadata": {
            "status": "Success"
        }
    }

    with patch("agents.google_search.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)

        health = google_search_agent.health_check(apikey)
        assert health["status"] == "healthy"


def test_health_check_failure(google_search_agent):
    """
    Test failed health check.
    Ensures the health_check method reports the service as unhealthy when the API returns an error.
    """
    apikey = '<KEY>'

    # Mock a failed health check response
    mock_response = {
        "search_metadata": {
            "status": "Error",
            "error": "Invalid API key"
        }
    }

    with patch("agents.google_search.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=400, json=lambda: mock_response)

        health = google_search_agent.health_check(apikey)
        assert health["status"] == "unhealthy"
        assert health["error"] == "Invalid API key"
