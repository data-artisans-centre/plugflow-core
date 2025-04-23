import requests
from core.base import AgentBase
from log import logger

class EmailValidationAgent(AgentBase):
    """Agent to validate email addresses using the API Ninjas Validate Email API."""

    API_URL = "https://api.api-ninjas.com/v1/validateemail"

    def execute(self, email: str, api_key: str):
        """
        Validate the provided email address via external API.

        Args:
            email (str): The email address to validate.
            api_key (str): Your API Ninjas key.

        Returns:
            dict: Result of the validation containing status, validity, and metadata.

        Raises:
            ValueError: If the API fails or parameters are missing/invalid.
        """
        try:
            if not api_key:
                raise ValueError("Missing API Key. [Required format: api_key=YOUR_API_KEY]")

            if not email:
                raise ValueError("Missing email parameter. Provide a valid email.")

            logger.info(f"Validating email via API: {email}")
            response = requests.get(
                f"{self.API_URL}?email={email}",
                headers={"X-Api-Key": api_key}
            )

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Validation successful: {data}")
                return {"status": "success", "data": data}
            elif response.status_code == 401:
                logger.error("Unauthorized: Invalid API key.")
                raise ValueError("Unauthorized: Invalid API key.")
            elif response.status_code == 400:
                logger.error("Bad request: Invalid parameters or URL.")
                raise ValueError("Bad request: Invalid parameters or URL.")
            else:
                logger.error(f"API returned error: {response.status_code}, {response.text}")
                raise ValueError(f"API Error: {response.status_code} - {response.text}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise ValueError(f"An unexpected error occurred: {str(e)}") from e

    def health_check(self):
        """
        Check if the email validation API is reachable and functional.

        Returns:
            dict: Health status of the plugin.
        """
        try:
            test_email = "test@example.com"
            dummy_key = "test_key_should_fail"
            logger.info("Performing health check...")

            response = requests.get(
                f"{self.API_URL}?email={test_email}",
                headers={"X-Api-Key": dummy_key}
            )

            if response.status_code == 401:
                logger.info("Health check passed (received expected unauthorized response).")
                return {"status": "healthy", "message": "API reachable (unauthorized without valid key)"}
            else:
                logger.warning("Unexpected health check response.")
                return {"status": "unhealthy", "message": f"Unexpected status: {response.status_code}"}

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}

