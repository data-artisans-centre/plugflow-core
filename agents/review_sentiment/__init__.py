import json
from typing import Dict, List
from textblob import TextBlob
import textstat
from pydantic import BaseModel, Field, ValidationError
from core.base import AgentBase
from log import logger


class CommentAnalysis(BaseModel):
    """Pydantic model to hold analysis results for a single comment."""
    comment: str = Field(..., description="The text of the comment.")
    sentiment_polarity: float = Field(..., description="Sentiment polarity of the comment (-1 to 1).")
    sentiment_subjectivity: float = Field(..., description="Subjectivity of the comment (0 to 1).")
    readability_score: float = Field(..., description="Flesch Reading Ease score.")
    review_length: int = Field(..., description="Length of the comment in words.")


class YouTubeReviewAnalyzer(AgentBase):
    """Agent to analyze YouTube comments."""

    def __init__(self):
        super().__init__()
        self.name = "youtube-review-analyzer"

    def analyze_comment(self, comment_text: str) -> CommentAnalysis:
        """
        Analyze a single comment for sentiment and other metrics.

        Args:
            comment_text (str): The comment text to analyze.

        Returns:
            CommentAnalysis: A validated Pydantic model containing analysis results.
        """
        blob = TextBlob(comment_text)
        analysis_data = {
            "comment": comment_text,
            "sentiment_polarity": blob.sentiment.polarity,
            "sentiment_subjectivity": blob.sentiment.subjectivity,
            "readability_score": textstat.flesch_reading_ease(comment_text),
            "review_length": len(comment_text.split())
        }
        try:
            return CommentAnalysis(**analysis_data)
        except ValidationError as e:
            logger.error(f"Validation error for comment analysis: {e}")
            raise ValueError("Invalid analysis data.") from e

    def process_comments(self, comments_data: List[Dict]) -> List[Dict]:
        """
        Process a list of comment dictionaries and return analysis results.

        Args:
            comments_data (List[Dict]): A list of comment data dictionaries.

        Returns:
            List[Dict]: A list of processed analysis results.
        """
        results = []
        for comment in comments_data:
            try:
                analysis = self.analyze_comment(comment["comment"])
                result = {
                    "author": comment["author"],
                    "original_comment": comment["comment"],
                    "likes": comment["likes"],
                    "time": comment["time"],
                    "analysis": analysis.dict()  # Converts Pydantic model to dictionary
                }
                results.append(result)
            except Exception as e:
                logger.error(f"Error processing comment: {e}")
        return results


    def execute(self, video_url: str, max_comments: int = 10):
        """
        Fetch comments and perform analysis on a YouTube video.

        Args:
            video_url (str): The URL of the YouTube video.
            max_comments (int): Maximum number of comments to analyze.

        Returns:
            list: A list of analyzed comments.

        Raises:
            ValueError: If an error occurs during analysis.
        """
        try:
            logger.info(f"Fetching and analyzing comments for video: {video_url}")
            # For this example, we'll use sample comments
            # Replace with actual YouTube API integration or comment fetching logic
            sample_comments = [
                {
                    "author": "TestUser",
                    "comment": "This is a great video!",
                    "likes": 42,
                    "time": "2 days ago"
                }
            ]
            # Process comments
            results = self.process_comments(sample_comments)
            # Log results as JSON
            results_json = json.dumps(results, indent=4)
            logger.info(f"Analysis results: {results_json}")
            print(results_json)
            return results
        except Exception as e:
            logger.error(f"Error analyzing YouTube comments: {e}")
            raise ValueError("Failed to analyze comments.") from e

    def health_check(self):
        """
        Check if the analyzer is functional.

        Returns:
            dict: Health status of the plugin.
        """
        try:
            logger.info("Performing health check for YouTubeReviewAnalyzer...")
            # Simple check with sample data
            self.analyze_comment("This is a sample comment for health check.")
            logger.info("Health check passed.")
            return {"status": "healthy", "message": "Service is operational"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
