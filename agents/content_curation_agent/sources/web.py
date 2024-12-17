import httpx
import trafilatura
from typing import Dict, Optional
from ..utils.exceptions import ExtractionError
import logging

class WebContentExtractor:
    """Efficient web content extraction"""
    
    @staticmethod
    async def extract(url: str) -> Optional[Dict[str, str]]:
        """
        Asynchronously extract web content
        
        Args:
            url (str): URL to extract content from
        
        Returns:
            Extracted content dictionary
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, follow_redirects=True)
                
                # Primary extraction with trafilatura
                extracted = trafilatura.extract(
                    response.text,
                    include_comments=False,
                    include_links=False
                )
                
                if not extracted:
                    raise ExtractionError(f"No content extracted from {url}")
                
                return {
                    'text': extracted,
                    'title': trafilatura.extract_title(response.text) or '',
                    'url': url
                }
        
        except Exception as e:
            logging.error(f"Web extraction error for {url}: {e}")
            raise ExtractionError(f"Failed to extract web content: {e}")