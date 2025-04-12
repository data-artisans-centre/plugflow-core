import pytest # type: ignore
from unittest.mock import patch, MagicMock
from agents.stock_intraday_analyzer import StockDataFetcher


# Mock data for a successful API response
MOCK_SUCCESS_RESPONSE = {
    "Meta Data": {
        "1. Information": "Intraday (1min) open, high, low, close prices and volume",
        "2. Symbol": "META",
        "3. Last Refreshed": "2020-01-31 19:59:00",
        "4. Interval": "1min",
        "5. Output Size": "Compact",
        "6. Time Zone": "US/Eastern",
    },
    "Time Series (1min)": {
        "2020-01-31 19:59:00": {
            "1. open": "200.6479",
            "2. high": "200.6479",
            "3. low": "200.6479",
            "4. close": "200.6479",
            "5. volume": "100",
        }
    },
}

# Mock data for an invalid symbol response
MOCK_ERROR_RESPONSE = {
    "Error Message": "Invalid API call. Please retry or visit the documentation for TIME_SERIES_INTRADAY."
}

# Test the execute method for a successful response
@patch("agents.stock_intraday_analyzer.requests.get")
def test_execute_success(mock_get):
    # Mock the response object
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_SUCCESS_RESPONSE
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    fetcher = StockDataFetcher()
    api_key = "mock_api_key"
    response = fetcher.execute(apikey=api_key, symbol="META", interval="1min", outputsize="compact")

    # Assertions
    assert "Meta Data" in response
    assert response["Meta Data"]["2. Symbol"] == "META"
    assert "Time Series (1min)" in response
    assert response["Time Series (1min)"]["2020-01-31 19:59:00"]["1. open"] == "200.6479"


# Test the execute method for an invalid symbol
@patch("agents.stock_intraday_analyzer.requests.get")
def test_execute_invalid_symbol(mock_get):
    # Mock the response object
    mock_response = MagicMock()
    mock_response.json.return_value = MOCK_ERROR_RESPONSE
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    fetcher = StockDataFetcher()
    api_key = "mock_api_key"

    with pytest.raises(ValueError, match="Invalid stock symbol: INVALID_SYMBOL"):
        fetcher.execute(apikey=api_key, symbol="INVALID_SYMBOL", interval="1min", outputsize="compact")


# Test the health_check method for a healthy API
@patch("agents.stock_intraday_analyzer.StockDataFetcher.execute")
def test_health_check_success(mock_execute):
    # Mock the execute method to return a success response
    mock_execute.return_value = MOCK_SUCCESS_RESPONSE

    fetcher = StockDataFetcher()
    api_key = "mock_api_key"
    health = fetcher.health_check(apikey=api_key)

    # Assertions
    assert health["status"] == "healthy"
    assert health["message"] == "Service is operational"


# Test the health_check method for an unhealthy API
@patch("agents.stock_intraday_analyzer.StockDataFetcher.execute")
def test_health_check_failure(mock_execute):
    # Mock the execute method to raise an exception
    mock_execute.side_effect = ValueError("Failed to fetch stock data")

    fetcher = StockDataFetcher()
    api_key = "mock_api_key"
    health = fetcher.health_check(apikey=api_key)

    # Assertions
    assert health["status"] == "unhealthy"
    assert "Failed to fetch stock data" in health["message"]
