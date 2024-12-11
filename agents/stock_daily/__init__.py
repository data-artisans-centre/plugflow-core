import requests
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional
from core.base import AgentBase
from log import logger


class DailyRequestModel(BaseModel):
    """Pydantic model for validating daily stock request parameters."""
    symbol: str = Field(..., description="Stock ticker symbol (e.g., IBM, RELIANCE.BSE)")
    apikey: str = Field(..., description="API key for Alpha Vantage")
    outputsize: str = Field("compact", description="Data output size ('compact' or 'full')")
    datatype: str = Field("json", description="Response format ('json') ")

    @field_validator("outputsize")
    def validate_outputsize(cls, value):
        valid_output_sizes = {"compact", "full"}
        if value not in valid_output_sizes:
            raise ValueError(f"Invalid outputsize: {value}. Valid options are {valid_output_sizes}.")
        return value

    @field_validator("datatype")
    def validate_datatype(cls, value):
        valid_datatypes = {"json"}
        if value not in valid_datatypes:
            raise ValueError(f"Invalid datatype: {value}. Valid options are {valid_datatypes}.")
        return value


class StockDailyFetcher(AgentBase):
    """Agent to fetch daily stock data from Alpha Vantage."""
    BASE_URL = "https://www.alphavantage.co/query"

    def execute(self, apikey: str, symbol: str, outputsize: str = "compact", datatype: str = "json") -> str:
        """
        Fetch daily stock data based on the provided parameters.

        Args:
            apikey (str): The API key for authentication.
            symbol (str): The stock symbol (e.g., 'IBM').
            outputsize (str): The size of the output data ('compact' or 'full').
            datatype (str): The response format ('json' or 'csv').

        Returns:
            str: JSON string or CSV string containing stock data.

        Raises:
            ValueError: If the request fails or the symbol is invalid.
        """
        params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
            "outputsize": outputsize,
            "datatype": datatype,
            "apikey": apikey,
        }

        logger.debug(f"Constructed URL with parameters: {params}")

        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to fetch stock data. Please check the API or network.")
            raise ValueError("Failed to fetch stock data. Please check the API or network.") from e

        data = response.json() if datatype == "json" else response.text

        if "Error Message" in data if datatype == "json" else "Error" in data:
            logger.error(f"Invalid stock symbol: {symbol}")
            raise ValueError(f"Invalid stock symbol: {symbol}")

        logger.info("Successfully fetched daily stock data.")
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
                outputsize="compact",
                datatype="json"
            )
            if "Meta Data" in test_result:
                return {"status": "healthy", "message": "Service is operational"}
            else:
                return {"status": "unhealthy", "message": "Unexpected API response"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}

