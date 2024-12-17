from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class ResearchQuery(BaseModel):
    """Structured research query model"""
    query: str = Field(..., description="Primary search query")
    sources: List[str] = Field(
        default=['scholar', 'arxiv', 'web'], 
        description="Sources to search"
    )
    max_results: int = Field(default=10, ge=1, le=50)
    language: str = Field(default='en')
    domains: Optional[List[str]] = None
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "query": "Artificial Intelligence trends",
                "sources": ["scholar", "web"],
                "max_results": 10
            }
        }
    )

class ResearchResult(BaseModel):
    """Standardized research result model"""
    title: str
    url: HttpUrl
    source: str
    summary: Optional[str] = None
    authors: Optional[List[str]] = None
    published_date: Optional[datetime] = None
    relevance_score: Optional[float] = None

    model_config = ConfigDict(
        arbitrary_types_allowed = True,
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
    )