import pytest
from unittest.mock import MagicMock, patch
from core.base import AgentBase
import http.client
import json
from agents.twitter_trend_tracker import TwitterHashtagAgent

class MockResponse:
    """Mock class for http.client.HTTPResponse."""
    def __init__(self, status=200, data=None):
        self.status = status
        self._data = json.dumps(data or {}).encode('utf-8')
    
    def read(self):
        return self._data

class MockConnection:
    """Mock class for http.client.HTTPSConnection."""
    def __init__(self, response):
        self.response = response
        self.requests = []
    
    def request(self, method, url, body, headers):
        self.requests.append({
            'method': method,
            'url': url,
            'body': body,
            'headers': headers
        })
    
    def getresponse(self):
        return self.response
    
    def close(self):
        pass

@pytest.fixture
def mock_tweet_data():
    """Fixture providing sample tweet data."""
    return {
        "results": [{
            "tweet_id": "123456",
            "creation_date": "2024-01-01T12:00:00Z",
            "text": "Test tweet #test",
            "media_url": ["http://example.com/image.jpg"],
            "video_url": [{
                "content_type": "video/mp4",
                "bitrate": "2000",
                "url": "http://example.com/video.mp4"
            }],
            "user": {
                "username": "testuser",
                "name": "Test User",
                "follower_count": 1000,
                "following_count": 500,
                "location": "Test City",
                "description": "Test bio",
                "profile_pic_url": "http://example.com/profile.jpg"
            },
            "favorite_count": 100,
            "retweet_count": 50,
            "reply_count": 25,
            "view_count": 1000
        }]
    }

@pytest.fixture
def twitter_agent(monkeypatch):
    """Fixture to initialize TwitterHashtagAgent with mocked connection."""
    agent = TwitterHashtagAgent(api_key="test_api_key")
    
    original_execute = agent.execute
    def mock_execute(**kwargs):
        hashtag = kwargs.get("hashtag")
        api_key = kwargs.get("api_key", agent.rapid_api_key)
        
        if not hashtag:
            raise ValueError("Hashtag parameter is required")
        if not api_key:
            raise ValueError("API key must be provided either during initialization or execution")
            
        return original_execute(**kwargs)
        
    monkeypatch.setattr(agent, 'execute', mock_execute)
    return agent

def test_init_with_api_key():
    """Test initialization with API key."""
    agent = TwitterHashtagAgent(api_key="test_api_key")
    assert agent.rapid_api_key == "test_api_key"
    assert agent.rapid_api_host == "twitter154.p.rapidapi.com"

def test_format_tweet(twitter_agent, mock_tweet_data):
    """Test tweet formatting."""
    formatted = twitter_agent.format_tweet(mock_tweet_data["results"][0])
    
    assert "Tweet ID: 123456" in formatted
    assert "Test tweet #test" in formatted
    assert "Media 1: ![Image](http://example.com/image.jpg)" in formatted
    assert "Quality 2000 kbps" in formatted
    assert "Username: testuser" in formatted
    assert "Favorites: 100" in formatted

def test_execute_success(twitter_agent, mock_tweet_data):
    """Test successful tweet fetching."""
    mock_response = MockResponse(200, mock_tweet_data)
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = twitter_agent.execute(
            hashtag="test",
            api_key="test_api_key"
        )
    
    assert "Tweet ID: 123456" in result
    assert "Test tweet #test" in result
    assert mock_conn.requests[0]['method'] == "POST"
    assert mock_conn.requests[0]['url'] == "/hashtag/hashtag"

def test_execute_missing_hashtag(twitter_agent):
    """Test handling of missing hashtag."""
    with pytest.raises(ValueError, match="Hashtag parameter is required"):
        twitter_agent.execute(api_key="test_api_key")

def test_execute_missing_api_key(monkeypatch):
    """Test handling of missing API key."""
    agent = TwitterHashtagAgent()
    
    def mock_execute(**kwargs):
        api_key = kwargs.get("api_key", agent.rapid_api_key)
        if not api_key:
            raise ValueError("API key must be provided either during initialization or execution")
        return {}
        
    monkeypatch.setattr(agent, 'execute', mock_execute)
    
    with pytest.raises(ValueError, match="API key must be provided"):
        agent.execute(hashtag="test")

def test_execute_api_error(twitter_agent):
    """Test handling of API error response."""
    mock_response = MockResponse(400, {"error": "Bad Request"})
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = twitter_agent.execute(
            hashtag="test",
            api_key="test_api_key"
        )
    
    assert isinstance(result, dict)
    assert result["status"] == "failed"
    assert "error" in result

def test_execute_with_custom_parameters(twitter_agent, mock_tweet_data):
    """Test execution with custom parameters."""
    mock_response = MockResponse(200, mock_tweet_data)
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        twitter_agent.execute(
            hashtag="test",
            api_key="test_api_key",
            limit=10,
            section="latest",
            language="fr"
        )
    
    request_body = json.loads(mock_conn.requests[0]['body'])
    assert request_body["limit"] == 10
    assert request_body["section"] == "latest"
    assert request_body["language"] == "fr"

def test_health_check_success(twitter_agent, mock_tweet_data):
    """Test health check success status."""
    mock_response = MockResponse(200, mock_tweet_data)
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = twitter_agent.health_check()
    
    assert result["status"] == "healthy"
    assert "Twitter API service is available" in result["message"]

def test_health_check_no_api_key():
    """Test health check without API key."""
    agent = TwitterHashtagAgent()
    result = agent.health_check()
    
    assert result["status"] == "unknown"
    assert "API key not provided" in result["message"]

def test_health_check_failure(twitter_agent):
    """Test health check failure status."""
    mock_response = MockResponse(500, {"error": "Internal Server Error"})
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = twitter_agent.health_check()
    
    assert result["status"] == "unhealthy"
    assert isinstance(result["message"], str)