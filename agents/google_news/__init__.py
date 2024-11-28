import json  # For parsing and formatting JSON data
from core.base import AgentBase  # Base class for agents
from log import logger  # Logging utility
import requests  # For making HTTP requests


class NewsFetcher(AgentBase):
    """Agent to fetch news based on category and country."""

    VALID_COUNTRIES = {
        "au", "br", "ca", "cn", "eg", "fr", "de", "gr", "hk", "in", "ie", "il", "it",
        "jp", "nl", "no", "pk", "pe", "ph", "pt", "ro", "ru", "sg", "es", "se", "ch",
        "tw", "ua", "gb", "us"
    }
    VALID_CATEGORIES = {
        "general", "world", "nation", "business", "technology",
        "entertainment", "sports", "science", "health"
    }

    def execute(self, apikey, category, country, max_articles=5):
        """
        Executes the news fetching process.

        Args:
            category (str): The category of news to fetch.
            country (str): The 2-letter country code (ISO Alpha-2 format).
            max_articles (int, optional): Maximum number of articles to fetch. Defaults to 5.

        Returns:
            str: JSON-formatted string containing fetched news data.

        Raises:
            ValueError: If the inputs are invalid or the API call fails.
        """

        # Validate the category
        if category not in self.VALID_CATEGORIES:
            raise ValueError(f"Invalid category: '{category}'. Valid categories are: {', '.join(self.VALID_CATEGORIES)}")

        # Validate the country
        if country not in self.VALID_COUNTRIES:
            raise ValueError(f"Invalid country code: '{country}'. Valid country codes are: {', '.join(self.VALID_COUNTRIES)}")

        # Construct the API endpoint
        url = (
            f"https://gnews.io/api/v4/top-headlines?"
            f"category={category}&lang=en&country={country}&max={max_articles}&apikey={apikey}"
        )

        try:
            # Make a GET request to the API
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Parse and format the JSON response
            raw_data = response.json()
            news_data = json.dumps(raw_data, indent=4)  # `indent=4` adds human-readable formatting
            return news_data

        except requests.exceptions.RequestException as e:
            # Log the error and raise a ValueError with a user-friendly message
            logger.error(f"An error occurred: {e}")
            raise ValueError("Failed to fetch news. Please check your inputs and try again.") from e

    def health(self,apikey):
        """
        Performs a health check to verify the functionality of the NewsFetcher agent.

        Returns:
            dict: A dictionary containing the health status and a message.
        """
        try:
            logger.info("Performing health check...")
            # Test with a known valid country code and category
            url = (
                f"https://gnews.io/api/v4/top-headlines?"
                f"category=technology&lang=en&country=us&max=1&apikey={apikey}"
            )

            # Make a test request to the API
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for non-2xx responses

            # Attempt to parse the response JSON
            test_data = response.json()
            if "articles" in test_data and len(test_data["articles"]) > 0:
                logger.info("Health check passed.")
                return {"status": "healthy", "message": "Service is available"}
            else:
                raise ValueError("Unexpected response structure from API.")

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}

