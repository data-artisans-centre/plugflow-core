import pytest
from unittest.mock import patch
from core.base import AgentBase
import json
from agents.crickAlert import CrickAlertAgent

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
    
    def request(self, method, url, headers):
        self.requests.append({
            'method': method,
            'url': url,
            'headers': headers
        })
    
    def getresponse(self):
        return self.response
    
    def close(self):
        pass

@pytest.fixture
def mock_cricket_data():
    """Fixture providing sample cricket match data."""
    return {
        "typeMatches": [
            {
                "seriesMatches": [
                    {
                        "seriesAdWrapper": {
                            "matches": [
                                {
                                    "matchInfo": {
                                        "matchId": "1234",
                                        "seriesName": "IPL 2024",
                                        "matchDesc": "Match 1",
                                        "matchFormat": "T20",
                                        "team1": {
                                            "teamId": "1",
                                            "teamName": "Mumbai Indians"
                                        },
                                        "team2": {
                                            "teamId": "2",
                                            "teamName": "Chennai Super Kings"
                                        },
                                        "venueInfo": {
                                            "ground": "Wankhede Stadium",
                                            "city": "Mumbai"
                                        }
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        ]
    }

@pytest.fixture
def cricket_agent():
    """Fixture to initialize CrickAlertAgent."""
    return CrickAlertAgent(api_key="test_api_key")

def test_init_with_api_key():
    """Test initialization with API key."""
    agent = CrickAlertAgent(api_key="test_api_key")
    assert agent.rapid_api_key == "test_api_key"
    assert agent.rapid_api_host == "cricbuzz-cricket.p.rapidapi.com"

def test_execute_success(cricket_agent, mock_cricket_data):
    """Test successful match fetching."""
    mock_response = MockResponse(200, mock_cricket_data)
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = cricket_agent.execute(api_key="test_api_key")
    
    assert result["status"] == "success"
    assert len(result["matches"]) == 1
    assert result["count"] == 1
    assert mock_conn.requests[0]['method'] == "GET"
    assert mock_conn.requests[0]['url'] == "/matches/v1/recent"

def test_execute_with_search_term(cricket_agent, mock_cricket_data):
    """Test match fetching with search term."""
    mock_response = MockResponse(200, mock_cricket_data)
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = cricket_agent.execute(
            api_key="test_api_key",
            search_term="mumbai"
        )
    
    assert result["status"] == "success"
    assert len(result["matches"]) == 1
    assert result["search_term"] == "mumbai"

def test_execute_no_matches_found(cricket_agent):
    """Test handling when no matches found."""
    mock_data = {"typeMatches": []}
    mock_response = MockResponse(200, mock_data)
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = cricket_agent.execute(api_key="test_api_key")
    
    assert result["status"] == "success"
    assert len(result["matches"]) == 0
    assert result["count"] == 0

def test_execute_missing_api_key(cricket_agent):
    """Test handling of missing API key."""
    cricket_agent.rapid_api_key = None
    result = cricket_agent.execute()
    
    assert result["status"] == "failed"
    assert "API key must be provided" in result["error"]

def test_execute_api_error(cricket_agent):
    """Test handling of API error response."""
    mock_response = MockResponse(400, {"error": "Bad Request"})
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = cricket_agent.execute(api_key="test_api_key")
    
    assert isinstance(result, dict)
    assert result["status"] == "failed"
    assert "error" in result

def test_search_term_matching(cricket_agent, mock_cricket_data):
    """Test different search term matching scenarios."""
    mock_response = MockResponse(200, mock_cricket_data)
    mock_conn = MockConnection(mock_response)
    
    test_cases = [
        ("ipl", 1),  # Matches series name
        ("mumbai", 1),  # Matches city and team name
        ("chennai", 1),  # Matches team name
        ("wankhede", 1),  # Matches ground
        ("t20", 1),  # Matches format
        ("test", 0),  # No matches
    ]
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        for search_term, expected_count in test_cases:
            result = cricket_agent.execute(
                api_key="test_api_key",
                search_term=search_term
            )
            assert result["count"] == expected_count, f"Failed for search term: {search_term}"

def test_health_check_success(cricket_agent, mock_cricket_data):
    """Test health check success status."""
    mock_response = MockResponse(200, mock_cricket_data)
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = cricket_agent.health_check()
    
    assert result["status"] == "healthy"
    assert "Cricbuzz API service is available" in result["message"]

def test_health_check_no_api_key():
    """Test health check without API key."""
    agent = CrickAlertAgent()
    result = agent.health_check()
    
    assert result["status"] == "unknown"
    assert "API key not provided" in result["message"]

def test_health_check_failure(cricket_agent):
    """Test health check failure status."""
    mock_response = MockResponse(500, {"error": "Internal Server Error"})
    mock_conn = MockConnection(mock_response)
    
    with patch('http.client.HTTPSConnection', return_value=mock_conn):
        result = cricket_agent.health_check()
    
    assert result["status"] == "unhealthy"
    assert isinstance(result["message"], str)