import pytest
from agents.youtube_review import YoutubeReviewAgent


class MockDownloader:
    """Mock class for YoutubeCommentDownloader."""
    def get_comments_from_url(self, url, sort_by=None):
        if "invalid" in url:
            raise ValueError("Invalid URL")
        # Return a generator simulating a valid response
        yield {"author": "TestUser", "comment": "This is a test comment"}


@pytest.fixture
def youtube_review_agent(monkeypatch):
    """Fixture to initialize the YoutubeReviewAgent with a mock downloader."""
    agent = YoutubeReviewAgent()
    # Patch the YoutubeCommentDownloader with the mock class
    monkeypatch.setattr("agents.youtube_review.YoutubeCommentDownloader", MockDownloader)
    return agent


def test_execute_success(youtube_review_agent):
    """Test successful execution of the YoutubeReviewAgent."""
    video_url = "https://www.youtube.com/watch?v=valid123"
    response = youtube_review_agent.execute(video_url, max_comments=1)
    # Check if 'TestUser' exists in the 'author' field of any comment
    assert any(comment.get("author") == "TestUser" for comment in response), "Expected 'TestUser' in comments."


def test_execute_invalid_url(youtube_review_agent):
    """Test execution with an invalid URL."""
    video_url = "https://www.youtube.com/watch?v=invalid123"
    with pytest.raises(ValueError, match="Failed to fetch comments. Please check the video URL and try again."):
        youtube_review_agent.execute(video_url, max_comments=1)


def test_health_check_success(youtube_review_agent):
    """Test health check success."""
    health = youtube_review_agent.health_check()
    assert health["status"] == "healthy", "Expected health status to be 'healthy'."
    assert "Service is available" in health["message"], "Expected success message in health check."


def test_health_check_failure(monkeypatch):
    """Test health check failure."""
    def mock_get_comments_from_url(*args, **kwargs):
        raise Exception("Mock service failure")

    # Patch the `get_comments_from_url` method to simulate a failure
    monkeypatch.setattr("agents.youtube_review.YoutubeCommentDownloader.get_comments_from_url", mock_get_comments_from_url)

    agent = YoutubeReviewAgent()
    health = agent.health_check()
    assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
    assert "Mock service failure" in health["message"], "Expected failure message in health check."

