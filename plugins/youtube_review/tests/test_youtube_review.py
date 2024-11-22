import pytest
from plugins.youtube_review import Plugin


class MockDownloader:
    """Mock class for YoutubeCommentDownloader"""
    def get_comments_from_url(self, url, sort_by=None):
        if "invalid" in url:
            raise ValueError("Invalid URL")
        # Return a generator simulating a valid response
        yield {"author": "TestUser", "comment": "This is a test comment"}

@pytest.fixture
def youtube_review_plugin(monkeypatch):
    """Fixture to initialize the youtube-review plugin with a mock downloader."""
    plugin = Plugin()
    # Patch the YoutubeCommentDownloader with the mock class
    monkeypatch.setattr("plugins.youtube_review.YoutubeCommentDownloader", MockDownloader)
    return plugin

def test_execute_success(youtube_review_plugin):
    """Test successful execution of youtube-review plugin."""
    video_url = "https://www.youtube.com/watch?v=valid123"
    response = youtube_review_plugin.execute(video_url, max_comments=1)
    # Check if 'TestUser' exists in the 'author' field of any comment
    assert any(comment.get("author") == "TestUser" for comment in response)



def test_execute_invalid_url(youtube_review_plugin):
    """Test execution with an invalid URL."""
    video_url = "https://www.youtube.com/watch?v=invalid123"
    with pytest.raises(ValueError, match="Invalid URL"):
        youtube_review_plugin.execute(video_url, max_comments=1)

def test_health_check_success(youtube_review_plugin):
    """Test health check success."""
    health = youtube_review_plugin.health_check()
    assert health["status"] == "healthy"
    assert "Service is available" in health["message"]

def test_health_check_failure(monkeypatch):
    """Test health check failure."""
    def mock_get_comments(*args, **kwargs):
        raise Exception("Mock service failure")

    monkeypatch.setattr("plugins.youtube_review.YoutubeCommentDownloader.get_comments_from_url", mock_get_comments)

    plugin = Plugin()
    health = plugin.health_check()
    assert health["status"] == "unhealthy"
    assert "Mock service failure" in health["message"]

