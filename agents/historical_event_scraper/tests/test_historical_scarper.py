import pytest
from agents.historical_event_scraper import HistoricalEventsAgent


class MockRequests:
    """Mock class for simulating requests.get behavior."""
    @staticmethod
    def get(url):
        if "invalid" in url:
            raise ValueError("Invalid URL")
        elif "/1/1/events.json" in url:
            # Simulate health check response
            return MockResponse({
                "events": [{"year": "2000", "description": "Test Event"}]
            })
        elif "/11/26/events.json" in url:
            # Simulate valid data for today's date
            return MockResponse({
                "events": [
                    {"year": "1922", "description": "Tutankhamun's tomb opened."},
                    {"year": "1942", "description": "Casablanca premiered."}
                ]
            })
        else:
            # Simulate no events for an unexpected endpoint
            return MockResponse({"events": []})


class MockResponse:
    """Mock response object for simulating requests.get responses."""
    def __init__(self, json_data):
        self.json_data = json_data
        self.status_code = 200

    def json(self):
        return self.json_data

    def raise_for_status(self):
        # Simulate HTTP error behavior
        if self.status_code != 200:
            raise ValueError("HTTP error")


@pytest.fixture
def historical_events_agent(monkeypatch):
    """Fixture to initialize the HistoricalEventsAgent with mocked requests."""
    agent = HistoricalEventsAgent()
    # Patch the requests.get function with the mock class
    monkeypatch.setattr("agents.historical_events_agent.requests.get", MockRequests.get)
    return agent


def test_execute_success(historical_events_agent):
    """Test successful execution of the HistoricalEventsAgent."""
    response = historical_events_agent.execute()
    assert len(response) == 2, "Expected 2 events in the response."
    assert response[0]["year"] == "1922", "Expected the first event year to be 1922."
    assert "Tutankhamun" in response[0]["description"], "Expected Tutankhamun in the first event description."


def test_execute_no_events(historical_events_agent, monkeypatch):
    """Test execution when no events are found."""
    def mock_no_events(*args, **kwargs):
        return MockResponse({"events": []})

    monkeypatch.setattr("agents.historical_events_agent.requests.get", mock_no_events)
    response = historical_events_agent.execute()
    assert response == [], "Expected an empty list when no events are available."


def test_execute_invalid_url(historical_events_agent, monkeypatch):
    """Test execution with an invalid URL."""
    def mock_invalid_url(*args, **kwargs):
        raise ValueError("Invalid URL")

    monkeypatch.setattr("agents.historical_events_agent.requests.get", mock_invalid_url)
    with pytest.raises(ValueError, match="Failed to fetch historical events. Please check the API or your connection."):
        historical_events_agent.execute()


def test_health_check_success(historical_events_agent):
    """Test health check success."""
    health = historical_events_agent.health_check()
    assert health["status"] == "healthy", "Expected health status to be 'healthy'."
    assert "Service is available" in health["message"], "Expected success message in health check."


def test_health_check_failure(monkeypatch):
    """Test health check failure."""
    def mock_service_failure(*args, **kwargs):
        raise Exception("Mock service failure")

    monkeypatch.setattr("agents.historical_events_agent.requests.get", mock_service_failure)
    agent = HistoricalEventsAgent()
    health = agent.health_check()
    assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
    assert "Mock service failure" in health["message"], "Expected failure message in health check."
