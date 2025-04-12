import json
import requests
from typing import Dict, Any
from log import logger
from core.base import AgentBase

class MovieHiveAgent(AgentBase):
    """Agent to fetch movie information using the OMDB API."""
    
    def __init__(self):
        """Initializing the MovieHive agent."""
        self.base_url = "http://www.omdbapi.com/"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch movie information based on title.
        
        Args:
            **kwargs: Keyword arguments including:
                - title: Movie title to search for
                - api_key: OMDB API key
        
        Returns:
            dict: A dictionary containing movie information or an error message.
        """
        try:
            # Passing required parameters
            title = kwargs.get("title", "").strip()
            api_key = kwargs.get("api_key", "").strip()
            
            if not title:
                raise ValueError("Movie title cannot be empty.")
            if not api_key:
                raise ValueError("API key cannot be empty.")
            
            # Building the query parameters with plot always set to full for fetching all the details
            params = {
                "apikey": api_key,
                "t": title,
                "plot": "full"
            }
            
            # Sending the API request
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if data.get("Response") == "True":
                return data
            else:
                return {"error": data.get("Error", "No movie found with the provided title.")}
        
        except Exception as e:
            logger.error(f"Movie information fetching error: {e}")
            return {"error": f"Failed to fetch movie information. {str(e)}"}
    
    def health_check(self, api_key: str) -> Dict[str, str]:
        """
        Perform a health check on the OMDB API service.
        
        Args:
            api_key: OMDB API key
            
        Returns:
            Dict with service health status.
        """
        try:
            logger.info("Performing OMDB API health check...")
            
            if not api_key:
                raise ValueError("API key cannot be empty.")
                
            # Testing with the following parameters
            test_params = {
                "apikey": api_key,
                "t": "The Godfather",
                "plot": "full"
            }
            
            response = requests.get(self.base_url, params=test_params)
            data = response.json()
            
            if data.get("Response") == "True":
                logger.info("OMDB API health check passed.")
                return {"status": "healthy", "message": "OMDB API is operational"}
            else:
                raise Exception(f"OMDB API test request failed: {data.get('Error')}")
        
        except Exception as e:
            logger.error(f"OMDB API health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}