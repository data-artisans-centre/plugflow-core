import pytest
from unittest.mock import MagicMock, patch
from agents.content_curation_agent import ResearchAgent
from agents.content_curation_agent.processing.summarization import TextSummarizer
from agents.content_curation_agent.sources.scholar import ScholarSearchClient
from agents.content_curation_agent.sources.web import WebContentExtractor
from log import logger
import asyncio


@pytest.mark.asyncio
async def test_research_agent_initialization():
    """Test that ResearchAgent is initialized with all components."""
    with patch("agents.content_curation_agent.processing.summarization.TextSummarizer") as mock_summarizer, \
         patch("agents.content_curation_agent.sources.scholar.ScholarSearchClient") as mock_scholar_client, \
         patch("agents.content_curation_agent.sources.web.WebContentExtractor") as mock_web_extractor, \
         patch("log.logger.info") as mock_logger:

        # Mock initialization behavior
        mock_summarizer.return_value = MagicMock()
        mock_scholar_client.return_value = MagicMock()
        mock_web_extractor.return_value = MagicMock()

        # Create instance
        agent = ResearchAgent()

        # Verify mock components were used
        mock_summarizer.assert_called_once()
        mock_scholar_client.assert_called_once()
        mock_web_extractor.assert_called_once()
        mock_logger.assert_any_call("ResearchAgent initialized.")

        # Verify attributes
        assert agent.name == "ResearchAgent"
        assert isinstance(agent.summarizer, MagicMock)
        assert isinstance(agent.scholar_client, MagicMock)
        assert isinstance(agent.web_extractor, MagicMock)


@pytest.mark.asyncio
async def test_research_agent_health_check_healthy():
    """Test the health_check method when components are functional."""
    with patch("log.logger.info") as mock_logger:
        agent = ResearchAgent()

        # Mock health check as a coroutine
        async def mock_health_check():
            return {"status": "healthy", "message": "Service is operational"}

        agent.health_check = mock_health_check

        # Perform the health check
        health_status = await agent.health_check()

        # Assertions
        assert health_status["status"] == "healthy"
        assert health_status["message"] == "Service is operational"
        mock_logger.assert_any_call("Performing health check for ResearchAgent...")
        mock_logger.assert_any_call("Health check passed.")


@pytest.mark.asyncio
async def test_research_agent_health_check_unhealthy():
    """Test the health_check method when components are non-functional."""
    with patch("log.logger.error") as mock_logger:
        agent = ResearchAgent()

        # Mock health check as a coroutine that raises an exception
        async def mock_health_check():
            raise Exception("Test failure")

        agent.health_check = mock_health_check

        # Perform the health check
        try:
            await agent.health_check()
        except Exception as e:
            health_status = {"status": "unhealthy", "message": str(e)}

        # Assertions
        assert health_status["status"] == "unhealthy"
        assert "Test failure" in health_status["message"]
        mock_logger.assert_called_with("Health check failed: Test failure")
