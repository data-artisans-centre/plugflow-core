import json
from typing import List, Optional
import requests
from pydantic import BaseModel
from core.base import AgentBase
from log import logger


class FlightDetailsResponse(BaseModel):
    """
    Model for flight details response.

    Attributes:
        flight_date (str): Date of the flight (YYYY-MM-DD).
        departure_airport (str): Name of the departure airport.
        arrival_airport (str): Name of the arrival airport.
        airline_name (str): Name of the airline.
        flight_number (str): Flight number.
        flight_status (str): Current status of the flight (e.g., scheduled, active, landed).
        departure_time (str): Scheduled departure time.
        arrival_time (str): Scheduled arrival time.
        error (Optional[List[str]]): List of errors, if any.
    """
    flight_date: Optional[str]
    departure_airport: Optional[str]
    arrival_airport: Optional[str]
    airline_name: Optional[str]
    flight_number: Optional[str]
    flight_status: Optional[str]
    departure_time: Optional[str]
    arrival_time: Optional[str]
    error: Optional[List[str]]


class FlightDetailsAgent(AgentBase):
    """
    Agent to fetch flight details using the AviationStack API.

    Attributes:
        API_URL (str): Base URL for the AviationStack Flights endpoint.
    """
    API_URL = "https://api.aviationstack.com/v1/flights"

    def execute(
        self,
        api_key: str,
        **kwargs,
    ) -> dict:
        """
        Fetch flight details based on user-selected parameters.

        Args:
            api_key (str): The API key for authentication.
            kwargs: Optional parameters for the API request.

        Returns:
            dict: Dictionary containing flight details or errors.

        Raises:
            ValueError: If API key is missing or API call fails.
        """
        # Validate API key
        if not api_key or not api_key.strip():
            return {
                "error": {
                    "code": "missing_access_key",
                    "message": "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"
                }
            }
        
        params = {"access_key": api_key}

        # Include optional parameters from kwargs
        optional_params = [
            "flight_date", "callback", "limit", "offset", "flight_status", "dep_iata", 
            "arr_iata", "dep_icao", "arr_icao", "airline_name", "airline_iata", 
            "airline_icao", "flight_number", "flight_iata", "flight_icao", "min_delay_dep", 
            "min_delay_arr", "max_delay_dep", "max_delay_arr", "arr_scheduled_time_arr", 
            "arr_scheduled_time_dep"
        ]

        # Add each optional parameter if provided
        for param in optional_params:
            if param in kwargs and kwargs[param] is not None:
                params[param] = kwargs[param]

        logger.info(f"Fetching flight details with parameters: {params}")

        try:
            # Send the API request
            response = requests.get(self.API_URL, params=params)

            # Handle HTTP errors
            if response.status_code == 401:
                raise ValueError("Invalid API key provided.")
            elif response.status_code == 400:
                logger.error("Bad request: Invalid parameters.")
                raise ValueError("Bad request: Invalid or missing parameters.")
            elif response.status_code == 429:
                logger.error("Rate limit exceeded: Too many requests.")
                raise ValueError("Rate limit exceeded: Try again later.")
            elif 500 <= response.status_code < 600:
                logger.error(f"Server error occurred: {response.status_code}")
                raise ValueError(f"Unexpected server error: {response.status_code}")

            # Parse the JSON response
            try:
                response_data = response.json()
                if not isinstance(response_data, dict):
                    raise ValueError("Unexpected response structure.")
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON response from the API: {response.text}") from e
            except ValueError:
                raise ValueError("Unexpected response structure.")  # Handle other types like list, etc.

            return response_data

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise ValueError("Failed to connect to the AviationStack API.") from e

    def health_check(self, api_key: str) -> dict:
        """
        Check if the AviationStack API is reachable.

        Args:
            api_key (str): The API key for authentication.

        Returns:
            dict: Health status of the agent.
        """
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty.")

        try:
            response = requests.get(self.API_URL, params={"access_key": api_key})

            if response.status_code == 200:
                return {"status": "healthy", "message": "AviationStack API is reachable."}
            else:
                return {"status": "unhealthy", "error": f"API returned status code {response.status_code}."}

        except requests.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
