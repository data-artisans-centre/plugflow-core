class ResearchAgentError(Exception):
    """Base exception for Research Agent"""
    pass

class SearchError(ResearchAgentError):
    """Exception raised for search-related errors"""
    pass

class ExtractionError(ResearchAgentError):
    """Exception raised for content extraction errors"""
    pass

class SummarizationError(ResearchAgentError):
    """Exception raised for summarization-related errors"""
    pass