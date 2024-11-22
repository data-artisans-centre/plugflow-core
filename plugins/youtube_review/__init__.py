import logging
import json
from itertools import islice
from core.base import PluginBase
from youtube_comment_downloader import YoutubeCommentDownloader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Plugin(PluginBase):
    """YouTube Review Plugin"""

    def execute(self, video_url, max_comments=10):
        """
        Fetch comments from a YouTube video and return as a list of dictionaries.

        Args:
            video_url (str): The URL of the YouTube video.
            max_comments (int): Maximum number of comments to fetch.

        Returns:
            list: A list of dictionaries containing comment data.

        Raises:
            ValueError: If the URL is invalid or comments cannot be fetched.
        """
        try:
            logger.info(f"Fetching comments from video: {video_url}")
            downloader = YoutubeCommentDownloader()
            comments = downloader.get_comments_from_url(video_url)
            limited_comments = list(islice(comments, max_comments))
                        # Convert the list of comments to a JSON-formatted string
            comments_json = json.dumps(limited_comments, indent=4)
            #Log the JSON-formatted comments
            print(comments_json)
            return limited_comments
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise ValueError("Failed to fetch comments. Please check the video URL and try again.") from e

    def health_check(self):
        """
        Check if the YouTube comment downloader is functional.

        Returns:
            dict: Health status of the plugin.
        """
        try:
            logger.info("Performing health check...")
            downloader = YoutubeCommentDownloader()
            # Test with a known valid video URL
            dummy_video_url = "https://www.youtube.com/watch?v=ScMzIvxBSi4"
            comments = downloader.get_comments_from_url(dummy_video_url)
            next(comments)  # Attempt to fetch the first comment
            logger.info("Health check passed.")
            return {"status": "healthy", "message": "Service is available"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}

