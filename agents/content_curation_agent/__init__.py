import asyncio
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from core.base import AgentBase
import aiohttp
from bs4 import BeautifulSoup
import requests
from scholarly import scholarly
import newspaper
import spacy
import sumy
from transformers import pipeline
from typing import Any
import logging

class ResearchQuery(BaseModel):
    """
    Model for defining research search parameters
    """
    query: str = Field(..., description="Primary search query")
    sources: List[str] = Field(
        default=['scholar', 'arxiv', 'web'], 
        description="Sources to search"
    )
    max_results: int = Field(default=10, ge=1, le=50)
    language: str = Field(default='en')
    domains: Optional[List[str]] = None
    
class ResearchResult(BaseModel):
    """
    Structured model for research results
    """
    title: str
    url: str
    source: str
    summary: Optional[str] = None
    authors: Optional[List[str]] = None
    published_date: Optional[str] = None
    relevance_score: Optional[float] = None

class ContentCurationAgent(AgentBase):
    """
    Advanced Content Curation and Research Agent
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize agent with configuration
        
        Args:
            config (Dict[str, Any]): Configuration parameters
        """
        # Load NLP models
        self.nlp = spacy.load('en_core_web_sm')
        self.summarization_model = pipeline("summarization")
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    async def fetch_web_content(self, url: str) -> Dict[str, str]:
        """
        Asynchronously fetch web content
        
        Args:
            url (str): URL to fetch content from
        
        Returns:
            Dict containing extracted content
        """
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        html = await response.text()
                        article = newspaper.Article(url)
                        article.download()
                        article.parse()
                        
                        return {
                            'title': article.title,
                            'text': article.text,
                            'authors': article.authors,
                            'published_date': str(article.publish_date)
                        }
            except Exception as e:
                self.logger.error(f"Error fetching {url}: {e}")
                return {}

    def scholar_search(self, query: str, max_results: int = 10) -> List[ResearchResult]:
        """
        Search academic papers using Google Scholar
        
        Args:
            query (str): Search query
            max_results (int): Maximum number of results
        
        Returns:
            List of research results
        """
        results = []
        for _ in range(max_results):
            try:
                search_query = scholarly.search_pubs(query)
                publication = next(search_query)
                
                result = ResearchResult(
                    title=publication.get('bib', {}).get('title', ''),
                    url=publication.get('bib', {}).get('url', ''),
                    source='scholar',
                    authors=publication.get('bib', {}).get('author', []),
                    published_date=publication.get('bib', {}).get('pub_year', None)
                )
                results.append(result)
            except StopIteration:
                break
        
        return results

    async def execute(self, research_query: Dict[str, Any]) -> List[ResearchResult]:
        """
        Execute comprehensive research based on query
        
        Args:
            research_query (Dict[str, Any]): Research parameters
        
        Returns:
            List of curated research results
        """
        query_model = ResearchQuery(**research_query)
        results = []

        # Parallel search across sources
        tasks = []
        
        # Scholar search
        if 'scholar' in query_model.sources:
            scholar_results = self.scholar_search(
                query_model.query, 
                max_results=query_model.max_results
            )
            results.extend(scholar_results)
        
        # Web content fetching
        if 'web' in query_model.sources:
            web_tasks = [
                self.fetch_web_content(result.url) 
                for result in results if result.url
            ]
            web_contents = await asyncio.gather(*web_tasks)
            
            # Enrich results with web content
            for idx, content in enumerate(web_contents):
                if content:
                    results[idx].summary = self._generate_summary(content.get('text', ''))

        return results

    def _generate_summary(self, text: str, max_length: int = 150) -> str:
        """
        Generate concise summary using transformer model
        
        Args:
            text (str): Input text
            max_length (int): Maximum summary length
        
        Returns:
            Summarized text
        """
        try:
            summary = self.summarization_model(
                text, 
                max_length=max_length, 
                min_length=30, 
                do_sample=False
            )[0]['summary_text']
            return summary
        except Exception as e:
            self.logger.error(f"Summary generation error: {e}")
            return ""

    def health_check(self) -> Dict[str, str]:
        """
        Perform system health check
        
        Returns:
            Health status dictionary
        """
        try:
            # Basic connectivity and model load checks
            assert self.nlp is not None
            assert self.summarization_model is not None
            
            return {
                "status": "healthy",
                "message": "Content Curation Agent is fully operational",
                "models_loaded": True
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Health check failed: {e}",
                "models_loaded": False
            }