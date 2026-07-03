from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class ArticleCreate(BaseModel):
    title: str
    content: str
    source_url: str
    source_name: str
    source_type: str
    author: Optional[str] = None
    published_date: datetime
    keywords_matched: Optional[str] = None
    sentiment: Optional[str] = "neutral"
    priority: Optional[str] = "medium"

    class Config:
        from_attributes = True


class ArticleResponse(BaseModel):
    id: int
    title: str
    source_name: str
    source_type: str
    published_date: datetime
    sentiment: str
    priority: str
    keywords_matched: Optional[str]
    engagement_count: int
    summary: Optional[str]
    source_url: str

    class Config:
        from_attributes = True


class ArticleDetailResponse(ArticleResponse):
    content: str
    author: Optional[str]
    keyword_categories: Optional[str]
    location: Optional[str]
    language: str
    crawled_date: datetime
    is_flagged: bool
    flag_reason: Optional[str]

    class Config:
        from_attributes = True
