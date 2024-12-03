import pytest
import requests
from unittest.mock import patch, Mock
from agents.currency_rates import CurrencyRatesAgent

@pytest.fixture
def currency_rates_agent():
    """
    Fixture to provide an instance of CurrencyRatesAgent.
    """
    return CurrencyRatesAgent()

@patch("agents.currency_rates.requests.get")
def test_execute_success(mock_get, currency_rates_agent):
    """
    Test successful execution of the CurrencyRatesAgent.
    """
    api_key = '<KEY>'
    base_currency = "USD"
    target_currency = "GBP"

    # Mock API response
    mock_response = {
        "result": "success",
        "base_code": "USD",
        "target_code": "GBP",
        "conversion_rate": 0.75
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.status_code = 200

    result = currency_rates_agent.execute(api_key, base_currency, target_currency)
    assert "\"USD\"" in result
    assert "\"GBP\"" in result
    assert "\"conversion_rate\": 0.75" in result

def test_execute_failure(currency_rates_agent):
    """
    Test execution failure due to invalid inputs.
    """
    api_key = '<KEY>'
    base_currency = "INVALID"
    target_currency = "GBP"

    with pytest.raises(ValueError, match="Invalid currency code"):
        currency_rates_agent.execute(api_key, base_currency, target_currency)

def test_health_check_success(currency_rates_agent):
    """
    Test successful health check.
    """
    api_key = '<KEY>'

    # Mock response for health check
    mock_response = {
        "result": "success",
        "base_code": "USD",
        "target_code": "GBP",
        "conversion_rate": 0.75
    }

    with patch("agents.currency_rates.requests.get") as mock_get:
        mock_get.return_value = Mock(status_code=200, json=lambda: mock_response)

        health = currency_rates_agent.health_check(api_key)
        assert health["status"] == "healthy"
        assert "Service is available" in health["message"]

def test_health_check_failure(currency_rates_agent):
    """
    Test health check failure.
    """
    api_key = '<KEY>'

    with patch("agents.currency_rates.requests.get") as mock_get:
        mock_get.side_effect = Exception("Mocked service failure")

        health = currency_rates_agent.health_check(api_key)
        assert health["status"] == "unhealthy"
        assert "Mocked service failure" in health["message"]
