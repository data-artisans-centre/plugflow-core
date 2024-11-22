from core.base import PluginBase
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
import json
from itertools import islice

class Plugin(PluginBase):
    """YouTube Review Plugin"""

    def execute(self, video_url, max_comments=10):
        """
        Fetch comments from a YouTube video and return as JSON.

        Args:
            video_url (str): The URL of the YouTube video.
            max_comments (int): Maximum number of comments to fetch.

        Returns:
            JSON: The comments data in JSON format.

        Raises:
            ValueError: If the URL is invalid or the comments cannot be fetched.
        """
        try:
            print(f"Fetching comments from video: {video_url}")
            downloader = YoutubeCommentDownloader()
            comments = downloader.get_comments_from_url(video_url)
            print(json.dumps(list(comments), indent=4))
            return [comment for _, comment in zip(range(max_comments), comments)]
        except ValueError as e:
            print(f"An error occurred: {e}")
            raise ValueError("Invalid URL") from e
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            raise e
    
    def health_check(self):
        """
        Check if the YouTube comment downloader is functional.

        Returns:
            dict: Health status of the plugin.
        """
        try:
            print("Performing health check...")
            downloader = YoutubeCommentDownloader()
            # Test with a known valid video ID
            dummy_video_url = "https://www.youtube.com/watch?v=ScMzIvxBSi4"
            comments = downloader.get_comments_from_url(dummy_video_url)
            next(comments)  # Attempt to fetch the first comment
            return {"status": "healthy", "message": "Service is available"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}

