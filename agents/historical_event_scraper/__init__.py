import json
from datetime import datetime
from core.base import AgentBase
from log import logger
import requests

class HistoricalEventsAgent(AgentBase):
    """Agent to fetch historical events for the current date."""

    def execute(self, month, day):
        """
        Fetch historical events for today's date from the API and return as a list of dictionaries.

        Returns:
            list: A list of dictionaries containing historical event data.

        Raises:
            ValueError: If the API request fails or data cannot be retrieved.
        """
        try:
            # Get the current date
            today = datetime.now()
            # month = today.month
            # day = today.day

            # Construct the API URL
            url = f"https://byabbe.se/on-this-day/{month}/{day}/events.json"
            logger.info(f"Fetching events from URL: {url}")

            # Fetch data from the API
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse JSON response
            events_data = response.json()
            events = events_data.get("events", [])
            
            # Convert the list of events to a JSON-formatted string
            events_json = json.dumps(events, indent=4)

            # Log the JSON-formatted events
            print(f"Historical Events on {today.strftime('%B %d')}:\n{events_json}")

            return events
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise ValueError("Failed to fetch historical events. Please check the API or your connection.") from e

    def health_check(self):
        """
        Check if the On This Day API is functional.

        Returns:
            dict: Health status of the plugin.
        """
        try:
            logger.info("Performing health check...")
            
            # Test the API with a known valid date
            test_url = "https://byabbe.se/on-this-day/1/1/events.json"
            response = requests.get(test_url)
            response.raise_for_status()
            
            # Attempt to parse and fetch the first event
            test_data = response.json()
            if "events" in test_data and test_data["events"]:
                logger.info("Health check passed.")
                return {"status": "healthy", "message": "Service is available"}
            else:
                raise ValueError("No events data found in the response.")
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
