import json
from typing import Dict, List
from textblob import TextBlob
from pydantic import BaseModel, Field, ValidationError
from core.base import AgentBase
from log import logger


class CommentAnalysis(BaseModel):
    """Pydantic model to hold analysis results for a single comment."""
    comment: str = Field(..., description="The text of the comment.")
    sentiment_polarity: float = Field(..., description="Sentiment polarity of the comment (-1 to 1).")
    sentiment_subjectivity: float = Field(..., description="Subjectivity of the comment (0 to 1).")
    readability_score: float = Field(..., description="Custom Reading Ease score.")
    review_length: int = Field(..., description="Length of the comment in words.")


class ReadabilityScorer:
    """Custom readability scoring implementation."""
    @staticmethod
    def calculate_flesch_reading_ease(text: str) -> float:
        """
        Calculate a custom Flesch Reading Ease equivalent score.
        
        Args:
            text (str): The text to analyze.
        
        Returns:
            float: A readability score similar to Flesch Reading Ease.
        """
        # Count sentences (minimum 1 to avoid division by zero)
        sentences = max(1, len([s for s in text.split('.') if s.strip()]))
        
        # Count words
        words = text.split()
        word_count = len(words)
        
        # Count syllables (simplified estimation)
        def count_syllables(word: str) -> int:
            vowels = 'aeiouy'
            word = word.lower()
            count = 0
            if len(word) > 3:
                if word.endswith('e'):
                    word = word[:-1]
            
            # Count vowel groups
            for index in range(len(word)):
                if (word[index] in vowels and 
                    (index == 0 or word[index-1] not in vowels)):
                    count += 1
            
            return max(1, count)
        
        syllable_count = sum(count_syllables(word) for word in words)
        
        # Custom Flesch-like readability calculation
        try:
            score = 206.835 - (
                1.015 * (word_count / sentences) - 
                84.6 * (syllable_count / word_count)
            )
            return max(0, min(100, score))  # Bound between 0-100
        except ZeroDivisionError:
            return 50.0  # Default score if calculation fails


class YouTubeReviewAnalyzer(AgentBase):
    """Agent to analyze YouTube comments."""

    def __init__(self):
        super().__init__()
        self.name = "youtube-review-analyzer"
        self.readability_scorer = ReadabilityScorer()

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
            "readability_score": self.readability_scorer.calculate_flesch_reading_ease(comment_text),
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
                    "author": comment.get("author", "Unknown"),
                    "original_comment": comment["comment"],
                    "likes": comment.get("likes", 0),
                    "time": comment.get("time", "Unknown"),
                    "analysis": analysis.model_dump()
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