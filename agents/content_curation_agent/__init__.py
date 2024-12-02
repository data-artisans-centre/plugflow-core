import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from core.base import AgentBase
from utils.models import ResearchQuery, ResearchResult
from sources.scholar import ScholarSearchClient
from sources.web import WebContentExtractor
from processing.summarization import TextSummarizer
from log import logger


class ResearchAnalysis(BaseModel):
    """Pydantic model to hold analysis results for research items."""
    title: str = Field(..., description="Title of the research item.")
    summary: str = Field(..., description="Summarized content of the research item.")
    source: str = Field(..., description="Source of the research item.")
    url: str = Field(..., description="URL of the research item.")
    relevance_score: float = Field(..., description="Relevance score based on the query.")


class ResearchAgent(AgentBase):
    """Main research agent for integrating various research tools and sources."""

    def __init__(self):
        super().__init__()
        self.name = "main-research-agent"
        self.summarizer = TextSummarizer()
        self.scholar_client = ScholarSearchClient()
        self.web_extractor = WebContentExtractor()
        logger.info(f"{self.name} initialized.")

    async def analyze_query(self, query: Dict[str, Any]) -> List[ResearchAnalysis]:
        """
        Process a research query asynchronously and return analysis results.

        Args:
            query (Dict[str, Any]): Research query parameters.

        Returns:
            List[ResearchAnalysis]: A list of analysis results.
        """
        try:
            research_query = ResearchQuery(**query)
            results = []

            # Task list for parallel processing
            tasks = []

            if 'scholar' in research_query.sources:
                tasks.append(
                    self.scholar_client.search(
                        research_query.query,
                        research_query.max_results
                    )
                )

            if 'web' in research_query.sources:
                tasks.append(
                    self.web_extractor.search_web_content(research_query.query)
                )

            # Gather results from all sources
            sources_results = await asyncio.gather(*tasks)
            for source in sources_results:
                if not source:
                    continue

                for item in source:
                    try:
                        # Summarize content
                        summary = self.summarizer.summarize(item.content)
                        analysis_data = {
                            "title": item.title,
                            "summary": summary,
                            "source": item.source,
                            "url": item.url,
                            "relevance_score": item.relevance_score
                        }
                        result = ResearchAnalysis(**analysis_data)
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Error analyzing research item: {e}")

            return results

        except Exception as e:
            logger.error(f"Error processing research query: {e}")
            raise ValueError("Invalid research query.") from e

    def health_check(self) -> Dict[str, Any]:
        """
        Check if the research agent is functional.

        Returns:
            dict: Health status of the agent.
        """
        try:
            logger.info("Performing health check for ResearchAgent...")
            # Simple check with a mock query
            mock_query = {
                "query": "Sample Query for Health Check",
                "sources": ["scholar", "web"],
                "max_results": 1
            }
            asyncio.run(self.analyze_query(mock_query))
            logger.info("Health check passed.")
            return {"status": "healthy", "message": "Service is operational"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
