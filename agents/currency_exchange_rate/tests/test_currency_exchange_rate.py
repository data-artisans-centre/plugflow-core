import pytest
import requests
from requests.exceptions import RequestException
from pydantic import ValidationError
from unittest.mock import patch
from agents.currency_exchange_rate import CurrencyExchangeAgent, CurrencyExchangeRequestModel

def test_valid_currency_exchange():
    """
    Test the fetcher's ability to fetch valid currency exchange rates.
    """
    fetcher = CurrencyExchangeAgent()
    mock_response = {
        "Realtime Currency Exchange Rate": {
            "1. From_Currency Code": "BTC",
            "2. From_Currency Name": "Bitcoin",
            "3. To_Currency Code": "EUR",
            "4. To_Currency Name": "Euro",
            "5. Exchange Rate": "99724.39000000",
            "6. Last Refreshed": "2024-12-16 06:09:02",
            "7. Time Zone": "UTC",
            "8. Bid Price": "99723.41700000",
            "9. Ask Price": "99727.33600000"
        }
    }
    
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        response = fetcher.execute(apikey="<KEY>", from_currency="BTC", to_currency="EUR")
        
        assert "Realtime Currency Exchange Rate" in response
        assert response["Realtime Currency Exchange Rate"]["1. From_Currency Code"] == "BTC"
        assert response["Realtime Currency Exchange Rate"]["3. To_Currency Code"] == "EUR"

def test_invalid_from_currency():
    """
    Test input validation when from_currency is invalid.
    """
    with pytest.raises(ValueError, match=r"Currency code must be exactly 3 uppercase letters.*"):
        CurrencyExchangeRequestModel(
            from_currency="123",
            to_currency="EUR",
            apikey="<KEY>"
        )

def test_invalid_to_currency():
    """
    Test input validation when to_currency is invalid.
    """
    with pytest.raises(ValueError, match="Currency code must be exactly 3 uppercase letters.*"):
        CurrencyExchangeRequestModel(
            from_currency="USD",
            to_currency="123",
            apikey="<KEY>"
        )

def test_missing_api_key():
    """
    Test validation error when API key is missing.
    """
    with pytest.raises(ValidationError, match="Field required"):
        CurrencyExchangeRequestModel(
            from_currency="USD",
            to_currency="EUR"
        )

def test_api_network_error():
    """
    Test fetcher handling of network errors.
    """
    fetcher = CurrencyExchangeAgent()
    with patch("requests.get") as mock_get:
        mock_get.side_effect = RequestException("Network error")
        
        with pytest.raises(ValueError, match="Network or API error"):
            fetcher.execute(apikey="<KEY>", from_currency="USD", to_currency="EUR")

def test_api_response_missing_key():
    """
    Test fetcher behavior when API response is missing required keys.
    """
    fetcher = CurrencyExchangeAgent()
    incomplete_response = {"Error Message": "Invalid API call."}

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = incomplete_response
        
        with pytest.raises(ValueError, match=r"Unexpected API response.*Realtime Currency Exchange Rate.*"):
            fetcher.execute(apikey="<KEY>", from_currency="USD", to_currency="EUR")

def test_health_check_success():
    """
    Test health check success when API returns valid response.
    """
    fetcher = CurrencyExchangeAgent()
    mock_response = {
        "Realtime Currency Exchange Rate": {
            "1. From_Currency Code": "USD",
            "3. To_Currency Code": "EUR"
        }
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_response
        
        result = fetcher.health_check(apikey="demo")
        assert result["status"] == "healthy"
        assert "API is operational" in result["message"]

def test_health_check_failure():
    """
    Test health check failure when API response is invalid.
    """
    fetcher = CurrencyExchangeAgent()

    with patch("requests.get") as mock_get:
        mock_get.side_effect = RequestException("API failure")
        
        result = fetcher.health_check(apikey="demo")
        assert result["status"] == "unhealthy"
        assert "API failure" in result["message"]

def test_api_with_large_currency_names():
    """
    Test the fetcher with unusually large currency codes (edge case).
    """
    fetcher = CurrencyExchangeAgent()
    large_currency_code = "BTCBTCBTCBTC"
    with pytest.raises(ValueError, match=r"Currency code must be exactly 3 uppercase letters.*"):
        fetcher.execute(apikey="<KEY>", from_currency=large_currency_code, to_currency="EUR")

def test_api_invalid_status_code():
    """
    Test fetcher behavior when API returns a non-200 status code.
    """
    fetcher = CurrencyExchangeAgent()
    with patch("requests.get") as mock_get:
        mock_get.side_effect = requests.RequestException("500 Internal Server Error")

        with pytest.raises(ValueError, match=r"Network or API error.*500.*"):
            fetcher.execute(apikey="<KEY>", from_currency="USD", to_currency="EUR")


def test_partial_api_response():
    """
    Test fetcher handling of partial response missing critical fields.
    """
    fetcher = CurrencyExchangeAgent()
    partial_response = {
        "Realtime Currency Exchange Rate": {
            "1. From_Currency Code": "USD"
        }
    }

    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = partial_response

        response = fetcher.execute(apikey="<KEY>", from_currency="USD", to_currency="EUR")
        assert "Realtime Currency Exchange Rate" in response
        assert response["Realtime Currency Exchange Rate"].get("3. To_Currency Code") is None

