import pytest
import requests
from agents.cghs_hospitals import CGHSHospitalsAgent
import re


@pytest.fixture
def agent():
    return CGHSHospitalsAgent()


def test_execute_success(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {
                    "records": [
                        {
                            "hospitalName": "Test Hospital",
                            "address": "123 Test St",
                            "city": "Delhi"
                        }
                    ]
                }
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    response = agent.execute(api_key="test_api_key", city_name="Delhi")
    assert response["status"] == "success"
    assert isinstance(response["data"], list)
    assert response["data"][0]["hospitalName"] == "Test Hospital"


def test_execute_missing_api_key(agent):
    with pytest.raises(ValueError, match=r"(?i).*api[_-]?key.*"):
        agent.execute(api_key=None)



def test_execute_invalid_api_key(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        class MockResponse:
            status_code = 401
            text = "Unauthorized"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError, match="Invalid API key"):
        agent.execute(api_key="invalid_key")

def test_execute_bad_request(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        class MockResponse:
            status_code = 400
            text = "Bad Request"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError, match=r"Bad request: Invalid parameters or URL\."):
        agent.execute(api_key="test_api_key", city_name="InvalidCity")


def test_execute_unexpected_error(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        class MockResponse:
            status_code = 500
            text = "Internal Server Error"
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    with pytest.raises(ValueError) as exc_info:
        agent.execute(api_key="test_api_key")

    # Print the actual exception message for debugging
    print(f"Actual exception message: {str(exc_info.value)}")

    # Assert that the exception message contains the expected substring
    assert "API Error: 500 - Internal Server Error" in str(exc_info.value)
    
def test_health_check_success(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        class MockResponse:
            status_code = 200
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    health = agent.health_check()
    assert health["status"] == "healthy"
    assert "API is reachable" in health["message"]


def test_health_check_unauthorized(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        class MockResponse:
            status_code = 401
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = agent.health_check()
    assert result["status"] == "healthy"
    assert "unauthorized" in result["message"].lower()


def test_health_check_unexpected_status(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        class MockResponse:
            status_code = 503
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    health = agent.health_check()
    assert health["status"] == "unhealthy"
    assert "Unexpected status" in health["message"]


def test_health_check_failure(monkeypatch, agent):
    def mock_get(url, params=None, **kwargs):
        raise Exception("Network failure")

    monkeypatch.setattr(requests, "get", mock_get)

    health = agent.health_check()
    assert health["status"] == "unhealthy"
    assert "Network failure" in health["message"]
