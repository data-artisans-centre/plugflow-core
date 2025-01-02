import json  # For parsing and formatting JSON data
from core.base import AgentBase  # Base class for agents
from log import logger  # Logging utility
import requests  # For making HTTP requests
from pydantic import BaseModel,Field,ValidationError
from typing import List,Optional,Dict

class SearchRequestModel(BaseModel):
    """
   Pydantic model for validating google search request parameters.
   """
    engine: str=Field("google",description="Google Search Engine by default.")
    q: str = Field(..., description="Search query string.")
    location: Optional[str] = Field(None, description=" Where you want the search to originate.")
    gl: Optional[str] = Field(None, description="Country to use for the Google search (e.g., 'us' for the United States).")
    hl: Optional[str] = Field(None, description="Language to use for the Google search (e.g., 'en' for English).")
    apikey: str = Field(..., description="Your API key for SerAPI.")

class Search(AgentBase):

    BASE_URL = 'https://serpapi.com/search.json'

    def execute(self,query,location,gl,hl,apikey)->Dict:
        try:
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

        params = {
            "q":SearchRequestModel.q,
            "location":SearchRequestModel.location,
            "gl":SearchRequestModel.gl,
            "hl":SearchRequestModel.hl,
            "apikey":SearchRequestModel.apikey
        }
        logger.info(f"Getting search results for query: {query}")
        try:
            response = requests.get(self.BASE_URL, params=params)

           # Check for successful response
            if response.status_code == 200:
                #data = response.json()  # Parse the response JSON
                print("Search Results:")
                print(response)
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            logger.error(f"An error occurred: {e}")
            raise ValueError(f"error occured: {e}")



