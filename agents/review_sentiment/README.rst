YouTube Review Analyzer
=======================

Overview
--------
The `YouTube Review Analyzer` is a Python package designed to analyze YouTube comments for sentiment, readability, and other metrics. It uses a combination of natural language processing and custom algorithms to generate insights into the tone and readability of comments.

Features
--------
- **Sentiment Analysis**: Computes polarity (negative to positive sentiment) and subjectivity (factual to opinion-based content) using `TextBlob`.
- **Custom Readability Scoring**: Implements a custom Flesch Reading Ease-like score to measure comment readability.
- **Comment Metrics**: Evaluates comment length and other statistical features.
- **Pydantic Validation**: Ensures structured and validated output using Pydantic models.
- **Health Check**: Includes a built-in health check for system diagnostics.

Installation
------------
Install the package using `pip`:

.. code-block:: bash

    pip install youtube-review-analyzer

Usage
-----
### Example: Analyzing Comments
The `YouTubeReviewAnalyzer` can analyze a single comment or a list of comments. Below is an example of how to use the package:

.. code-block:: python

    from youtube_review_analyzer import YouTubeReviewAnalyzer

    analyzer = YouTubeReviewAnalyzer()
    
    # Analyze a single comment
    comment_analysis = analyzer.analyze_comment("This video is fantastic!")
    print(comment_analysis)

    # Process multiple comments
    sample_comments = [
        {
            "author": "User1",
            "comment": "Amazing content, very helpful!",
            "likes": 15,
            "time": "1 day ago"
        },
        {
            "author": "User2",
            "comment": "I found this difficult to follow.",
            "likes": 5,
            "time": "3 days ago"
        }
    ]
    results = analyzer.process_comments(sample_comments)
    print(results)

### Fetching Comments from YouTube
The `execute` method simulates fetching and analyzing comments for a given YouTube video:

.. code-block:: python

    results = analyzer.execute(video_url="https://www.youtube.com/watch?v=example", max_comments=10)
    print(results)

Modules and Classes
-------------------
### `CommentAnalysis`
A Pydantic model representing the analysis results for a single comment.

- **Fields**:
  - `comment`: The text of the comment.
  - `sentiment_polarity`: Sentiment polarity (-1 to 1).
  - `sentiment_subjectivity`: Subjectivity (0 to 1).
  - `readability_score`: Custom readability score (0 to 100).
  - `review_length`: The number of words in the comment.

### `ReadabilityScorer`
Calculates a custom readability score inspired by Flesch Reading Ease.

- **Methods**:
  - `calculate_flesch_reading_ease(text: str)`: Returns the readability score for a given text.

### `YouTubeReviewAnalyzer`
The main class for comment analysis.

- **Methods**:
  - `analyze_comment(comment_text: str)`: Analyzes a single comment.
  - `process_comments(comments_data: List[Dict])`: Processes a list of comments.
  - `execute(video_url: str, max_comments: int = 10)`: Fetches and analyzes comments for a video.
  - `health_check()`: Checks the system's operational status.

Logging
-------
This package uses a custom logger to track activity and errors. Logs are written to a file or console depending on configuration.

Contributing
------------
Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

License
-------
This project is licensed under the MIT License.
