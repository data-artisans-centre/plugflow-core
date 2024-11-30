import pytest
from agents.github_activities import GitHubActivitiesAgent
import requests
import json
class MockGitHubAPI:
    """Mock class for GitHub API responses. """
    def get_events_from_repo(self, repo_url):
        if "invalid-repo" in repo_url:
            raise ValueError("Invalid repository URL")
        # Return a generator simulating a valid response
        yield {"type": "PushEvent", "actor": {"login":"MockUser"}}


@pytest.fixture
def github_activities_agent(monkeypatch):
    """Fixture to initialize the GitHubActivitiesAgent with a mock API."""
    agent = GitHubActivitiesAgent()
    # Patch the GitHub API with the mock class
    def mock_get(url, headers=None):
        if "invalid-repo" in url:
            mock_response = requests.Response()
            mock_response.status_code = 404
            mock_response.reason = "Not Found"
            raise requests.exceptions.HTTPError(response=mock_response)
        mock_response = requests.Response()
        mock_response.status_code = 200
        mock_response._content = b'[{"type": "PushEvent", "actor": {"login": "MockUser"}}]'
        return mock_response
       
    monkeypatch.setattr("requests.get", mock_get)
    return agent


def test_execute_success(github_activities_agent):
    """Test successful execution of the GitHubActivitiesAgent"""
    repo_url = "https://github.com/test-user/test-repo"
    response = github_activities_agent.execute(repo_url, max_events=1)
    events = json.loads(response)
    assert len(events) == 1, "Expected one event in the response."
    assert events[0]["type"] == "PushEvent", "Expected event type 'PushEvent'."
    assert events[0]["actor"]["login"] == "MockUser", "Expected actor login 'MockUser'."    


def test_execute_invalid_url(github_activities_agent):
    """Test execution with an invalid repo."""
    repo_url = "https://github.com/test-user/invalid-repo"
    with pytest.raises(ValueError, match="Failed to fetch events. Please check the repository URL and try again."):
        github_activities_agent.execute(repo_url, max_events=1)


def test_health_check_success(github_activities_agent):
    """Test health check success."""
    health = github_activities_agent.health_check()
    assert health["status"] == "healthy", "Expected health status to be 'healthy'."
    assert "Service is available" in health["message"], "Expected success message in health check."


def test_health_check_failure(monkeypatch):
    """Test health check failure."""
    def mock_get(*args, **kwargs):
        raise Exception("Mock service failure")

    # Patch the `requests.get` method to simulate a failure
    monkeypatch.setattr("requests.get", mock_get)

    agent = GitHubActivitiesAgent()
    health = agent.health_check()
    assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
    assert "Mock service failure" in health["message"], "Expected failure message in health check."

