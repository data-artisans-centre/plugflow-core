import requests
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Dict
from core.base import AgentBase
from log import logger
import re

class CurrencyExchangeRequestModel(BaseModel):
    """
    Pydantic model for validating currency exchange request parameters.
    """
    function: str = Field(default="CURRENCY_EXCHANGE_RATE", description="API function to fetch exchange rate.")
    from_currency: str = Field(..., description="Currency to convert from (e.g., USD, BTC).")
    to_currency: str = Field(..., description="Currency to convert to (e.g., USD, EUR).")
    apikey: str = Field(..., description="Your API key for Alpha Vantage API.")

    @field_validator("from_currency","to_currency")
    def validate_to_currency(cls, v):
        if not re.fullmatch(r"[A-Z]{3}", v):
            raise ValueError("Currency code must be exactly 3 uppercase letters.")
        return v

class CurrencyExchangeAgent(AgentBase):
    """
    Agent to fetch real-time currency exchange rates from Alpha Vantage API.
    """
    BASE_URL = "https://www.alphavantage.co/query"

    def execute(self, apikey: str, from_currency: str, to_currency: str) -> Dict:
        """
        Fetch the real-time exchange rate for a currency pair.
        
        Args:
            apikey (str): API key for authentication.
            from_currency (str): The currency to convert from (e.g., USD, BTC).
            to_currency (str): The currency to convert to (e.g., USD, EUR).

        Returns:
            Dict: JSON response containing exchange rate details.

        Raises:
            ValueError: If the request fails, or the response contains errors.
            ValidationError: If input parameters fail validation.
        """
        # Input Validation
        try:
            request_model = CurrencyExchangeRequestModel(
                from_currency=from_currency,
                to_currency=to_currency,
                apikey=apikey
            )
            logger.debug(f"Validated input parameters: {request_model}")
        except ValidationError as e:
            logger.error(f"Input validation failed: {e}")
            raise ValueError(f"Input validation failed: {e}")

        # Prepare API request parameters
        params = {
            "function": request_model.function,
            "from_currency": request_model.from_currency,
            "to_currency": request_model.to_currency,
            "apikey": request_model.apikey
        }
        logger.info(f"Fetching exchange rate for {from_currency} to {to_currency}")

        # Make API Request
        try:
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
            logger.debug(f"API response status code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Network or API error: {e}")
            raise ValueError(f"Network or API error: {e}")

        # Parse and Validate API Response
        json_response = response.json()
        if "Realtime Currency Exchange Rate" not in json_response:
            logger.error("Unexpected API response: Missing 'Realtime Currency Exchange Rate'")
            raise ValueError("Unexpected API response: Missing 'Realtime Currency Exchange Rate'")

        logger.info("Successfully fetched currency exchange rate.")
        return json_response

    def health_check(self, apikey: str) -> Dict:
        """
        Perform a health check to verify if the Alpha Vantage API is operational.

        Args:
            apikey (str): API key for authentication.

        Returns:
            Dict: Health status of the API.
        """
        logger.info("Performing health check for Alpha Vantage API.")
        try:
            response = self.execute(apikey=apikey, from_currency="USD", to_currency="EUR")
            if "Realtime Currency Exchange Rate" in response:
                return {"status": "healthy", "message": "API is operational."}
            else:
                return {"status": "unhealthy", "message": "API response missing expected keys."}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}

