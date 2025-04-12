import pytest
import requests
from pydantic import ValidationError
from agents.stock_daily import StockDailyFetcher, DailyRequestModel


def test_valid_request():
    """
    Test a valid request to the StockDailyFetcher with proper parameters.
    Ensures that the response contains expected keys.
    """
    fetcher = StockDailyFetcher()
    response = fetcher.execute(
        apikey="<KEY>",
        symbol="TSCO.LON",
        outputsize="full",
        datatype="json"
    )
    assert "Meta Data" in response, "Response missing 'Meta Data'"
    assert "Time Series (Daily)" in response, "Response missing 'Time Series (Daily)'"


def test_invalid_stock_symbol():
    """
    Test the behavior of StockDailyFetcher when an invalid stock symbol is provided.
    Ensures a ValueError is raised with an appropriate error message.
    """
    fetcher = StockDailyFetcher()
    with pytest.raises(ValueError, match="Invalid stock symbol"):
        fetcher.execute(
            apikey="<KEY>",
            symbol="INVALID_SYMBOL",
            outputsize="full",
            datatype="json"
        )


def test_invalid_output_size():
    """
    Test the validation of an invalid 'outputsize' parameter.
    Ensures a ValidationError is raised by the DailyRequestModel.
    """
    with pytest.raises(ValidationError, match="Invalid outputsize"):
        DailyRequestModel(
            symbol="TSCO.LON",
            apikey="<KEY>",
            outputsize="invalid_size",
            datatype="json"
        )


def test_invalid_datatype():
    """
    Test the validation of an invalid 'datatype' parameter.
    Ensures a ValidationError is raised by the DailyRequestModel.
    """
    with pytest.raises(ValidationError, match="Invalid datatype"):
        DailyRequestModel(
            symbol="TSCO.LON",
            apikey="<KEY>",
            outputsize="full",
            datatype="invalid_type"
        )


def test_network_error(monkeypatch):
    """
    Simulate a network error during the API call.
    Ensures that a ValueError is raised with the appropriate error message.
    """
    def mock_requests_get(*args, **kwargs):
        raise requests.RequestException("Network error")

    monkeypatch.setattr(requests, "get", mock_requests_get)

    fetcher = StockDailyFetcher()
    with pytest.raises(ValueError, match="Failed to fetch stock data"):
        fetcher.execute(
            apikey="<KEY>",
            symbol="TSCO.LON",
            outputsize="compact",
            datatype="json"
        )


def test_missing_api_key():
    """
    Test the behavior when the 'apikey' field is missing.
    Ensures a ValidationError is raised with the correct error message.
    """
    with pytest.raises(ValidationError, match=r"apikey\n  Field required \[type=missing.*"):
        DailyRequestModel(
            symbol="TSCO.LON",
            outputsize="compact",
            datatype="json"
        )


def test_health_check_success(monkeypatch):
    """
    Simulate a successful health check for the StockDailyFetcher.
    Ensures the health check returns a 'healthy' status.
    """
    def mock_execute(*args, **kwargs):
        return {
            "Meta Data": {"1. Information": "Daily Prices"},
            "Time Series (Daily)": {"2024-12-09": {}}
        }

    fetcher = StockDailyFetcher()
    monkeypatch.setattr(fetcher, "execute", mock_execute)

    status = fetcher.health_check(apikey="<KEY>")
    assert status["status"] == "healthy", "Health check status should be 'healthy'"
    assert "Service is operational" in status["message"], "Health check message is incorrect"


def test_health_check_failure(monkeypatch):
    """
    Simulate a failed health check for the StockDailyFetcher.
    Ensures the health check returns an 'unhealthy' status.
    """
    def mock_execute(*args, **kwargs):
        raise ValueError("API failure")

    fetcher = StockDailyFetcher()
    monkeypatch.setattr(fetcher, "execute", mock_execute)

    status = fetcher.health_check(apikey="<KEY>")
    assert status["status"] == "unhealthy", "Health check status should be 'unhealthy'"
    assert "API failure" in status["message"], "Health check message is incorrect"


def test_large_output_size():
    """
    Test fetching data with 'full' output size.
    Ensures that the response contains a large number of records.
    """
    fetcher = StockDailyFetcher()
    response = fetcher.execute(
        apikey="<KEY>",
        symbol="TSCO.LON",
        outputsize="full",
        datatype="json"
    )
    assert len(response["Time Series (Daily)"]) > 1000, "Expected more than 1000 records for full output size"

