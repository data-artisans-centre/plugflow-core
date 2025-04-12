import json
import requests
from typing import Dict, Any
from log import logger
from core.base import AgentBase

class LyricsAgent(AgentBase):
    """Agent to fetch song lyrics using the Lyrics.ovh API."""
    
    def __init__(self):
        """Initialize the LyricsAgent."""
        self.base_url = "https://api.lyrics.ovh/v1"
    
    def execute(self, **kwargs) -> Dict[str, Any]:
        """
        Fetch lyrics for the given artist and song title.
        
        Args:
            **kwargs: Keyword arguments including 'artist' and 'title'.
        
        Returns:
            dict: A dictionary containing the lyrics or an error message.
        
        Raises:
            ValueError: If fetching lyrics fails or invalid input is provided.
        """
        try:
            artist = kwargs.get("artist", "").strip()
            title = kwargs.get("title", "").strip()
            
            if not artist or not title:
                raise ValueError("Artist and song title cannot be empty.")
            
            url = f"{self.base_url}/{artist}/{title}"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                if "lyrics" in data and data["lyrics"]:
                    lyrics_result = {
                        "artist": artist,
                        "title": title,
                        "lyrics": data["lyrics"],
                    }
                    return lyrics_result
                else:
                    return {"error": "No lyrics found for this song."}
            else:
                return {"error": "Unable to fetch lyrics. Check the song title and artist name."}
        
        except Exception as e:
            logger.error(f"Lyrics fetching error: {e}")
            return {"error": f"Failed to fetch lyrics. {str(e)}"}
    
    def health_check(self) -> Dict[str, str]:
        """
        Perform a health check on the lyrics service.
        
        Returns:
            Dict with service health status.
        """
        try:
            logger.info("Performing lyrics API health check...")
            test_url = f"{self.base_url}/Coldplay/Yellow"
            response = requests.get(test_url)
            
            if response.status_code == 200:
                logger.info("Lyrics API health check passed.")
                return {"status": "healthy", "message": "Lyrics API is operational"}
            else:
                raise Exception("Lyrics API test request failed")
        
        except Exception as e:
            logger.error(f"Lyrics API health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
