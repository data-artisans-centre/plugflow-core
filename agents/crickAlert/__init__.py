import http.client
import json
from typing import Dict, Any, Optional, List, Union
from core.base import AgentBase
from log import logger

class CrickAlertAgent(AgentBase):
    """Agent to fetch cricket match information using Cricbuzz RapidAPI."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the CrickAlert agent with RapidAPI authentication.

        Args:
            api_key: Optional RapidAPI key for authentication
        """
        self.rapid_api_key = api_key
        self.rapid_api_host = "cricbuzz-cricket.p.rapidapi.com"
        self.base_url = "cricbuzz-cricket.p.rapidapi.com"

    def execute(self, **kwargs: Any) -> Union[str, Dict[str, str]]:
        """
        Fetch cricket matches based on the specified endpoint and search term.
        
        Args:
            **kwargs: Keyword arguments including:
                - api_key: RapidAPI key (required if not provided during init)
                - search_term: Term to search for in match details (optional)
                - endpoint: API endpoint to query (default: 'matches/v1/recent')

        Returns:
            Union[str, Dict[str, str]]: Match data or error information
        """
        conn = None
        try:
            self.rapid_api_key = kwargs.get("api_key", self.rapid_api_key)
            if not self.rapid_api_key:
                raise ValueError("API key must be provided")

            search_term = kwargs.get("search_term", "").strip().lower()
            endpoint = kwargs.get("endpoint", "matches/v1/recent")

            headers = {
                'x-rapidapi-key': self.rapid_api_key,
                'x-rapidapi-host': self.rapid_api_host
            }

            logger.info(f"Fetching cricket matches from endpoint: {endpoint}")
            if search_term:
                logger.info(f"Searching for matches containing: {search_term}")

            conn = http.client.HTTPSConnection(self.base_url)
            conn.request("GET", f"/{endpoint}", headers=headers)
            
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            
            if response.status != 200:
                raise ValueError(f"API request failed with status {response.status}: {data}")

            result = json.loads(data)
            all_matches = []
            
            # Process matches
            for type_match in result.get("typeMatches", []):
                for series_match in type_match.get("seriesMatches", []):
                    matches = series_match.get("seriesAdWrapper", {}).get("matches", [])
                    if matches:
                        all_matches.extend(matches)
            
            # Filter matches based on search term
            filtered_matches = []
            if all_matches:
                for match in all_matches:
                    if not search_term:
                        filtered_matches.append(match)
                        continue
                        
                    match_info = match.get("matchInfo", {})
                    
                    # Check series name
                    series_name = match_info.get("seriesName", "").lower()
                    if search_term in series_name:
                        filtered_matches.append(match)
                        continue
                        
                    # Check team names
                    team1_name = match_info.get("team1", {}).get("teamName", "").lower()
                    team2_name = match_info.get("team2", {}).get("teamName", "").lower()
                    if search_term in team1_name or search_term in team2_name:
                        filtered_matches.append(match)
                        continue
                        
                    # Check venue information
                    venue_info = match_info.get("venueInfo", {})
                    ground = venue_info.get("ground", "").lower()
                    city = venue_info.get("city", "").lower()
                    if search_term in ground or search_term in city:
                        filtered_matches.append(match)
                        continue
                        
                    # Check match format and description
                    match_format = match_info.get("matchFormat", "").lower()
                    match_desc = match_info.get("matchDesc", "").lower()
                    if search_term in match_format or search_term in match_desc:
                        filtered_matches.append(match)
            
            return {
                "status": "success",
                "matches": filtered_matches,
                "count": len(filtered_matches),
                "search_term": search_term if search_term else None
            }

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            return {"error": f"Invalid JSON response: {str(e)}", "status": "failed"}
        except Exception as e:
            logger.error(f"Error fetching cricket matches: {e}")
            return {"error": str(e), "status": "failed"}
        finally:
            if conn:
                conn.close()

    def health_check(self) -> Dict[str, str]:
        """
        Check if the RapidAPI Cricbuzz connection is functional.

        Returns:
            Dict[str, str]: Service health status and message
        """
        try:
            logger.info("Performing RapidAPI Cricbuzz health check...")
            
            if not self.rapid_api_key:
                return {"status": "unknown", "message": "API key not provided"}
                
            result = self.execute(api_key=self.rapid_api_key, endpoint="matches/v1/recent")
            
            if isinstance(result, dict) and result.get("status") == "success":
                logger.info("RapidAPI Cricbuzz health check passed.")
                return {
                    "status": "healthy",
                    "message": "Cricbuzz API service is available"
                }
            
            raise ValueError(result.get("error", "Unknown error occurred"))
            
        except Exception as e:
            logger.error(f"RapidAPI Cricbuzz health check failed: {e}")
            return {
                "status": "unhealthy",
                "message": str(e)
            }