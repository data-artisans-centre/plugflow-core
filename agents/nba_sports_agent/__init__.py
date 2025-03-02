import requests
import json  # For parsing and formatting JSON data
import logging
from urllib.parse import urlencode
from core.base import AgentBase  # Base class for agents

logger = logging.getLogger(__name__)

class Urls:
    @staticmethod
    def url_dict():
        return {
            "seasons": "https://v2.nba.api-sports.io/seasons",
            "leagues": "https://v2.nba.api-sports.io/leagues",
            "games": "https://v2.nba.api-sports.io/games",
            "games_statistics": "https://v2.nba.api-sports.io/games/statistics",
            "teams": "https://v2.nba.api-sports.io/teams",
            "teams_statistics": "https://v2.nba.api-sports.io/teams/statistics",
            "players": "https://v2.nba.api-sports.io/players",
            "players_statistics": "https://v2.nba.api-sports.io/players/statistics",
            "standings": "https://v2.nba.api-sports.io/standings"
        }

class SportsAgent(AgentBase):
    BASE_HEADERS = {
        "x-rapidapi-host": "v2.nba.api-sports.io"
    }
    @staticmethod
    def construct_url(base_url, params):
        query_string = urlencode(params)
        return f"{base_url}?{query_string}"

    @staticmethod
    def fetch_data(url, headers):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            raise

    def health_check(self, apikey: str):
        """
        Checks the health of the NBA API by inspecting the response code and error message.

        :param apikey: API key for the Football API.
        :return: Dictionary with the health status of the API.
        """
        try:
            response = requests.get(
                "https://v2.nba.api-sports.io/",
                headers={"x-apisports-key": apikey}  # Correct API header
            )
            response_data = response.json()

            if response.status_code == 200 and response_data.get("api", {}).get("code") == 200:
                return {"status": "healthy"}
            else:
                error_message = response_data.get("api", {}).get("error", "Unknown error")
                logger.error(f"Health check failed: {error_message}")
                return {"status": "unhealthy", "error": error_message}

        except Exception as e:
            logger.error(f"Health check exception: {e}")
            return {"status": "unhealthy", "error": str(e)}

        except Exception as e:
            logger.error(f"Health check exception: {e}")
            return {"status": "unhealthy", "error": str(e)}
    def execute(self, apikey=None):
        if not apikey:
            apikey = input("Enter your API key: ").strip()
            if not apikey:
                logger.error("API key is required.")
                raise ValueError("API key is required.")

        try:
            url_call = Urls.url_dict()
            logger.info("Available categories:")
            for i, category in enumerate(url_call.keys(), 1):
                logger.info(f"{i}. {category}")

            category_choice = int(input("Choose a category by number: "))
            if category_choice < 1 or category_choice > len(url_call):
                logger.error("Invalid category selection.")
                raise IndexError("Invalid category selection.")

            category = list(url_call.keys())[category_choice - 1]
            logger.info(f"Selected category: {category}")

            api_url = url_call[category]
            params = {}
            while True:
                param_name = input("Enter parameter name (or 'done' to finish): ").strip()
                if param_name.lower() == 'done':
                    break
                param_value = input(f"Enter value for '{param_name}': ").strip()
                params[param_name] = param_value

            final_url = self.construct_url(api_url, params)
            logger.info(f"Constructed API URL: {final_url}")

            headers = {**self.BASE_HEADERS, "x-rapidapi-key": apikey}
            response = self.fetch_data(final_url, headers)

            # Explicitly check for API key failure
            if response.get("message") == "Invalid API Key":
                logger.error("Invalid API key provided.")
                raise ValueError("Invalid API key")

            logger.info("API Response:")
            logger.info(json.dumps(response, indent=4))

        except ValueError as e:
            logger.error(f"Invalid input: {e}")
            raise
        except IndexError as e:
            logger.error(f"Category selection error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
