import pytest
from agents.valid_email import EmailValidationAgent
import requests
from unittest.mock import MagicMock


@pytest.fixture
def email_agent():
    """Fixture to initialize the EmailValidationAgent."""
    return EmailValidationAgent()


def test_execute_valid_email(monkeypatch, email_agent):
    """Test valid email with proper API response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "is_valid": True,
        "email": "info@example.com",
        "domain": "example.com",
        "local_part": "info"
    }

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: mock_response)

    result = email_agent.execute("info@example.com", "fake_api_key")
    assert result["status"] == "success"
    assert result["data"]["is_valid"] is True


def test_execute_invalid_email(monkeypatch, email_agent):
    """Test invalid email format."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "is_valid": False,
        "email": "45645y.in"
    }

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: mock_response)

    result = email_agent.execute("45645y.in", "fake_api_key")
    assert result["status"] == "success"
    assert result["data"]["is_valid"] is False


def test_execute_missing_api_key(email_agent):
    """Test when API key is missing."""
    with pytest.raises(ValueError, match="Missing API Key"):
        email_agent.execute("info@example.com", "")


def test_execute_missing_email(email_agent):
    """Test when email is missing."""
    with pytest.raises(ValueError, match="Missing email parameter"):
        email_agent.execute("", "some_api_key")


def test_execute_invalid_api_key(monkeypatch, email_agent):
    """Test when API key is invalid (401 Unauthorized)."""
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: mock_response)

    with pytest.raises(ValueError, match="Unauthorized: Invalid API key."):
        email_agent.execute("info@example.com", "invalid_key")


def test_health_check_success(monkeypatch, email_agent):
    """Test health check returns healthy if API is reachable."""
    mock_response = MagicMock()
    mock_response.status_code = 401  # Still considered reachable

    monkeypatch.setattr(requests, "get", lambda *args, **kwargs: mock_response)

    result = email_agent.health_check()
    assert result["status"] == "healthy"
    assert "API reachable" in result["message"]


def test_health_check_failure(monkeypatch, email_agent):
    """Test health check returns unhealthy on exception."""
    def raise_error(*args, **kwargs):
        raise Exception("Service unavailable")

    monkeypatch.setattr(requests, "get", raise_error)

    result = email_agent.health_check()
    assert result["status"] == "unhealthy"
    assert "Service unavailable" in result["message"]

