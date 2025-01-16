import http.client
import json
from core.base import AgentBase
from log import logger

class CrickAlertAgent(AgentBase):
    """Agent to fetch cricket match information using Cricbuzz RapidAPI."""

    def __init__(self, api_key=None):
        """Initialize the CrickAlert agent with RapidAPI authentication."""
        self.rapid_api_key = api_key
        self.rapid_api_host = "cricbuzz-cricket.p.rapidapi.com"
        self.base_url = "cricbuzz-cricket.p.rapidapi.com"

    def safe_get(self, obj, *keys, default="N/A"):
        """Safely get nested dictionary values."""
        try:
            for key in keys:
                if obj is None:
                    return default
                obj = obj.get(key, default)
            return obj if obj is not None else default
        except Exception:
            return default

    def match_contains_term(self, match, search_term):
        """Check if a match contains the search term in its details."""
        if not search_term:
            return True
            
        search_term = search_term.lower()
        match_info = self.safe_get(match, "matchInfo", default={})
        
        # Check in series name
        series_name = self.safe_get(match_info, "seriesName", "").lower()
        if search_term in series_name:
            return True
            
        # Check in team names
        team1_name = self.safe_get(match_info, "team1", "teamName", "").lower()
        team2_name = self.safe_get(match_info, "team2", "teamName", "").lower()
        if search_term in team1_name or search_term in team2_name:
            return True
            
        # Check in venue
        venue = self.safe_get(match_info, "venueInfo", "ground", "").lower()
        if search_term in venue:
            return True
            
        return False

    def format_match(self, match):
        """Format a single match into the desired structured output."""
        try:
            match_info = self.safe_get(match, "matchInfo", default={})
            match_score = self.safe_get(match, "matchScore", default={})
            
            # Basic match details
            match_id = self.safe_get(match_info, "matchId")
            series_name = self.safe_get(match_info, "seriesName")
            match_desc = self.safe_get(match_info, "matchDesc")
            match_format = self.safe_get(match_info, "matchFormat")
            state = self.safe_get(match_info, "state")
            status = self.safe_get(match_info, "status")
            
            # Team information
            team1_info = self.safe_get(match_info, "team1", default={})
            team2_info = self.safe_get(match_info, "team2", default={})
            
            team1_name = self.safe_get(team1_info, "teamName", default="Team 1")
            team2_name = self.safe_get(team2_info, "teamName", default="Team 2")
            
            # Format scores
            team1_score = "No score"
            team2_score = "No score"
            
            if match_score:
                team1_innings = self.safe_get(match_score, "team1Score", default=[{}])[0]
                if team1_innings:
                    runs = self.safe_get(team1_innings, "runs", default="")
                    wickets = self.safe_get(team1_innings, "wickets", default="")
                    overs = self.safe_get(team1_innings, "overs", default="")
                    if runs:
                        team1_score = f"{runs}/{wickets} ({overs} overs)"
                
                team2_innings = self.safe_get(match_score, "team2Score", default=[{}])[0]
                if team2_innings:
                    runs = self.safe_get(team2_innings, "runs", default="")
                    wickets = self.safe_get(team2_innings, "wickets", default="")
                    overs = self.safe_get(team2_innings, "overs", default="")
                    if runs:
                        team2_score = f"{runs}/{wickets} ({overs} overs)"
            
            # Venue information
            venue_info = self.safe_get(match_info, "venueInfo", default={})
            ground = self.safe_get(venue_info, "ground")
            city = self.safe_get(venue_info, "city")
            
            formatted_match = f"""
### Match Details
Match ID: {match_id}
Series: {series_name}
Format: {match_format}
Description: {match_desc}
State: {state}
Status: {status}

Teams:
- {team1_name} vs {team2_name}

Scores:
- {team1_name}: {team1_score}
- {team2_name}: {team2_score}

Venue: {ground}
Location: {city}
"""
            return formatted_match.strip()
        except Exception as e:
            logger.error(f"Error formatting match: {str(e)}")
            return None

    def execute(self, **kwargs):
        """
        Fetch cricket matches based on the specified endpoint and search term.
        
        Args:
            kwargs (dict): Input arguments containing:
                - api_key (str): RapidAPI key (required if not provided during init)
                - search_term (str): Term to search for in match details (optional)
                - endpoint (str): API endpoint to query (default: 'matches/v1/recent')
        """
        conn = None
        try:
            self.rapid_api_key = kwargs.get("api_key", self.rapid_api_key)
            if not self.rapid_api_key:
                raise ValueError("API key must be provided either during initialization or execution")

            search_term = kwargs.get("search_term", "").strip()
            endpoint = kwargs.get("endpoint", "matches/v1/recent")

            headers = {
                'x-rapidapi-key': self.rapid_api_key,
                'x-rapidapi-host': self.rapid_api_host
            }

            logger.info(f"Fetching cricket matches from endpoint: {endpoint}")
            if search_term:
                logger.info(f"Filtering matches for term: {search_term}")

            conn = http.client.HTTPSConnection(self.base_url)
            conn.request("GET", f"/{endpoint}", headers=headers)
            
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            
            if response.status != 200:
                raise ValueError(f"API request failed with status code {response.status}")

            result = json.loads(data)
            type_matches = result.get("typeMatches", [])
            all_matches = []
            
            for type_match in type_matches:
                series_matches = type_match.get("seriesMatches", [])
                for series_match in series_matches:
                    matches = series_match.get("seriesAdWrapper", {}).get("matches", [])
                    if matches:
                        all_matches.extend(matches)
            
            # Filter matches based on search term
            filtered_matches = [
                match for match in all_matches 
                if self.match_contains_term(match, search_term)
            ]
            
            if not filtered_matches:
                return f"No matches found for '{search_term}'" if search_term else "No matches found"
                
            formatted_matches = []
            for match in filtered_matches:
                formatted_match = self.format_match(match)
                if formatted_match:
                    formatted_matches.append(formatted_match)
            
            if not formatted_matches:
                return f"No match details available for '{search_term}'"
                
            return "\n\n---\n\n".join(formatted_matches)

        except Exception as e:
            logger.error(f"An error occurred while fetching cricket matches: {e}")
            return {"error": str(e), "status": "failed"}
        finally:
            if conn:
                conn.close()

    def health_check(self):
        """Check if the RapidAPI Cricbuzz connection is functional."""
        try:
            logger.info("Performing RapidAPI Cricbuzz health check...")
            
            if not self.rapid_api_key:
                return {"status": "unknown", "message": "API key not provided"}
                
            result = self.execute(
                api_key=self.rapid_api_key,
                endpoint="matches/v1/recent"
            )
            
            if isinstance(result, str) and "error" not in result.lower():
                logger.info("RapidAPI Cricbuzz health check passed.")
                return {"status": "healthy", "message": "Cricbuzz API service is available"}
            else:
                raise ValueError(result.get("error", "Unknown error occurred"))
            
        except Exception as e:
            logger.error(f"RapidAPI Cricbuzz health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}