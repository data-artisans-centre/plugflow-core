import json
from typing import List, Optional
import requests
from pydantic import BaseModel
from core.base import AgentBase
from log import logger


class BINCheckResponse(BaseModel):
    """
    Model for BIN check response.
    
    Attributes:
        bank_name (str): Name of the issuing bank or institution.
        bin (str): The BIN code.
        country (str): Country of issuance.
        scheme (str): Card scheme or network (e.g., Visa, MasterCard).
        type (str): Type of the card (Credit/Debit).
        url (str): URL of the issuing institution.
    """
    bank_name: Optional[str]
    bin: Optional[str]
    country: Optional[str]
    scheme: Optional[str]
    type: Optional[str]
    url: Optional[str]
    status: Optional[str]
    data: Optional[dict]
    error: Optional[List[str]]


class BINCheckerAgent(AgentBase):
    """
    Agent to check and retrieve information about Bank Identification Numbers (BINs).
    
    Attributes:
        API_URL (str): Base URL for the BIN Checker API.
    """
    API_URL = "https://api.apilayer.com/bincheck"  # Replace with the actual BIN Checker API endpoint

    def execute(self, bin_code: str, api_key: str) -> dict:
        """
        Retrieve information for a given BIN code.

        Args:
            bin_code (str): The BIN code to retrieve information for (6-digit number).
            api_key (str): The API key for authentication.

        Returns:
            dict: Dictionary containing BIN information.

        Raises:
            ValueError: If the BIN code is invalid or the API call fails.
        """
        # Validate that the BIN code is a 6-digit number
        if not bin_code.isdigit() or len(bin_code) != 6:
            raise ValueError("BIN code must be a 6-digit number.")
    
        if not api_key:
            raise ValueError("API key cannot be empty.")

        url = f"{self.API_URL}/{bin_code}"
        headers = {"apikey": api_key}
        logger.info(f"Fetching BIN information for {bin_code}.")

        try:
            response = requests.get(url, headers=headers)

            # Handle known status codes without relying on specific fields
            if response.status_code == 401:
                raise ValueError("Invalid API key provided.")
            elif response.status_code == 404:
                logger.warning(f"BIN code {bin_code} not found.")
                return {"status": "not_found", "message": "The BIN code does not exist in the database."}
            elif response.status_code == 400:
                logger.error("Bad request: Invalid parameters.")
                raise ValueError("Bad request: Invalid or missing parameters.")
            elif response.status_code == 429:
                logger.error("Rate limit exceeded: Too many requests.")
                raise ValueError("Rate limit exceeded: Try again later.")
            elif 500 <= response.status_code < 600:
                logger.error(f"Server error occurred: {response.status_code} - {response.text}")
                raise ValueError(f"Unexpected server error: {response.status_code}")

            # Parse the JSON response if the status code is 200
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON response: {response.text}")
                raise ValueError("Invalid JSON response from the API.")
            
            # Handle unexpected response structure
            if not isinstance(response_data, dict):
                raise ValueError("Unexpected response structure.")

            return response_data

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise ValueError("Failed to connect to the BIN Checker API.") from e
        
    def health_check(self, api_key: str) -> dict:
        """
        Check if the BIN Checker API is reachable.

        Args:
            api_key (str): The API key for authentication.

        Returns:
            dict: Health status of the agent.
        """
        # Test with a valid example BIN code for health check
        url = f"{self.API_URL}/health"
        headers = {"apikey": api_key}

        try:
            response = requests.post(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            response_data = response.json()

            if response_data.get("status") == "healthy":
                return response_data
            else:
                raise ValueError("Health check failed: API status is unhealthy.")
    
        except ConnectionError:
            logger.error("Unable to connect to the API server.")
            raise ValueError("Health check failed: Unable to connect to the API server.")
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            raise ValueError(f"Health check failed due to unexpected error: {e}")