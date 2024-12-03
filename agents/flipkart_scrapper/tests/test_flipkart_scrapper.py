import pytest # type: ignore
import json
from agents.flipkart_scrapper import FlipkartScrapperAgent
from unittest.mock import Mock
import requests


class MockResponse:
    """Mock class to simulate requests.Response."""
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.RequestException(f"HTTP {self.status_code}")
        

class MockRequests:
    """Mock class to simulate requests.get."""
    RequestException = requests.exceptions.RequestException  # Link to real RequestException

    def __init__(self, mock_data):
        self.mock_data = mock_data

    def get(self, url, headers=None):
        if "iphone" in url:
            return MockResponse(self.mock_data["valid"])
        elif "empty" in url:
            return MockResponse("", 200)
        return MockResponse("Error", 404)
    
    
@pytest.fixture
def flipkart_scrapper_agent(monkeypatch):
    """Fixture to initialize the FlipkartScrapperAgent with mock requests."""
    agent = FlipkartScrapperAgent()

    # Mock data simulating Flipkart's HTML structure
    mock_data = {
        "valid": """
            <html>
                <div class="_1AtVbE">
                    <div class="_4rR01T">APPLE iPhone 15 (Blue, 128 GB)</div>
                    <div class="_30jeq3">₹79,900</div>
                    <div class="_3LWZlK">4.5</div>
                    <div class="_3Ay6Sb">10% off</div>
                    <div class="_3XINqE">Free delivery</div>
                </div>
                <div class="_1AtVbE">
                    <div class="_4rR01T">APPLE iPhone 15 Pro (Black, 256 GB)</div>
                    <div class="_30jeq3">₹1,39,900</div>
                    <div class="_3LWZlK">4.8</div>
                    <div class="_3Ay6Sb">5% Cashback</div>
                    <div class="_3XINqE">Free delivery</div>
                </div>
            </html>
        """,
    }

    # Patch the requests module with mock data
    monkeypatch.setattr("agents.flipkart_scrapper.requests", MockRequests(mock_data))
    return agent


def test_execute_success(flipkart_scrapper_agent):
    """Test successful execution of the FlipkartScrapperAgent."""
    item_name = "iphone"
    max_products = 2
    response = flipkart_scrapper_agent.execute(item_name=item_name, max_products=max_products)
    response_json = json.loads(response)

    # Validate the response contains the expected number of products
    assert len(response_json) == max_products, f"Expected {max_products} products in the response."

    # Validate specific fields in the first product
    first_product = response_json[0]
    assert first_product["product_name"] == "APPLE iPhone 15 (Blue, 128 GB)"
    assert first_product["price"] == "₹79,900"
    assert first_product["rating"] == "4.5"
    assert first_product["offers"] == "10% off"
    assert first_product["delivery_charge"] == "Free delivery"
    
    
def test_execute_empty_response(flipkart_scrapper_agent, monkeypatch):
    """Test execution with a search query that yields no results."""
    def mock_get_empty(*args, **kwargs):

        # Simulate an empty HTML response
        return MockResponse("", 200)  # Simulate an empty HTML response

    monkeypatch.setattr("agents.flipkart_scrapper.requests.get", mock_get_empty)
    
    item_name = "empty"
    max_products = 2

    with pytest.raises(ValueError, match="No products found for the given search query."):
        flipkart_scrapper_agent.execute(item_name=item_name, max_products=max_products)

    
    
def test_execute_invalid_url(flipkart_scrapper_agent, monkeypatch):
    """Test execution with a non-Flipkart URL."""
    def mock_get_invalid(*args, **kwargs):
        # Simulate an invalid response with 404 status code
        return MockResponse("Error", 404)
    
    monkeypatch.setattr("agents.flipkart_scrapper.requests.get", mock_get_invalid)

    item_name = "invalid_item"
    max_products = 1

    # Used pytest.raises to validate exception and message
    with pytest.raises(ValueError, match=r"Failed to fetch product details\. Please check the URL or network\."):
        flipkart_scrapper_agent.execute(item_name=item_name, max_products=max_products)


def test_health_check_success(flipkart_scrapper_agent):
    """Test health check success."""
    health = flipkart_scrapper_agent.health_check()
    assert health["status"] == "healthy", "Expected health status to be 'healthy'."
    assert "Scraper is functional" in health["message"], "Expected success message in health check."


def test_health_check_failure(monkeypatch):
    """Test health check failure when scraping fails."""
    def mock_execute_failure(*args, **kwargs):
        raise ValueError("Mock scraping failure")
    monkeypatch.setattr("agents.flipkart_scrapper.FlipkartScrapperAgent.execute", mock_execute_failure)
    agent = FlipkartScrapperAgent()
    health = agent.health_check()
    assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
    assert "Mock scraping failure" in health["message"], "Expected failure message in health check."

