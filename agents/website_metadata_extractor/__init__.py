import requests
import json
from bs4 import BeautifulSoup
from core.base import AgentBase
from log import logger

class WebsiteMetadataAgent(AgentBase):
    """Agent to extract metadata from a website."""

    def execute(self, url):
        """Extract metadata from a website."""
        try:
            logger.info(f"Fetching metadata for URL: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise error for HTTP issues

            soup = BeautifulSoup(response.content, "html.parser")
            metadata = {
                "Title": self._get_meta_data(soup, "title"),
                "Meta Description": self._get_meta_data(soup, "description"),
                "Meta Keywords": self._get_meta_data(soup, "keywords"),
            }
            metadata_json = json.dumps(metadata, indent=4)
            logger.info(f"Extracted Metadata:\n{metadata_json}")
            return metadata

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise ValueError(f"Failed to fetch metadata. Error: {e}")

    def health_check(self):
        """Check if the agent can fetch a test URL."""
        try:
            logger.info("Performing health check...")
            test_url = "https://example.com"
            response = requests.get(test_url, timeout=5)
            if response.status_code == 200:
                logger.info("Health check passed.")
                return {"status": "healthy", "message": "Service is operational"}
            else:
                logger.error(f"Health check failed: Unexpected response {response.status_code}.")
                return {"status": "unhealthy", "message": f"Unexpected response: {response.status_code}"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": f"Health check failed with error: {str(e)}"}

    def _get_meta_data(self, soup, meta_name):
        """Helper function to extract metadata from HTML content."""
        if meta_name == "title" and soup.title:
            return soup.title.string.strip()
        elif meta_name == "description" or meta_name == "keywords":
            meta_tag = soup.find("meta", attrs={"name": meta_name})
            if meta_tag and "content" in meta_tag.attrs:
                return meta_tag["content"].strip()
        return f"No {meta_name} found"
