import requests
from bs4 import BeautifulSoup
import json
from itertools import islice
from core.base import AgentBase
from log import logger


class FlipkartScrapperAgent(AgentBase):
    """Agent to fetch product details from Flipkart."""

    BASE_URL = "https://www.flipkart.com/search?q="

    def execute(self, item_name, max_products=10):
        """
        Fetch product details from Flipkart based on a search term.

        Args:
            item_name (str): The name of the item to search for.
            max_products (int): Maximum number of products to fetch.

        Returns:
            list: A list of dictionaries containing product details.

        Raises:
            ValueError: If the request fails or no product details are found.
        """
        try:
            # Construct search URL
            search_url = f"{self.BASE_URL}{item_name.replace(' ', '+')}"
            logger.debug(f"Constructed Search URL: {search_url}")
            logger.info(f"Fetching product details for: {item_name}")
            logger.debug(f"Search URL: {search_url}")

            # Make the request
            response = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                error_message = "Failed to fetch product details. Please check the inputs and try again."
                logger.error(error_message)
                raise ValueError(error_message)

            soup = BeautifulSoup(response.text, 'html.parser')
            product_cards = soup.find_all('div', {'class': '_1AtVbE'})  # Update if necessary
            logger.info(f"Found {len(product_cards)} product cards.")

            products = []
            for card in islice(product_cards, max_products):
                # Extract product details
                product_name = card.find('div', {'class': '_4rR01T'}) or card.find('a', {'class': 'IRpwTa'})
                price = card.find('div', {'class': '_30jeq3'})
                rating = card.find('div', {'class': '_3LWZlK'})
                offers = card.find('div', {'class': '_3Ay6Sb'})
                delivery = card.find('div', {'class': '_3XINqE'})

                # Skip if essential data is missing
                if not product_name or not price:
                    continue

                product_details = {
                    "product_name": product_name.text.strip(),
                    "category": "N/A",  # Flipkart does not directly show category in search results
                    "sub_category": "N/A",  # Can add subcategory parsing if needed
                    "price": price.text.strip(),
                    "offers": offers.text.strip() if offers else "No offers",
                    "delivery_charge": delivery.text.strip() if delivery else "Free delivery",
                    "rating": rating.text.strip() if rating else "No rating",
                    "customers_bought": "N/A",  # Flipkart does not provide this directly in search results
                }
                products.append(product_details)

            if not products:
                error_message = "No products found for the given search query."
                logger.error(error_message)
                raise ValueError(error_message)

            # Return as JSON
            logger.info(f"Successfully fetched {len(products)} products.")
            return json.dumps(products, indent=4)

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise e

    def health_check(self):
        """
        Check if the Flipkart scraper is functional.

        Returns:
            dict: Health status of the scraper.
        """
        try:
            logger.info("Performing health check...")
            test_search = "iphone"
            result = self.execute(test_search, max_products=1)
            if result:
                logger.info("Health check passed.")
                return {"status": "healthy", "message": "Scraper is functional"}
            else:
                raise Exception("Health check failed: No results.")
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
