import pytest
from agents.website_metadata_extractor import WebsiteMetadataAgent
import requests

class MockRequests:
    """Mock class for requests.get."""
    @staticmethod
    def get(url, timeout=10):
        if "invalid" in url:
            raise ValueError("Invalid URL")
        elif "error" in url:
            # Simulate network error
            raise Exception("Simulated network error")

        class MockResponse:
            status_code = 200

            @staticmethod
            def raise_for_status():
                pass

            @property
            def content(self):
                # Simulate a simple HTML response for testing
                return """
                    <html>
                        <head>
                            <title>Test Title</title>
                            <meta name="description" content="This is a test description">
                            <meta name="keywords" content="test, metadata, extractor">
                        </head>
                        <body>
                            <h1>Header 1</h1>
                            <h2>Header 2</h2>
                        </body>
                    </html>
                """
        return MockResponse()


@pytest.fixture
def website_metadata_agent(monkeypatch):
    """Fixture to initialize the WebsiteMetadataAgent with a mock requests.get."""
    agent = WebsiteMetadataAgent()
    # Patch the requests.get method with the mock class
    monkeypatch.setattr("requests.get", MockRequests.get)
    return agent


def test_execute_success(website_metadata_agent):
    """Test successful execution of the WebsiteMetadataAgent."""
    url = "https://valid-url.com"
    metadata = website_metadata_agent.execute(url)

    # Assertions for metadata fields
    assert metadata["Title"] == "Test Title", "Expected title to be 'Test Title'."
    assert metadata["Meta Description"] == "This is a test description", "Expected meta description to match."
    assert metadata["Meta Keywords"] == "test, metadata, extractor", "Expected meta keywords to match."


def test_execute_invalid_url(website_metadata_agent):
    """Test execution with an invalid URL."""
    url = "https://invalid-url.com"
    with pytest.raises(ValueError) as excinfo:
        website_metadata_agent.execute(url)

    assert "Invalid URL" in str(excinfo.value)


def test_execute_network_error(website_metadata_agent):
    """Test execution with a simulated network error."""
    url = "https://error-url.com"
    with pytest.raises(Exception, match="Simulated network error"):
        website_metadata_agent.execute(url)


def test_health_check_success(website_metadata_agent):
    """Test health check success."""
    health = website_metadata_agent.health_check()
    assert health["status"] == "healthy", "Expected health status to be 'healthy'."
    assert "Service is operational" in health["message"], "Expected success message in health check."


def test_health_check_failure(monkeypatch, website_metadata_agent):
    """Test health check failure by mocking requests.get to raise an exception."""

    # Define the mock method to simulate a failure in health check
    def mock_get(*args, **kwargs):
        # Raising the correct exception (generic exception)
        raise requests.exceptions.RequestException("Mock health check failure")

    # Patch the requests.get method to simulate a failure during the health check
    monkeypatch.setattr("requests.get", mock_get)

    # Run the health check and assert the error
    health = website_metadata_agent.health_check()

    # Validate the output after the simulated failure
    assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
    assert "Mock health check failure" in health["message"], "Expected failure message in health check."
