import pytest
import json
from unittest.mock import patch, MagicMock
from agents.amazon_product import AmazonProductAgent

class MockResponse:
    def __init__(self, status, data):
        self.status = status
        self._data = data
        
    def read(self):
        return self._data

@pytest.fixture
def successful_response():
    return MockResponse(200, json.dumps({
        "query": "Phone",
        "results": [{"title": "Example Phone", "asin": "B0AXXXXX", "price": {"raw": "$299.99"}}]
    }).encode('utf-8'))

@pytest.fixture
def error_response():
    return MockResponse(404, json.dumps({"message": "Not found"}).encode('utf-8'))

@pytest.fixture
def agent():
    return AmazonProductAgent(api_key="test_api_key")

# Core functionality tests
@patch('http.client.HTTPSConnection')
def test_basic_search(mock_conn, agent, successful_response):
    mock_instance = MagicMock()
    mock_conn.return_value = mock_instance
    mock_instance.getresponse.return_value = successful_response
    
    result = agent.execute(query="Phone")
    
    assert result["status"] == "success"
    assert "Phone" in str(result["data"])
    mock_instance.request.assert_called_once()

# Parameter tests
@patch('http.client.HTTPSConnection')
def test_search_with_params(mock_conn, agent, successful_response):
    mock_instance = MagicMock()
    mock_conn.return_value = mock_instance
    mock_instance.getresponse.return_value = successful_response
    
    agent.execute(
        query="Laptop", 
        country="UK", 
        is_prime=True,
        page=2
    )
    
    url = mock_instance.request.call_args[0][1]
    assert "query=Laptop" in url
    assert "country=UK" in url
    assert "is_prime=true" in url
    assert "page=2" in url

# Error handling tests
def test_missing_required_params(agent):
    result = agent.execute(query="")
    assert result["status"] == "failed"
    assert "required" in result["error"].lower()

@patch('http.client.HTTPSConnection')
def test_api_error_response(mock_conn, agent, error_response):
    mock_instance = MagicMock()
    mock_conn.return_value = mock_instance
    mock_instance.getresponse.return_value = error_response
    
    result = agent.execute(query="NonExistent")
    
    assert result["status"] == "failed"
    assert "Not found" in result["error"] or "404" in result["error"]

@patch('http.client.HTTPSConnection')
def test_connection_exception(mock_conn, agent):
    mock_instance = MagicMock()
    mock_conn.return_value = mock_instance
    mock_instance.request.side_effect = Exception("Network error")
    
    result = agent.execute(query="Phone")
    
    assert result["status"] == "failed"
    assert "Network error" in result["error"]

# Health check tests
@patch('http.client.HTTPSConnection')
def test_health_check(mock_conn, agent, successful_response):
    mock_instance = MagicMock()
    mock_conn.return_value = mock_instance
    mock_instance.getresponse.return_value = successful_response
    
    result = agent.health_check()
    
    assert result["status"] == "healthy"

def test_health_check_without_api_key():
    agent = AmazonProductAgent()
    result = agent.health_check()
    assert result["status"] == "unhealthy"

@patch('http.client.HTTPSConnection')
def test_malformed_json_response(mock_conn, agent):
    mock_instance = MagicMock()
    mock_conn.return_value = mock_instance
    mock_instance.getresponse.return_value = MockResponse(200, b'Invalid JSON')
    
    result = agent.execute(query="Phone")
    
    assert result["status"] == "failed"
    assert "Expecting value:" in result["error"] or "parse" in result["error"].lower()

@patch('http.client.HTTPSConnection')
def test_unexpected_status_code(mock_conn, agent):
    mock_instance = MagicMock()
    mock_conn.return_value = mock_instance
    mock_instance.getresponse.return_value = MockResponse(418, b'{"message": "I\'m a teapot"}')
    
    result = agent.execute(query="Phone")
    
    assert result["status"] == "failed"
    assert "418" in result["error"] or "teapot" in result["error"]