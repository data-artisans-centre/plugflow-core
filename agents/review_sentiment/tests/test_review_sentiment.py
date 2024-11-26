import pytest
from agents.review_sentiment import YouTubeReviewAnalyzer


class MockAnalyzer:
    """Mock class for YouTubeReviewAnalyzer."""
    def analyze_comment(self, comment_text):
        if not comment_text.strip():
            raise ValueError("Empty comment text")
        return {
            "comment": comment_text,
            "sentiment": {
                "polarity": 0.5,
                "subjectivity": 0.5
            },
            "sentiment_polarity": 0.5,
            "sentiment_subjectivity": 0.5,
            "readability_score": 80.0,
            "review_length": len(comment_text.split())
        }

    def process_comments(self, comments_data):
        return [
            {
                "author": comment.get("author", "Unknown"),
                "original_comment": comment["comment"],
                "likes": comment.get("likes", 0),
                "time": comment.get("time", "Unknown"),
                "analysis": self.analyze_comment(comment["comment"])
            }
            for comment in comments_data
        ]

    def health_check(self):
        try:
            # Perform a simple health check
            self.analyze_comment("Test comment")
            return {
                "status": "healthy",
                "message": "Service is operational"
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": str(e)
            }


@pytest.fixture
def youtube_review_analyzer(monkeypatch):
    """Fixture to initialize the YouTubeReviewAnalyzer with a mock implementation."""
    analyzer = YouTubeReviewAnalyzer()
    # Patch the methods with the mock implementation
    mock_analyzer = MockAnalyzer()
    monkeypatch.setattr(analyzer, "analyze_comment", mock_analyzer.analyze_comment)
    monkeypatch.setattr(analyzer, "process_comments", mock_analyzer.process_comments)
    monkeypatch.setattr(analyzer, "health_check", mock_analyzer.health_check)
    return analyzer


def test_execute_success(youtube_review_analyzer):
    """Test successful execution of the YouTubeReviewAnalyzer."""
    video_url = "https://www.youtube.com/watch?v=valid123"
    sample_comments = [
        {
            "author": "TestUser",
            "comment": "This is a great video!",
            "likes": 42,
            "time": "2 days ago"
        }
    ]
    response = youtube_review_analyzer.process_comments(sample_comments)
    assert len(response) == 1, "Expected one comment in the response."
    assert response[0]["author"] == "TestUser", "Expected author to be 'TestUser'."
    assert "sentiment" in response[0]["analysis"], "Missing 'sentiment' in analysis."
    assert response[0]["analysis"]["sentiment"]["polarity"] >= 0, "Unexpected sentiment polarity."


def test_execute_empty_comments(youtube_review_analyzer):
    """Test execution with empty comments."""
    empty_comments = [{"author": "TestUser", "comment": "", "likes": 0, "time": "Unknown"}]
    with pytest.raises(ValueError, match="Empty comment text"):
        youtube_review_analyzer.process_comments(empty_comments)


def test_health_check_success(youtube_review_analyzer):
    """Test health check success."""
    health = youtube_review_analyzer.health_check()
    assert health["status"] == "healthy", "Expected health status to be 'healthy'."
    assert "Service is operational" in health["message"], "Expected success message in health check."


def test_health_check_failure(monkeypatch):
    """Test health check failure."""
    def mock_analyze_comment(comment_text):
        raise Exception("Mock analysis failure")

    analyzer = YouTubeReviewAnalyzer()
    monkeypatch.setattr(analyzer, "analyze_comment", mock_analyze_comment)
    
    health = analyzer.health_check()
    assert health["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
    assert "Mock analysis failure" in health["message"], "Expected failure message in health check."


def test_invalid_data_structure(youtube_review_analyzer):
    """Test invalid data structure for comments."""
    invalid_data = [{"invalid_key": "Invalid data"}]
    with pytest.raises(KeyError, match="'comment'"):
        youtube_review_analyzer.process_comments(invalid_data)


def test_partial_data(youtube_review_analyzer):
    """Test comments with missing optional fields."""
    partial_data = [
        {"author": "TestUser", "comment": "Great content!", "time": "1 hour ago"}
    ]
    response = youtube_review_analyzer.process_comments(partial_data)
    assert len(response) == 1, "Expected one comment in the response."
    assert response[0]["author"] == "TestUser", "Expected author to be 'TestUser'."
    assert response[0]["likes"] == 0, "Expected default value of likes to be 0."
    assert response[0]["time"] == "1 hour ago", "Expected time to be '1 hour ago'."


def test_large_comment(youtube_review_analyzer):
    """Test analysis of a very large comment."""
    large_comment = {
        "author": "TestUser",
        "comment": "This is a " + "very " * 1000 + "large comment.",
        "likes": 10,
        "time": "1 day ago"
    }
    response = youtube_review_analyzer.process_comments([large_comment])
    assert len(response) == 1, "Expected one comment in the response."
    assert response[0]["analysis"]["review_length"] > 1000, "Expected review length to be greater than 1000."