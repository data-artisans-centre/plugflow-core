import json
import requests
from pydantic import BaseModel
from core.base import AgentBase
from log import logger

class ProfanityCheckResponse(BaseModel):
    """Model for profanity check response."""
    bad_words_list: list
    bad_words_total: int
    censored_content: str
    content: str


class ProfanityCheckerAgent(AgentBase):
    """Agent to detect and censor profanities in text."""

    API_URL = "https://api.apilayer.com/bad_words"

    def execute(self, text: str, api_key: str, censor_character: str = "*") -> dict:
        """
        Perform profanity check on the given text.

        Args:
            text (str): Text to check for profanity.
            api_key (str): The API key for authentication.
            censor_character (str): Character to use for censoring profanities. Defaults to '*'.

        Returns:
            dict: Dictionary containing profanity check details.

        Raises:
            ValueError: If the input text is invalid or the API call fails.
        """
        if not text.strip():
            raise ValueError("Input text cannot be empty.")

        url = f"{self.API_URL}?censor_character={censor_character}"
        headers = {"apikey": api_key}
        payload = text.encode("utf-8")

        try:
            logger.info("Sending request to profanity API.")
            response = requests.post(url, headers=headers, data=payload)

            if response.status_code != 200:
                logger.error(f"API call failed: {response.status_code} - {response.text}")
                raise ValueError("Failed to perform profanity check.")

            response_data = response.json()
            logger.info("Profanity check completed successfully.")
            return ProfanityCheckResponse(**response_data).model_dump()
        except Exception as e:
            logger.error(f"An error occurred during profanity check: {e}")
            raise ValueError("An error occurred while processing the request.") from e

    def health_check(self, api_key: str) -> dict:
        """
        Check if the profanity API is reachable.

        Args:
            api_key (str): The API key for authentication.

        Returns:
            dict: Health status of the agent.
        """
        try:
            logger.info("Performing health check for profanity API.")
            # Here we are performing a mock execution with dummy text to check if the API is reachable
            test_text = "This is a test."
            # Call the execute method with dummy text to simulate a real check
            self.execute(test_text, api_key)
            logger.info("Health check passed.")
            # Return a response that includes required fields
            return {
                "status": "healthy",
                "message": "Service is available"
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            # Return a response with error information
            return {
                "status": "unhealthy",
                "message": f"An error occurred: {str(e)}"
            }


