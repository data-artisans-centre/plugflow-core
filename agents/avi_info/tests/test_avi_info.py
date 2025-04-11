import pytest
from unittest.mock import patch, Mock
import requests
from agents.avi_info import AviationDataFetcher


@pytest.fixture
def fetcher():
    """Fixture to initialize the AviationDataFetcher instance."""
    return AviationDataFetcher()


def test_execute_success(fetcher):
    """Test successful API call with valid API key and category."""
    mock_response = {"data": "some_data"}
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        mock_get.return_value.json.return_value = mock_response
        result = fetcher.execute(api_key="valid_key", category="airports")
        assert result == mock_response


def test_execute_missing_api_key(fetcher):
    """Test API call with missing API key."""
    result = fetcher.execute(api_key="", category="airports")
    assert result == {
        "error": {
            "code": "missing_access_key",
            "message": "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"
        }
    }


def test_execute_http_error(fetcher):
    """Test API call that returns an HTTP error (e.g., 404)."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=404,
            raise_for_status=Mock(side_effect=requests.exceptions.HTTPError("404 Client Error"))
        )
        result = fetcher.execute(api_key="valid_key", category="airports")
        assert result == {
            "error": {"code": "http_error", "message": "404 Client Error"}
        }


def test_execute_invalid_json(fetcher):
    """Test API call that returns invalid JSON."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=200,
            json=Mock(side_effect=ValueError("Invalid JSON"))
        )
        result = fetcher.execute(api_key="valid_key", category="airports")
        assert result == {
            "error": {"code": "invalid_json", "message": "The response returned invalid JSON."}
        }


def test_execute_request_exception(fetcher):
    """Test API call that raises a request exception (e.g., connection error)."""
    with patch("requests.get", side_effect=requests.RequestException("Connection error")):
        result = fetcher.execute(api_key="valid_key", category="airports")
        assert result == {
            "error": {"code": "request_exception", "message": "Connection error"}
        }


def test_execute_invalid_api_key(fetcher):
    """Test API call with an invalid API key."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=401,
            json=Mock(return_value={"error": {"code": "invalid_access_key", "message": "Invalid API Key."}})
        )
        result = fetcher.execute(api_key="invalid_key", category="airports")
        assert result["error"]["code"] == "invalid_access_key"


def test_execute_bad_request(fetcher):
    """Test API call that results in a bad request (400 error)."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=400,
            json=Mock(return_value={"error": {"code": "bad_request", "message": "Bad request."}})
        )
        result = fetcher.execute(api_key="valid_key", category="invalid_category")
        assert result["error"]["code"] == "bad_request"


def test_execute_rate_limit_exceeded(fetcher):
    """Test API call that exceeds the rate limit (429 error)."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=429,
            json=Mock(return_value={"error": {"code": "rate_limit_exceeded", "message": "Rate limit exceeded."}})
        )
        result = fetcher.execute(api_key="valid_key", category="airports")
        assert result["error"]["code"] == "rate_limit_exceeded"


def test_execute_server_error(fetcher):
    """Test API call that results in a server error (500 error)."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(
            status_code=500,
            json=Mock(return_value={"error": {"code": "server_error", "message": "Internal server error."}})
        )
        result = fetcher.execute(api_key="valid_key", category="airports")
        assert result["error"]["code"] == "server_error"


def test_health_check(fetcher):
    """Test the health check method for API availability."""
    with patch("requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200)
        result = fetcher.health_check(api_key="valid_key")
        assert result == {"status": "healthy", "message": "AviationStack API is reachable."}
