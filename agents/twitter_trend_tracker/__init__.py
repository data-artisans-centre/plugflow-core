import requests
import json
from core.base import AgentBase
from log import logger
from .utils import WOEIDLocations

class TwitterTrendingAgent(AgentBase):
    """Agent to fetch trending tweets using RapidAPI."""

    def __init__(self):
        """
        Initialize the Twitter agent with RapidAPI authentication.
        """
        self.rapid_api_key = '043ca59f1fmsh4888cbf47d4856bp1a242ajsn9fbcf042a9b0'
        self.rapid_api_host = 'twitter-x.p.rapidapi.com'

        self.headers = {
            "X-RapidAPI-Key": self.rapid_api_key,
            "X-RapidAPI-Host": self.rapid_api_host
        }
        self.base_url = "https://twitter-x.p.rapidapi.com/trends/"

    def execute(self, **kwargs):
        """
        Fetch trending tweets based on keyword arguments with country name.
        
        Args:
            kwargs (dict): Input arguments containing 'country' and 'max_trends'.
            
        Returns:
            dict: A dictionary containing trending topics and location information.
        """
        try:
            # Parse input parameters
            country_name = kwargs.get("country", "").strip()
            max_trends = kwargs.get("max_trends", 10)

            # Find location by country name
            selected_location = WOEIDLocations.find_location_by_name(country_name)

            if not selected_location:
                raise ValueError(f"No WOEID found for country: {country_name}")

            woeid = selected_location["woeid"]

            logger.info(f"Fetching trending tweets for {selected_location['name']} (WOEID: {woeid})")

            # API endpoint for trends by WOEID
            url = f"{self.base_url}by_woeid/"
            querystring = {"woeid": woeid}

            response = requests.get(url, headers=self.headers, params=querystring)

            # Check if the request was successful
            if response.status_code != 200:
                raise ValueError(f"API request failed with status code {response.status_code}")

            # Parse the response
            trends_data = response.json()

            # Process and limit trends
            processed_trends = []
            for trend in trends_data[:max_trends]:
                trend_info = {
                    "name": trend.get("name", ""),
                    "tweet_volume": trend.get("tweet_volume", 0),
                    "url": trend.get("url", ""),
                    "promoted_content": trend.get("promoted_content", False),
                }
                processed_trends.append(trend_info)

            # Prepare return dictionary
            result = {
                "location": {
                    "name": selected_location["name"],
                    "country": selected_location["country"],
                    "woeid": woeid,
                },
                "trends": processed_trends,
            }

            # Log the results
            logger.info(f"Fetched {len(processed_trends)} trending topics")

            return result

        except Exception as e:
            logger.error(f"An error occurred while fetching trends: {e}")
            return {"error": str(e), "status": "failed"}

    def health_check(self):
        """
        Check if the RapidAPI Twitter connection is functional.
        
        Returns:
            dict: Health status of the plugin.
        """
        try:
            logger.info("Performing RapidAPI Twitter health check...")
            
            # Try to fetch global trends as a basic connectivity test
            url = f"{self.base_url}by_woeid/"
            querystring = {"woeid": 1}  # Global trends
            
            response = requests.get(url, headers=self.headers, params=querystring)
            
            if response.status_code == 200:
                logger.info("RapidAPI Twitter health check passed.")
                return {"status": "healthy", "message": "Twitter API service is available"}
            else:
                raise ValueError(f"Health check failed with status code {response.status_code}")
        
        except Exception as e:
            logger.error(f"RapidAPI Twitter health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
