import json
import requests
import os
from typing import Optional
from pydantic import BaseModel
from core.base import AgentBase
from log import logger

class PDFConversionResponse(BaseModel):
    """
    Model for PDF conversion response.

    Attributes:
        conversion_cost (int): The cost of the conversion in API credits.
        file_name (str): Name of the output PDF file.
        file_url (str): URL to download the converted PDF.
        status (str): Status of the conversion (success or error).
        error (Optional[str]): Error message in case of failure.
    """
    conversion_cost: Optional[int]
    file_name: Optional[str]
    file_url: Optional[str]
    status: str
    error: Optional[str]

class URLToPDFConverter(AgentBase):
    """
    Agent to convert a given URL into a PDF using ConvertAPI.

    Attributes:
        API_URL (str): Base URL for the ConvertAPI endpoint.
    """
    API_URL = "https://v2.convertapi.com/convert/web/to/pdf"

    def execute(self, url: str, api_key: str, output_dir: Optional[str] = None, file_name: str = "output") -> dict:
        
        """
        Convert the given URL into a PDF.

        Args:
            url (str): The URL to be converted to a PDF.
            api_key (str): API key for authentication.
            output_dir (Optional[str]): Directory to save the converted PDF. If None, file is not saved locally.
            file_name (str): Desired name of the output PDF file (default: "output").

        Returns:
            dict: Dictionary containing the conversion response details.

        Raises:
            ValueError: If the API call fails or required parameters are invalid.
        """
        if not url:
            raise ValueError("URL cannot be empty.")
        if not api_key:
            raise ValueError("API key cannot be empty.")
        
        # URL encoding (if necessary)
        url = requests.utils.quote(url)

        payload = {
            "Url": url,
            "FileName": file_name
        }
        headers = {
            "Authorization": f"Bearer {api_key}"
        }

        logger.info(f"Initiating PDF conversion for URL: {url}")

        try:
            response = requests.post(self.API_URL, headers=headers, json=payload)
            response.raise_for_status()

            # Handle API error responses based on status codes
            if response.status_code == 401:
                raise ValueError("Invalid API key provided.")
            elif response.status_code == 400:
                raise ValueError("Bad request: Invalid parameters or URL.")
            elif response.status_code == 429:
                raise ValueError("Rate limit exceeded: Try again later.")
            elif response.status_code >= 500:
                raise ValueError(f"Server error: {response.status_code}")

            response_data = response.json()

            if "Files" not in response_data:
                raise ValueError("Unexpected response format from the API. No 'Files' key found.")

            file_info = response_data["Files"][0]
            file_url = file_info["Url"]

            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
                file_path = os.path.join(output_dir, file_info['FileName'])
                pdf_response = requests.get(file_url)
                with open(file_path, "wb") as pdf_file:
                    pdf_file.write(pdf_response.content)
                logger.info(f"PDF conversion successful. File saved at: {file_path}")

            return {
                "conversion_cost": response_data.get("ConversionCost", 0),
                "file_name": file_info["FileName"],
                "file_url": file_url,
                "status": "success"
            }

        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise ValueError(f"Failed to connect to the ConvertAPI: {str(e)}") from e
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise ValueError(f"An unexpected error occurred: {str(e)}") from e

    
    def health_check(self, api_key: str) -> dict:
        """
        Check if the ConvertAPI service is reachable.

        Args:
            api_key (str): API key for authentication.

        Returns:
            dict: Health status of the service.

        Raises:
            ValueError: If the health check fails.
        """
        url = f"https://v2.convertapi.com/health"
        headers = {"Authorization": f"Bearer {api_key}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            response_data = response.json()
            if response_data.get("status") == "healthy":
                logger.info("ConvertAPI service is healthy.")
                return response_data
            else:
                raise ValueError("ConvertAPI service is unhealthy.")
        except requests.RequestException as e:
            logger.error(f"Health check failed: {e}")
            raise ValueError("Failed to connect to the ConvertAPI service.") from e
