from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from core.base import AgentBase
from log import logger
import yfinance as yf


class TickerRequest(BaseModel):
    """Model for ticker request inputs."""
    stock_tickers: str
    max_tickers: int = Field(5, ge=1, le=10, description="Maximum number of tickers to analyze")
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class TickerData(BaseModel):
    """Model for ticker data output."""
    ticker: str
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    price_change_percent: Optional[float] = None
    company_name: str = "N/A"
    sector: str = "N/A"
    market_cap: Optional[int] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    error: Optional[str] = None


class TickerAgent(AgentBase):
    """Agent to fetch and analyze ticker data."""

    def execute(self, ticker_request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Fetch and analyze ticker data for given tickers.

        Args:
            ticker_request (Dict[str, Any]): Dictionary containing ticker request parameters.

        Returns:
            List[Dict[str, Any]]: List of analyzed ticker data.
        """
        try:
            # Validate and parse input using Pydantic
            request = TickerRequest(**ticker_request)
            tickers = [ticker.strip().upper() for ticker in request.stock_tickers.split(",")[:request.max_tickers]]

            if not tickers:
                raise ValueError("No valid stock tickers provided.")

            # Analyze each ticker
            ticker_results = [self._analyze_single_ticker(ticker, request.start_date, request.end_date) for ticker in tickers]

            # Log results as JSON
            logger.info("Ticker analysis completed.")
            logger.debug(f"Analyzed Ticker Data: {ticker_results}")
            return [ticker.model_dump() for ticker in ticker_results]

        except ValidationError as ve:
            logger.error(f"Validation error: {ve}")
            raise ValueError(f"Invalid input: {ve}") from ve
        except Exception as e:
            logger.error(f"Ticker analysis failed: {e}")
            raise ValueError(f"Failed to analyze tickers: {e}") from e

    def _analyze_single_ticker(self, ticker: str, start_date: Optional[str], end_date: Optional[str]) -> TickerData:
        """
        Analyze a single ticker and return its data.

        Args:
            ticker (str): Ticker symbol.
            start_date (Optional[str]): Start date for historical data.
            end_date (Optional[str]): End date for historical data.

        Returns:
            TickerData: Analyzed ticker data model.
        """
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date, period="2d")

            current_price = hist['Close'][-1] if not hist.empty else None
            previous_close = hist['Close'][-2] if len(hist) > 1 else None
            price_change_percent = (
                ((current_price - previous_close) / previous_close) * 100
                if current_price and previous_close else None
            )

            info = stock.info
            return TickerData(
                ticker=ticker,
                current_price=current_price,
                previous_close=previous_close,
                price_change_percent=round(price_change_percent, 2) if price_change_percent else None,
                company_name=info.get("longName", "N/A"),
                sector=info.get("sector", "N/A"),
                market_cap=info.get("marketCap"),
                pe_ratio=info.get("trailingPE"),
                dividend_yield=info.get("dividendYield")
            )
        except Exception as e:
            logger.error(f"Error analyzing ticker {ticker}: {e}")
            return TickerData(ticker=ticker, error=str(e))

    def health_check(self) -> Dict[str, str]:
        """
        Perform a health check to verify the ticker analysis service.

        Returns:
            Dict[str, str]: Health status of the agent.
        """
        try:
            logger.info("Performing health check for Ticker Agent...")
            for ticker in ['AAPL', 'GOOGL', 'MSFT']:
                stock = yf.Ticker(ticker)
                _ = stock.info.get('regularMarketPrice')
            logger.info("Health check passed.")
            return {"status": "healthy", "message": "Ticker analysis service is operational."}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": f"Ticker data retrieval failed: {e}"}
