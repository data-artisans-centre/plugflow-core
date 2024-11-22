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
        """
        try:
            print(f"Fetching comments from video: {video_url}")
            downloader = YoutubeCommentDownloader()
            comments = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)

            # Fetch and limit the number of comments
            limited_comments = list(islice(comments, max_comments))

            # Convert comments to JSON format
            comments_json = json.dumps(limited_comments, indent=4)
            print(f"Fetched {len(limited_comments)} comments.")
            print(comments_json)
            return comments_json
        except Exception as e:
            print(f"An error occurred: {e}")
            return json.dumps({"error": str(e)})

