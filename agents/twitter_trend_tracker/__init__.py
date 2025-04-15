import http.client
import json
from core.base import AgentBase
from log import logger

class TwitterHashtagAgent(AgentBase):
    """Agent to fetch tweets by hashtag using RapidAPI."""

    def __init__(self, api_key=None):
        """
        Initialize the Twitter hashtag agent with RapidAPI authentication.
        
        Args:
            api_key (str, optional): RapidAPI key. Can be provided during initialization 
                                   or during execution.
        """
        self.rapid_api_key = api_key
        self.rapid_api_host = "twitter154.p.rapidapi.com"
        self.base_url = "twitter154.p.rapidapi.com"

    def format_tweet(self, tweet):
        """
        Format a single tweet into the desired structured output.
        
        Args:
            tweet (dict): Raw tweet data.
        
        Returns:
            str: Formatted tweet as a string.
        """
        tweet_id = tweet.get("tweet_id", "N/A")
        creation_date = tweet.get("creation_date", "N/A")
        text = tweet.get("text", "N/A")
        media = tweet.get("media_url", [])
        video_urls = tweet.get("video_url", [])
        user = tweet.get("user", {})
        
        user_details = {
            "Username": user.get("username", "N/A"),
            "Name": user.get("name", "N/A"),
            "Followers": user.get("follower_count", "N/A"),
            "Following": user.get("following_count", "N/A"),
            "Location": user.get("location", "N/A"),
            "Description": user.get("description", "N/A"),
            "Profile Picture": user.get("profile_pic_url", "N/A")
        }
        
        engagements = {
            "Favorites": tweet.get("favorite_count", "N/A"),
            "Retweets": tweet.get("retweet_count", "N/A"),
            "Replies": tweet.get("reply_count", "N/A"),
            "Views": tweet.get("view_count", "N/A")
        }
        
        # Format the tweet details
        formatted_tweet = f"""
### Tweet
Tweet ID: {tweet_id}  
Creation Date: {creation_date}  
Text:  
{text}  

Media:
""" 
        for idx, media_url in enumerate(media, 1):
            formatted_tweet += f"- Media {idx}: ![Image]({media_url})\n"
        
        if video_urls:
            formatted_tweet += "\n Videos:\n"
            for video in video_urls:
                if video.get("content_type") == "video/mp4":
                    bitrate = video.get("bitrate", "N/A")
                    url = video.get("url", "N/A")
                    formatted_tweet += f"- [Quality {bitrate} kbps]({url})\n"

        formatted_tweet += "\nUser Details:\n"
        for key, value in user_details.items():
            formatted_tweet += f"- {key}: {value}\n"

        formatted_tweet += "\n Engagements: \n"
        for key, value in engagements.items():
            formatted_tweet += f"- {key}: {value}\n"

        return formatted_tweet.strip()

    def execute(self, **kwargs):
        """
        Fetch tweets based on hashtag.
        
        Args:
            kwargs (dict): Input arguments containing:
                - hashtag (str): Hashtag to search for (required)
                - api_key (str): RapidAPI key (required if not provided during init)
                - limit (int): Maximum number of tweets to fetch (default: 20)
                - section (str): Section to search in (default: 'top')
                - language (str): Language code (default: 'en')
            
        Returns:
            str: Formatted tweets.
        """
        try:
            # Getting the  parameters
            hashtag = kwargs.get("hashtag")
            if not hashtag:
                raise ValueError("Hashtag parameter is required")

            # Passsing the API in runtime 
            self.rapid_api_key = kwargs.get("api_key", self.rapid_api_key)
            if not self.rapid_api_key:
                raise ValueError("API key must be provided either during initialization or execution")

            limit = kwargs.get("limit", 20)
            section = kwargs.get("section", "top")
            language = kwargs.get("language", "en")

            # Preparing the payload
            payload = json.dumps({
                "hashtag": hashtag,
                "limit": limit,
                "section": section,
                "language": language
            })

            # Setting up  the headers
            headers = {
                'x-rapidapi-key': self.rapid_api_key,
                'x-rapidapi-host': self.rapid_api_host,
                'Content-Type': "application/json"
            }

            logger.info(f"Fetching tweets for hashtag: {hashtag}")

            # Making the request
            conn = http.client.HTTPSConnection(self.base_url)
            conn.request("POST", "/hashtag/hashtag", payload, headers)
            
            response = conn.getresponse()
            data = response.read()
            
            # Check if the request was successful
            if response.status != 200:
                raise ValueError(f"API request failed with status code {response.status}")

            result = json.loads(data.decode("utf-8"))
            tweets = result.get("results", [])
            
            # Format the tweets
            formatted_tweets = "\n\n---\n\n".join([self.format_tweet(tweet) for tweet in tweets])
            return formatted_tweets

        except Exception as e:
            logger.error(f"An error occurred while fetching tweets: {e}")
            return {"error": str(e), "status": "failed"}
        finally:
            if 'conn' in locals():
                conn.close()

    def health_check(self):
        """
        Check if the RapidAPI Twitter connection is functional.
        
        Returns:
            dict: Health status of the plugin.
        """
        try:
            logger.info("Performing RapidAPI Twitter hashtag search health check...")
            
            # Try a simple test search if API key is available
            if not self.rapid_api_key:
                return {"status": "unknown", "message": "API key not provided"}
                
            result = self.execute(
                hashtag="#test",
                api_key=self.rapid_api_key,
                limit=1
            )
            
            if "error" not in result:
                logger.info("RapidAPI Twitter hashtag search health check passed.")
                return {"status": "healthy", "message": "Twitter API service is available"}
            else:
                raise ValueError(result["error"])
            
        except Exception as e:
            logger.error(f"RapidAPI Twitter hashtag search health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
