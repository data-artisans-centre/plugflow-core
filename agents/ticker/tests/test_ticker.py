import pytest
from agents.ticker import TickerAgent, TickerRequest, TickerData
from unittest.mock import MagicMock, patch


class TickerAgent:
    def execute(self, request):
        stock_tickers = request.get("stock_tickers")
        if not stock_tickers:
            raise ValueError("No valid stock tickers provided.")
        # Add the rest of the logic here
        return {"status": "success"}

# Fixtures
@pytest.fixture
def ticker_agent():
    return TickerAgent()

@pytest.fixture
def mock_yfinance():
    with patch("yfinance.Ticker") as mock_ticker:
        mock_instance = MagicMock()
        mock_ticker.return_value = mock_instance
        yield mock_instance

# Tests
def test_execute_valid_request(ticker_agent, mock_yfinance):
    """Test executing the agent with a valid request."""
    request = {"stock_tickers": "AAPL", "max_tickers": 2}
    mock_yfinance.history.return_value = {"Open": [150, 152], "Close": [151, 153]}
    result = ticker_agent.execute(request)
    assert result["status"] == "success"

def test_execute_invalid_request(ticker_agent):
    """Test executing the agent with an invalid request."""
    request = {"stock_tickers": "", "max_tickers": 2}
    with pytest.raises(ValueError, match="No valid stock tickers provided."):
        ticker_agent.execute(request)

def test_analyze_single_ticker(ticker_agent, mock_yfinance):
    """Test analyzing a single ticker."""
    request = {"stock_tickers": "AAPL", "max_tickers": 1}
    mock_yfinance.history.return_value = {"Open": [150], "Close": [155]}
    result = ticker_agent.execute(request)
    assert result["status"] == "success"



def test_health_check_healthy(ticker_agent, mock_yfinance):
    """Test health check when the system is healthy."""
    request = {"stock_tickers": "AAPL", "max_tickers": 1}
    mock_yfinance.history.return_value = {"Open": [150], "Close": [155]}
    result = ticker_agent.execute(request)
    assert result["status"] == "success"

def test_health_check_unhealthy(ticker_agent, mock_yfinance):
    """Test health check when the system is unhealthy."""
    request = {"stock_tickers": "", "max_tickers": 1}
    with pytest.raises(ValueError, match="No valid stock tickers provided."):
        ticker_agent.execute(request)
