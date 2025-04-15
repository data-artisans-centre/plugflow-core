import http.client
import json
import urllib.parse
from core.base import AgentBase
from log import logger

class SpotifySearchAgent(AgentBase):
    """Agent to search Spotify using RapidAPI."""
    
    def __init__(self, api_key=None):
        self.rapid_api_key = api_key
        self.rapid_api_host = "spotify23.p.rapidapi.com"
        self.base_url = "spotify23.p.rapidapi.com"

    def _filter_album_data(self, album_data):
        """Filter out coverArt and simplify album data structure."""
        filtered_data = {
            'uri': album_data['uri'],
            'name': album_data['name'],
            'artist': album_data['artists']['items'][0]['profile']['name'],
            'year': album_data['date']['year']
        }
        return filtered_data

    def execute(self, **kwargs):
        """
        Search Spotify for content.
        
        Args:
            kwargs (dict):
                - query (str): Search query (required)
                - api_key (str): RapidAPI key (required if not provided during init)
                - type (str): Search type (default: 'multi')
                - offset (int): Results offset (default: 0)
                - limit (int): Maximum results (default: 10)
                - top_results (int): Number of top results (default: 5)
        
        Returns:
            dict: Search results in JSON format
        """
        try:
            query = kwargs.get("query")
            if not query:
                raise ValueError("Search query is required")

            encoded_query = urllib.parse.quote(query)

            self.rapid_api_key = kwargs.get("api_key", self.rapid_api_key)
            if not self.rapid_api_key:
                raise ValueError("API key must be provided")

            search_type = kwargs.get("type", "multi")
            offset = kwargs.get("offset", 0)
            limit = kwargs.get("limit", 10)
            top_results = kwargs.get("top_results", 5)

            endpoint = f"/search/?q={encoded_query}&type={search_type}&offset={offset}&limit={limit}&numberOfTopResults={top_results}"

            headers = {
                'x-rapidapi-key': self.rapid_api_key,
                'x-rapidapi-host': self.rapid_api_host
            }

            logger.info(f"Searching Spotify for: {query}")

            conn = http.client.HTTPSConnection(self.base_url)
            conn.request("GET", endpoint, headers=headers)
            
            response = conn.getresponse()
            data = response.read()
            
            if response.status != 200:
                error_message = f"API request failed with status {response.status}"
                try:
                    error_data = json.loads(data.decode("utf-8"))
                    if isinstance(error_data, dict) and "message" in error_data:
                        error_message += f": {error_data['message']}"
                except:
                    pass
                raise ValueError(error_message)

            response_data = json.loads(data.decode("utf-8"))
            
            # Filter and restructure the response
            if 'albums' in response_data:
                filtered_albums = {
                    'total_count': response_data['albums']['totalCount'],
                    'albums': [
                        self._filter_album_data(item['data']) 
                        for item in response_data['albums']['items']
                    ]
                }
                return filtered_albums
            return response_data

        except Exception as e:
            logger.error(f"Error during Spotify search: {e}")
            return {"error": str(e), "status": "failed"}
        finally:
            if 'conn' in locals():
                conn.close()

    def health_check(self):
        """Check if the Spotify API connection is functional."""
        try:
            logger.info("Performing Spotify search health check...")
            
            if not self.rapid_api_key:
                return {"status": "unknown", "message": "API key not provided"}
                
            result = self.execute(
                query="test",
                api_key=self.rapid_api_key,
                limit=1
            )
            
            if "error" not in result:
                logger.info("Spotify search health check passed")
                return {"status": "healthy", "message": "Spotify API service is available"}
            else:
                raise ValueError(result["error"])
            
        except Exception as e:
            logger.error(f"Spotify search health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}