import http.client
import json
from typing import Dict, Any, Optional
from log import logger
from core.base import AgentBase

class AmazonProductAgent(AgentBase):
    """Agent to fetch product details from Amazon using the Real-Time Amazon Data API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with RapidAPI key"""
        self.api_key = api_key
        self.host = "real-time-amazon-data.p.rapidapi.com"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Fetch product details from Amazon."""    
        try:
            api_key = kwargs.get('api_key', self.api_key)
            query = kwargs.get('query', '').strip()
            
            if not api_key or not query:
                return {"error": "API key and query are required", "status": "failed"}
            
            # Get optional parameters with defaults
            page = kwargs.get('page', 1)
            country = kwargs.get('country', 'IN')
            sort_by = kwargs.get('sort_by', 'RELEVANCE')
            product_condition = kwargs.get('product_condition', 'ALL')
            is_prime = 'true' if kwargs.get('is_prime', False) else 'false'
            deals_and_discounts = kwargs.get('deals_and_discounts', 'NONE')
            
            logger.info(f"Searching Amazon for: {query}")
            
            # Prepare request
            headers = {
                'x-rapidapi-key': api_key,
                'x-rapidapi-host': self.host
            }
            
            endpoint = f"/search?query={query}&page={page}&country={country}" \
                       f"&sort_by={sort_by}&product_condition={product_condition}" \
                       f"&is_prime={is_prime}&deals_and_discounts={deals_and_discounts}"
            
            # Make API request
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", endpoint, headers=headers)
            response = conn.getresponse()
            data = response.read()
            
            # Handle response
            if response.status == 200:
                return {
                    "status": "success",
                    "data": json.loads(data.decode("utf-8"))
                }
            else:
                try:
                    error_data = json.loads(data.decode("utf-8"))
                    error_msg = error_data.get('message', f"API request failed with status code {response.status}")
                except:
                    error_msg = f"API request failed with status code {response.status}"
                    
                logger.error(error_msg)
                return {"error": error_msg, "status": "failed"}
                
        except Exception as e:
            logger.error(f"Error fetching Amazon products: {e}")
            return {"error": str(e), "status": "failed"}
    
    def health_check(self) -> Dict[str, str]:
        """Check if the Amazon Product API connection is functional."""
        try:
            if not self.api_key:
                return {"status": "unhealthy", "message": "No API key provided"}
            
            headers = {
                'x-rapidapi-key': self.api_key,
                'x-rapidapi-host': self.host
            }
            
            conn = http.client.HTTPSConnection(self.host)
            conn.request("GET", "/search?query=test&page=1&country=US", headers=headers)
            response = conn.getresponse()
            
            if response.status == 200:
                return {"status": "healthy", "message": "Amazon Product API service is available"}
            else:
                return {"status": "unhealthy", "message": f"Health check failed with status code {response.status}"}
                
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}