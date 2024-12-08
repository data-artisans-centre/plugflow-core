import requests
import json
from core.base import AgentBase
from log import logger

class WeatherAgent(AgentBase):
    """Agent to fetch real-time weather details for a given location."""

    def __init__(self,api_key):
        """
        Initialize the WeatherAgent with Weatherbit API configuration.
        """
        # You might want to use environment variables or a config file for API key
        self.api_key = api_key  # Replace with actual key
        self.base_url = "https://api.weatherbit.io/v2.0/current"

    def execute(self, **kwargs):
        """
        Fetch weather details based on input parameters.
        
        Args:
            kwargs (dict): Input arguments containing location details.
            Supported keys:
            - location (str, optional): City name
            - lat (float, optional): Latitude
            - lon (float, optional): Longitude
            - units (str, optional): 'M' for Metric, 'I' for Imperial
            - language (str, optional): Language code

        Returns:
            dict: Comprehensive weather information.
        """
        try:
            # Extract parameters with defaults
            location = kwargs.get('location')
            lat = kwargs.get('lat')
            lon = kwargs.get('lon')
            units = kwargs.get('units', 'M')
            language = kwargs.get('language', 'en')

            # Validate input - must have either location or lat/lon
            if not location and (lat is None or lon is None):
                raise ValueError("Either location or lat/lon must be provided")

            logger.info(f"Fetching weather for location: {location or f'Lat: {lat}, Lon: {lon}'}")

            # Prepare request parameters
            params = {
                "key": self.api_key,
                "units": units,
                "lang": language
            }

            # Add location parameters
            if location:
                params["city"] = location
            elif lat is not None and lon is not None:
                params["lat"] = lat
                params["lon"] = lon

            # Make API request
            response = requests.get(self.base_url, params=params)

            # Check if the request was successful
            if response.status_code != 200:
                raise ValueError(f"API request failed with status code {response.status_code}")

            # Parse JSON response
            weather_data = response.json()

            # Check if data is available
            if not weather_data.get('data'):
                raise ValueError("No weather data found")

            # Extract the first observation
            obs = weather_data['data'][0]

            # Parse weather information
            result = {
                "location": {
                    "name": obs.get("city_name", "Unknown"),
                    "country": obs.get("country_code", "Unknown"),
                    "latitude": obs.get("lat"),
                    "longitude": obs.get("lon")
                },
                "temperature": {
                    "current": obs.get("temp"),
                    "feels_like": obs.get("app_temp")
                },
                "weather": {
                    "description": obs.get("weather", {}).get("description", "Unknown"),
                    "code": obs.get("weather", {}).get("code"),
                    "icon": obs.get("weather", {}).get("icon")
                },
                "wind": {
                    "speed": obs.get("wind_spd"),
                    "direction": obs.get("wind_dir"),
                    "direction_full": obs.get("wind_cdir_full")
                },
                "humidity": obs.get("rh"),
                "pressure": {
                    "station": obs.get("pres"),
                    "sea_level": obs.get("slp")
                },
                "clouds": obs.get("clouds"),
                "visibility": obs.get("vis"),
                "solar_radiation": obs.get("solar_rad"),
                "uv_index": obs.get("uv"),
                "air_quality_index": obs.get("aqi")
            }

            logger.info("Successfully fetched weather information")
            return result

        except Exception as e:
            logger.error(f"An error occurred while fetching weather: {e}")
            return {"error": str(e), "status": "failed"}

    def health_check(self):
        """
        Check if the Weatherbit API connection is functional.
        
        Returns:
            dict: Health status of the agent.
        """
        try:
            logger.info("Performing Weatherbit API health check...")
            
            # Try to fetch weather for a default location (e.g., New York)
            params = {
                "key": self.api_key,
                "city": "New York,NY"
            }
            
            response = requests.get(self.base_url, params=params)
            
            if response.status_code == 200:
                logger.info("Weatherbit API health check passed.")
                return {"status": "healthy", "message": "Weatherbit API service is available"}
            else:
                raise ValueError(f"Health check failed with status code {response.status_code}")
        
        except Exception as e:
            logger.error(f"Weatherbit API health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}