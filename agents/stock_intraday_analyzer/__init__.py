import requests
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional
from core.base import AgentBase
from log import logger


class IntradayRequestModel(BaseModel):
    """Pydantic model for validating intraday request parameters."""
    symbol: str = Field(..., description="Stock ticker symbol (e.g., META, IBM)")
    interval: str = Field(..., description="Time interval (1min, 5min, 15min, 30min, 60min)")
    apikey: str = Field(..., description="API key for Alpha Vantage")
    outputsize: str = Field("compact", description="Data output size ('compact' or 'full')")
    month: Optional[str] = Field(None, description="Specific month in YYYY-MM format (optional)")

    @field_validator("interval")
    def validate_interval(cls, value):
        valid_intervals = {"1min", "5min", "15min", "30min", "60min"}
        if value not in valid_intervals:
            raise ValueError(f"Invalid interval: {value}. Valid intervals are {valid_intervals}.")
        return value


class StockDataFetcher(AgentBase):
    """Agent to fetch intraday stock data from Alpha Vantage."""
    BASE_URL = "https://www.alphavantage.co/query"

    def execute(self, apikey: str, symbol: str, interval: str, outputsize: str = "compact", month: Optional[str] = None) -> str:
        """
        Fetch intraday stock data based on the provided parameters.

        Args:
            apikey (str): The API key for authentication.
            symbol (str): The stock symbol (e.g., 'META').
            interval (str): The time interval between data points (e.g., '1min').
            outputsize (str): The size of the output data ('compact' or 'full').
            month (Optional[str]): The month to fetch data for (e.g., '2020-01').

        Returns:
            str: JSON string containing stock data.

        Raises:
            ValueError: If the request fails or the symbol is invalid.
        """
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": apikey,
        }

        logger.debug(f"Constructed URL with parameters: {params}")

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to fetch stock data. Please check the API or network.")
            raise ValueError("Failed to fetch stock data. Please check the API or network.") from e

        data = response.json()

        if "Error Message" in data:
            logger.error(f"Invalid stock symbol: {symbol}")
            raise ValueError(f"Invalid stock symbol: {symbol}")

        logger.info("Successfully fetched stock data.")
        return data

    def health_check(self, apikey: str) -> dict:
        """
        Check if the Alpha Vantage API is operational.

        Args:
            apikey (str): API key for Alpha Vantage.

        Returns:
            dict: Health status of the API.
        """
        logger.info("Performing health check...")

        try:
            test_result = self.execute(
                apikey=apikey,
                symbol="IBM",
                interval="1min",
                outputsize="compact"
            )
            if "Time Series (1min)" in test_result:
                return {"status": "healthy", "message": "Service is operational"}
            else:
                return {"status": "unhealthy", "message": "Unexpected API response"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
