import pytest
from unittest.mock import MagicMock, patch
from content_curation_agent import ResearchAgent
from processing.summarization import TextSummarizer
from sources.scholar import ScholarSearchClient
from sources.web import WebContentExtractor
from log import logger


def test_research_agent_initialization():
    """Test that ResearchAgent is initialized with all components."""
    with patch("processing.summarization.TextSummarizer") as mock_summarizer, \
         patch("sources.scholar.ScholarSearchClient") as mock_scholar_client, \
         patch("sources.web.WebContentExtractor") as mock_web_extractor, \
         patch("log.logger.info") as mock_logger:

        # Create instance
        agent = ResearchAgent()

        # Check component initialization
        mock_summarizer.assert_called_once()
        mock_scholar_client.assert_called_once()
        mock_web_extractor.assert_called_once()
        mock_logger.assert_called_with("__init__ initialized.")

        # Verify attributes
        assert agent.name == "__init__"
        assert isinstance(agent.summarizer, MagicMock)
        assert isinstance(agent.scholar_client, MagicMock)
        assert isinstance(agent.web_extractor, MagicMock)


def test_research_agent_health_check_healthy(mocker):
    """Test the health_check method when components are functional."""
    mocker.patch("asyncio.run", return_value=None)
    with patch("log.logger.info") as mock_logger:
        agent = ResearchAgent()
        health_status = agent.health_check()

        # Assertions
        assert health_status["status"] == "healthy"
        assert health_status["message"] == "Service is operational"
        mock_logger.assert_any_call("Performing health check for ResearchAgent...")
        mock_logger.assert_any_call("Health check passed.")


def test_research_agent_health_check_unhealthy(mocker):
    """Test the health_check method when components are non-functional."""
    mocker.patch("asyncio.run", side_effect=Exception("Test failure"))
    with patch("log.logger.error") as mock_logger:
        agent = ResearchAgent()
        health_status = agent.health_check()

        # Assertions
        assert health_status["status"] == "unhealthy"
        assert "Test failure" in health_status["message"]
        mock_logger.assert_called_with("Health check failed: Test failure")
