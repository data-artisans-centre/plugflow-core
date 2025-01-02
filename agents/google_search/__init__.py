import json  # For parsing and formatting JSON data
from core.base import AgentBase  # Base class for agents
from log import logger  # Logging utility
import requests  # For making HTTP requests
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional, Dict


class SearchRequestModel(BaseModel):
    """
    Pydantic model for validating Google search request parameters.
    """
    engine: str = Field("google", description="Google Search Engine by default.")
    q: str = Field(..., description="Search query string.")
    location: Optional[str] = Field(
        None, description="Where you want the search to originate."
    )
    gl: Optional[str] = Field(
        None, description="Country to use for the Google search (e.g., 'us' for the United States)."
    )
    hl: Optional[str] = Field(
        None, description="Language to use for the Google search (e.g., 'en' for English)."
    )
    apikey: str = Field(..., description="Your API key for SerpAPI.")


class Search(AgentBase):
    BASE_URL = 'https://serpapi.com/search.json'

    def execute(
            self,
            query: str,
            location: Optional[str] = None,
            gl: Optional[str] = None,
            hl: Optional[str] = None,
            apikey: str = ""
    ) -> Dict:
        """
        Executes a search query using SerpAPI.

        :param query: Search query string.
        :param location: Search location (optional).
        :param gl: Country for Google search (optional).
        :param hl: Language for Google search (optional).
        :param apikey: API key for SerpAPI.
        :return: Dictionary containing search results.
        """
        try:
            # Validate input parameters using the Pydantic model
            api_request = SearchRequestModel(
                q=query,
                location=location,
                gl=gl,
                hl=hl,
                apikey=apikey
            )
            logger.debug(f"Validated input parameters: {api_request}")

        except ValidationError as e:
            logger.error(f"Input validation failed: {e}")
            raise ValueError(f"Input validation failed: {e}")

        # Construct params from the validated Pydantic model
        params = {
            "q": api_request.q,
            "location": api_request.location,
            "gl": api_request.gl,
            "hl": api_request.hl,
            "apikey": api_request.apikey
        }
        logger.info(f"Getting search results for query: {api_request.q}")

        try:
            # Make the HTTP GET request
            response = requests.get(self.BASE_URL, params=params)

            # Check for successful response
            if response.status_code == 200:
                logger.info("Search results:")
                search_data = json.dumps(response.json(), indent=3)
                return search_data
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                raise ValueError(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            raise ValueError(f"An error occurred: {e}")

    def health_check(self, apikey: str) -> Dict:
        """
        Checks the health of the API by inspecting the search_metadata.status field.

        :param apikey: API key for SerpAPI.
        :return: Dictionary with the health status of the API.
        """
        try:
            response = requests.get(
                "https://serpapi.com/search",
                headers={"Authorization": apikey}
            )
            response_data = response.json()

            # Check if the status is available and successful
            status = response_data.get("search_metadata", {}).get("status")
            if response.status_code == 200 and status == "Success":
                return {"status": "healthy"}
            else:
                error_message = response_data.get("search_metadata", {}).get("error", "Unknown error")
                logger.error(f"Health check failed: {error_message}")
                return {"status": "unhealthy", "error": error_message}

        except Exception as e:
            logger.error(f"Health check exception: {e}")
            return {"status": "unhealthy", "error": str(e)}
