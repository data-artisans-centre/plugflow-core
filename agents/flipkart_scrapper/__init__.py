import json
import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, HttpUrl, ValidationError
from typing import List, Optional
from itertools import islice
from core.base import AgentBase
from log import logger


class Product(BaseModel):
    """Pydantic model for a Flipkart product."""
    product_name: str
    category: str = "N/A"
    sub_category: str = "N/A"
    price: str
    offers: str = "No offers"
    delivery_charge: str = "Free delivery"
    rating: Optional[str] = "No rating"
    customers_bought: str = "N/A"


class FlipkartScrapperAgent(AgentBase):
    """Agent to fetch product details from Flipkart."""
    BASE_URL: HttpUrl = "https://www.flipkart.com/search?q="

    def execute(self, item_name: str, max_products: int = 10) -> str:
        """
        Fetch product details from Flipkart based on a search term.

        Args:
            item_name (str): The name of the item to search for.
            max_products (int): Maximum number of products to fetch.

        Returns:
            str: JSON string containing product details.

        Raises:
            ValueError: If the request fails or no product details are found.
        """
        search_url = f"{self.BASE_URL}{item_name.replace(' ', '+')}"
        logger.debug(f"Constructed Search URL: {search_url}")

        try:
            response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Failed to fetch product details. Please check the URL or network.")
            raise ValueError("Failed to fetch product details. Please check the URL or network.") from e

        soup = BeautifulSoup(response.text, 'html.parser')
        product_cards = soup.find_all('div', {'class': '_1AtVbE'})

        products = []
        for card in islice(product_cards, max_products):
            try:
                product = Product(
                    product_name=(card.find('div', {'class': '_4rR01T'}) or 
                                  card.find('a', {'class': 'IRpwTa'})).text.strip(),
                    price=card.find('div', {'class': '_30jeq3'}).text.strip(),
                    offers=card.find('div', {'class': '_3Ay6Sb'}).text.strip() if card.find('div', {'class': '_3Ay6Sb'}) else "No offers",
                    delivery_charge=card.find('div', {'class': '_3XINqE'}).text.strip() if card.find('div', {'class': '_3XINqE'}) else "Free delivery",
                    rating=card.find('div', {'class': '_3LWZlK'}).text.strip() if card.find('div', {'class': '_3LWZlK'}) else None
                )
                products.append(product.model_dump())
            except AttributeError:
                continue  # Skip cards with missing essential data

        if not products:
            logger.error("No products found for the given search query.")
            raise ValueError("No products found for the given search query.")

        logger.info(f"Successfully fetched {len(products)} products.")
        return json.dumps(products, indent=4)

    def health_check(self) -> dict:
        """
        Check if the Flipkart scraper is functional.

        Returns:
            dict: Health status of the scraper.
        """
        logger.info("Performing health check...")
        try:
            test_result = self.execute("iphone", max_products=1)
            return {"status": "healthy", "message": "Scraper is functional"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
