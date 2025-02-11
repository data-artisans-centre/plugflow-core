import pytest
from unittest import mock
from agents.url2pdf import URLToPDFConverter  # Update with the correct import path
import os

@pytest.fixture
def mock_requests_post():
    with mock.patch("requests.post") as mock_post:
        yield mock_post

@pytest.fixture
def mock_requests_get():
    with mock.patch("requests.get") as mock_get:
        yield mock_get

# Test Case 1: Test for Successful Conversion
def test_execute_success(mock_requests_post, mock_requests_get):
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "Files": [{"FileName": "test_output.pdf", "Url": "http://example.com/test_output.pdf"}],
        "ConversionCost": 5
    }
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.content = b"PDF content"

    converter = URLToPDFConverter()
    url = "http://example.com"
    api_key = "valid_api_key"
    output_dir = "/path/to/output"
    file_name = "test_output"
    
    response = converter.execute(url, api_key, output_dir, file_name)
    
    assert response["status"] == "success"
    assert response["file_name"] == "test_output.pdf"
    assert response["file_url"] == "http://example.com/test_output.pdf"
    assert response["conversion_cost"] == 5

# Test Case 2: Test for Missing URL
def test_execute_missing_url():
    converter = URLToPDFConverter()
    api_key = "valid_api_key"
    
    with pytest.raises(ValueError, match="URL cannot be empty."):
        converter.execute("", api_key)

# Test Case 3: Test for Missing API Key
def test_execute_missing_api_key():
    converter = URLToPDFConverter()
    url = "http://example.com"
    
    with pytest.raises(ValueError, match="API key cannot be empty."):
        converter.execute(url, "")

# Test Case 4: Test for Missing Output Directory
def test_execute_without_output_dir(mock_requests_post, mock_requests_get):
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "Files": [{"FileName": "test_output.pdf", "Url": "http://example.com/test_output.pdf"}],
        "ConversionCost": 5
    }
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.content = b"PDF content"

    converter = URLToPDFConverter()
    url = "http://example.com"
    api_key = "valid_api_key"
    
    response = converter.execute(url, api_key, output_dir=None)
    
    assert response["status"] == "success"
    assert response["file_name"] == "test_output.pdf"
    assert response["file_url"] == "http://example.com/test_output.pdf"

# Test Case 5: Test for Invalid API Key
def test_execute_invalid_api_key(mock_requests_post):
    mock_requests_post.return_value.status_code = 401
    mock_requests_post.return_value.json.return_value = {"error": "Invalid API key"}

    converter = URLToPDFConverter()
    url = "http://example.com"
    api_key = "invalid_api_key"

    with pytest.raises(ValueError, match=r"Invalid API key provided\."):
        converter.execute(url, api_key)

# Test Case 6: Test for API Error (Bad Request)
def test_execute_api_bad_request(mock_requests_post):
    mock_requests_post.return_value.status_code = 400
    mock_requests_post.return_value.json.return_value = {"error": "Bad request"}

    converter = URLToPDFConverter()
    url = "http://example.com"
    api_key = "valid_api_key"

    with pytest.raises(ValueError, match=r"An unexpected error occurred: Bad request: Invalid parameters or URL\."):

        converter.execute(url, api_key)

# Test Case 7: Test for Server Error (500+)
def test_execute_server_error(mock_requests_post):
    mock_requests_post.return_value.status_code = 500
    mock_requests_post.return_value.json.return_value = {"error": "Server error"}

    converter = URLToPDFConverter()
    url = "http://example.com"
    api_key = "valid_api_key"

    with pytest.raises(ValueError, match=r"Server error: 500"):
        converter.execute(url, api_key)

# Test Case 8: Test Health Check Success
def test_health_check_success(mock_requests_get):
    # Mock successful health check response
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {"status": "healthy"}

    converter = URLToPDFConverter()
    api_key = "valid_api_key"

    response = converter.health_check(api_key)

    assert response["status"] == "healthy"
    mock_requests_get.assert_called_once_with(
        "https://v2.convertapi.com/health", headers={"Authorization": "Bearer valid_api_key"}
    )

# Test Case 9: Test Health Check Failure
def test_health_check_failure(mock_requests_get):
    # Mock failed health check response
    mock_requests_get.return_value.status_code = 500
    mock_requests_get.return_value.json.return_value = {"error": "Server error"}

    converter = URLToPDFConverter()
    api_key = "valid_api_key"

    with pytest.raises(ValueError, match="ConvertAPI service is unhealthy."):
        converter.health_check(api_key)

# Test Case 10: Test for Invalid Response Format
def test_execute_invalid_response_format(mock_requests_post):
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {"status": "success"}  # Missing 'Files' key

    converter = URLToPDFConverter()
    url = "http://example.com"
    api_key = "valid_api_key"

    with pytest.raises(ValueError, match="Unexpected response format from the API."):
        converter.execute(url, api_key)
