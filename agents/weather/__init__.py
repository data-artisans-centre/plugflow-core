import requests
from typing import Dict, Any, Optional
from log import logger
from core.base import AgentBase

class WeatherAgent(AgentBase):
    """Agent to fetch weather data using the Open Weather API from RapidAPI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the WeatherAgent with RapidAPI configuration.
        
        Args:
            api_key (str, optional): RapidAPI key
        """
        self.api_key = api_key
        self.base_url = "https://open-weather13.p.rapidapi.com"
        self.host = "open-weather13.p.rapidapi.com"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch weather details for the specified city.
        
        Args:
            **kwargs: Keyword arguments including:
                - api_key (str, optional): API key to override the instance key
                - city (str): Name of the city
                - country_code (str, optional): Two-letter country code
        
        Returns:
            dict: A dictionary containing the weather data or an error message.
        """
        try:
            api_key = kwargs.get('api_key', self.api_key)
            
            if not api_key:
                raise ValueError("API key must be provided")
            
            city = kwargs.get('city', '').strip()
            country_code = kwargs.get('country_code', '').strip()
            
            if not city:
                raise ValueError("City name cannot be empty")
            
            logger.info(f"Fetching weather for city: {city}")
            
            # Prepare request headers
            headers = {
                'x-rapidapi-key': api_key,
                'x-rapidapi-host': self.host
            }
            
            # Prepare URL
            if country_code:
                url = f"{self.base_url}/city/{city}/{country_code}"
            else:
                url = f"{self.base_url}/city/{city}"
            
            # Make API request
            logger.info(f"Making request to {url}")
            response = requests.get(url, headers=headers)
            
            # Handle API response
            if response.status_code == 200:
                weather_data = response.json()
                
                # Transform to a cleaner format
                result = {
                    "location": {
                        "name": city,
                        "country": country_code or weather_data.get("sys", {}).get("country", "Unknown")
                    },
                    "temperature": {
                        "current": weather_data.get("main", {}).get("temp"),
                        "feels_like": weather_data.get("main", {}).get("feels_like"),
                        "min": weather_data.get("main", {}).get("temp_min"),
                        "max": weather_data.get("main", {}).get("temp_max")
                    },
                    "weather": {
                        "description": weather_data.get("weather", [{}])[0].get("description", "Unknown"),
                        "main": weather_data.get("weather", [{}])[0].get("main", "Unknown"),
                        "icon": weather_data.get("weather", [{}])[0].get("icon")
                    },
                    "wind": {
                        "speed": weather_data.get("wind", {}).get("speed"),
                        "direction": weather_data.get("wind", {}).get("deg")
                    },
                    "humidity": weather_data.get("main", {}).get("humidity"),
                    "pressure": weather_data.get("main", {}).get("pressure"),
                    "clouds": weather_data.get("clouds", {}).get("all"),
                    "visibility": weather_data.get("visibility")
                }
                
                logger.info("Successfully fetched weather information")
                return result
            else:
                error_msg = f"API request failed with status code {response.status_code}"
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        error_msg = f"API error: {error_data['message']}"
                except:
                    pass
                logger.error(error_msg)
                return {"error": error_msg, "status": "failed"}
                
        except Exception as e:
            logger.error(f"An error occurred while fetching weather: {e}")
            return {"error": str(e), "status": "failed"}
    
    def health_check(self) -> Dict[str, str]:
        """
        Check if the Open Weather API connection is functional.
        
        Returns:
            dict: Health status of the agent
        """
        try:
            if not self.api_key:
                return {"status": "unhealthy", "message": "No API key provided"}
            
            logger.info("Performing Open Weather API health check...")
            
            # Testing with a common city
            headers = {
                'x-rapidapi-key': self.api_key,
                'x-rapidapi-host': self.host
            }
            
            test_url = f"{self.base_url}/city/london/GB"
            response = requests.get(test_url, headers=headers)
            
            if response.status_code == 200:
                logger.info("Open Weather API health check passed")
                return {"status": "healthy", "message": "Open Weather API service is available"}
            else:
                error_msg = f"Health check failed with status code {response.status_code}"
                try:
                    error_data = response.json()
                    if 'message' in error_data:
                        error_msg = f"Health check failed: {error_data['message']}"
                except:
                    pass
                raise ValueError(error_msg)
        
        except Exception as e:
            logger.error(f"Open Weather API health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}