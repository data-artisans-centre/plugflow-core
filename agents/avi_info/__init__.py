import json
import os
from typing import Any, Dict, Optional, List
import requests
from pydantic import BaseModel, ValidationError
from core.base import AgentBase
from log import logger


class AviationDataResponse(BaseModel):
    """
    Model for aviation data response.

    Attributes:
        data (Optional[List[Dict[str, Any]]]): List of aviation data.
        error (Optional[Dict[str, Any]]): Error details if any.
    """
    data: Optional[List[Dict[str, Any]]]
    error: Optional[Dict[str, Any]]


class AviationDataFetcher(AgentBase):
    """
    Agent to fetch aviation data from AviationStack API.

    Attributes:
        BASE_URL (str): Base URL for the AviationStack API.
    """
    BASE_URL = "https://api.aviationstack.com/v1/"

    def execute(self, api_key, category, **params) -> dict:
        """
        Fetch aviation data for a given category.

        Args:
            api_key (str): The API key for authentication.
            category (str): The type of data to fetch (airports, airlines, etc.).
            kwargs: Optional parameters for the API request.

        Returns:
            dict: Dictionary containing aviation data or errors.

        Raises:
            ValueError: If API key is missing or API call fails.
        """
        # Validate API key
        if not api_key :
            return {
                "error": {
                    "code": "missing_access_key",
                    "message": "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"
                }
            }

        params["access_key"] = api_key

        try:
            response = requests.get(f"{self.BASE_URL}{category}", params=params)
            response.raise_for_status()
            try:
                response_data = response.json()
            except (json.JSONDecodeError, ValueError):
                return {"error": {"code": "invalid_json", "message": "The response returned invalid JSON."}}

            if "error" in response_data:
                return {"error": response_data["error"]}
            return response_data

        except requests.exceptions.HTTPError as http_err:
            return {"error": {"code": "http_error", "message": str(http_err)}}
        except requests.exceptions.RequestException as req_err:
            return {"error": {"code": "request_exception", "message": str(req_err)}}
        except Exception as e:
            return {"error": {"code": "unknown_error", "message": str(e)}}
        
    def health_check(self, api_key: str) -> dict:
        """
        Check if the AviationStack API is reachable.

        Args:
            api_key (str): The API key for authentication.

        Returns:
            dict: Health status of the agent.
        """
        if not api_key or not api_key.strip():
            return {
                "error": {
                    "code": "missing_access_key",
                    "message": "You have not supplied an API Access Key. [Required format: access_key=YOUR_ACCESS_KEY]"
                }
            }

        try:
            response = requests.get(f"{self.BASE_URL}airports", params={"access_key": api_key})

            if response.status_code == 200:
                return {"status": "healthy", "message": "AviationStack API is reachable."}
            else:
                logger.error(f"Health check failed with status code {response.status_code}")
                return {"status": "unhealthy", "error": f"API returned status code {response.status_code}."}

        except requests.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "error": str(e)}
