import pytest
import requests
from unittest.mock import patch, Mock
from agents.google_news import NewsFetcher


@pytest.fixture
def news_fetcher_agent():
    """
    Fixture to provide an instance of NewsFetcher.
    This allows for reusable setup in tests.
    """
    return NewsFetcher()


@patch("agents.google_news.requests.get")  # Patching the requests.get method used in the NewsFetcher module
def test_execute_success(mock_get, news_fetcher_agent):
    """
    Test successful execution of the NewsFetcher.
    Ensures the execute method fetches news articles correctly when valid inputs are provided.
    """
    apikey = '<KEY>'
    category = "technology"
    country = "us"
    max_articles = 2

    # Mock API response with dummy articles
    mock_response = {
        "articles": [
            {"title": "Tech News 1", "description": "Description 1"},
            {"title": "Tech News 2", "description": "Description 2"},
        ]
    }
    mock_get.return_value.json.return_value = mock_response  # Configure mock to return the fake response
    mock_get.return_value.status_code = 200  # Set a successful HTTP status code

    # Call the execute method and validate the response
    result = news_fetcher_agent.execute(apikey, category, country, max_articles)
    assert '"Tech News 1"' in result  # Check if the first article title is in the result
    assert '"Tech News 2"' in result  # Check if the second article title is in the result


def test_execute_failure(news_fetcher_agent):
    """
    Test execution failure due to an invalid country code.
    Ensures the execute method raises a ValueError for invalid inputs.
    """
    apikey = '<KEY>'
    category = "technology"
    country = "invalid_country_code"

    # Expect a ValueError with a specific error message
    with pytest.raises(ValueError, match="Invalid country code"):
        news_fetcher_agent.execute(apikey, category, country, max_articles=1)


def test_health_check_success(news_fetcher_agent):
    """
    Test successful health check.
    Ensures the health method reports the service as healthy when the API is reachable.
    """
    apikey = '<KEY>'

    # Mock a valid health check response
    mock_response = {"articles": [{"title": "Health Check News"}]}

    # Patch the requests.get method to simulate a successful API call
    with patch("agents.google_news.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)  # Configure mock response

        # Call the health method and validate the response
        health = news_fetcher_agent.health(apikey)
        assert health["status"] == "healthy", "Expected health status to be 'healthy'."
        assert "Service is available" in health["message"], "Expected success message in health check."


def test_health_check_failure(news_fetcher_agent):
    """
    Test health check failure.
    Ensures the health method reports the service as unhealthy when the API call fails.
    """
    apikey = '<KEY>'

    # Patch the requests.get method to simulate an API failure
    with patch("agents.google_news.requests.get") as mock_get:
        mock_get.side_effect = Exception("Mocked service failure")  # Simulate an exception during the API call

        # Call the health method and validate the response
        health = news_fetcher_agent.health(apikey)
        assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
        assert "Mocked service failure" in health["message"], "Expected failure message in health check."
