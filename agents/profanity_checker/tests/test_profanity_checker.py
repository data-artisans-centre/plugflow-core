import pytest
from unittest.mock import patch, MagicMock
from agents.profanity_checker import ProfanityCheckerAgent, ProfanityCheckResponse


# Mock response for the profanity check
def mock_profanity_check_response(*args, **kwargs):
    """Mock the API response for profanity check."""
    return {
        "bad_words_list": [
            {
                "deviations": 0,
                "end": 16,
                "info": 2,
                "original": "shitty",
                "replacedLen": 6,
                "start": 10,
                "word": "shitty"
            }
        ],
        "bad_words_total": 1,
        "censored_content": "this is a ****** sentence",
        "content": "this is a shitty sentence"
    }


# Mock response for the health check
def mock_health_check_response(*args, **kwargs):
    """Mock the health check response."""
    return {"status": "healthy", "message": "Service is available"}


@pytest.fixture
def profanity_checker_agent():
    """Fixture to initialize the ProfanityCheckerAgent."""
    return ProfanityCheckerAgent()


@patch("requests.post")
def test_execute_success(mock_post, profanity_checker_agent):
    """Test successful execution of profanity check."""
    # Mock the API response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json = MagicMock(return_value=mock_profanity_check_response())

    text = "This is a shitty sentence"
    api_key = "valid-api-key"
    result = profanity_checker_agent.execute(text, api_key)

    # Check the result
    assert "bad_words_list" in result, "Expected bad_words_list in response."
    assert len(result["bad_words_list"]) == 1, "Expected one bad word in the response."
    assert result["censored_content"] == "this is a ****** sentence", "Censorship did not work."


@patch("requests.post")
def test_execute_empty_text(mock_post, profanity_checker_agent):
    """Test execution with empty text."""
    text = ""
    api_key = "valid-api-key"
    
    with pytest.raises(ValueError, match="Input text cannot be empty."):
        profanity_checker_agent.execute(text, api_key)


@patch("requests.post")
def test_execute_invalid_api_key(mock_post, profanity_checker_agent):
    """Test execution with invalid API key."""
    # Mock the API failure response
    mock_post.return_value.status_code = 401
    mock_post.return_value.text = '{"message": "Invalid authentication credentials"}'

    text = "This is a shitty sentence"
    invalid_api_key = "invalid-api-key"

    with pytest.raises(ValueError, match="An error occurred while processing the request."):
        profanity_checker_agent.execute(text, invalid_api_key)


@patch("requests.post")
def test_execute_unexpected_response(mock_post, profanity_checker_agent):
    """Test execution with unexpected API response."""
    # Mock an unexpected response
    mock_post.return_value.status_code = 200
    mock_post.return_value.json = MagicMock(return_value={})

    text = "This is a shitty sentence"
    api_key = "valid-api-key"
    
    with pytest.raises(ValueError, match="An error occurred while processing the request."):
        profanity_checker_agent.execute(text, api_key)


@patch("requests.post")
def test_health_check_success(mock_post, profanity_checker_agent):
    """Test health check success."""
    # Mock the API response for health check
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "bad_words_list": [],
        "bad_words_total": 0,
        "censored_content": "This is a test.",
        "content": "This is a test."
    }

    # Mock the execute method to simulate the behavior of the API call
    with patch.object(profanity_checker_agent, 'execute', return_value=mock_response):

        # Simulating the successful health check
        health_status = profanity_checker_agent.health_check("valid-api-key")

    # Check if the response has the expected status
    assert health_status["status"] == "healthy", "Expected health status to be 'healthy'."
    
@patch("requests.post")
def test_health_check_failure(mock_post, profanity_checker_agent):
    """Test health check failure."""
    # Mock a failed health check response
    mock_post.return_value.status_code = 500
    mock_post.return_value.text = "Internal Server Error"

    api_key = "valid-api-key"
    health_status = profanity_checker_agent.health_check(api_key)
    print(health_status)

    # Check health status
    assert health_status["status"] == "unhealthy", "Expected health status to be 'unhealthy'."
    assert "An error occurred" in health_status["message"],"Expected failure message."

