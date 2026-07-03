from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Enum, Index
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class SentimentEnum(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class PriorityEnum(str, enum.Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SourceTypeEnum(str, enum.Enum):
    NATIONAL_MEDIA = "national_media"
    REGIONAL_MEDIA = "regional_media"
    INTERNATIONAL_MEDIA = "international_media"
    JOURNAL = "journal"
    SOCIAL_MEDIA_LINKEDIN = "social_media_linkedin"
    SOCIAL_MEDIA_FACEBOOK = "social_media_facebook"
    SOCIAL_MEDIA_INSTAGRAM = "social_media_instagram"


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    source_url = Column(String(1000), nullable=False, unique=True, index=True)
    source_name = Column(String(255), nullable=False, index=True)
    source_type = Column(Enum(SourceTypeEnum), nullable=False, index=True)
    author = Column(String(255))
    published_date = Column(DateTime, nullable=False, index=True)
    crawled_date = Column(DateTime, default=datetime.utcnow, index=True)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Content Analysis
    summary = Column(Text)
    keywords_matched = Column(String(1000))  # JSON serialized list
    keyword_categories = Column(String(500))  # JSON serialized list
    
    # Sentiment & Priority
    sentiment = Column(Enum(SentimentEnum), default=SentimentEnum.NEUTRAL, index=True)
    sentiment_score = Column(Float)  # -1.0 to 1.0
    priority = Column(Enum(PriorityEnum), default=PriorityEnum.MEDIUM, index=True)
    
    # Geographic Information
    country = Column(String(100), index=True)
    region = Column(String(100))
    location = Column(String(255))
    
    # Flags
    is_relevant = Column(Boolean, default=True, index=True)
    is_processed = Column(Boolean, default=False, index=True)
    is_flagged = Column(Boolean, default=False)
    flag_reason = Column(Text)
    
    # Engagement (for social media)
    engagement_count = Column(Integer, default=0)
    share_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    
    # Media specific fields
    language = Column(String(10), default="id", index=True)
    
    # Create indexes for common queries
    __table_args__ = (
        Index('idx_source_published', 'source_name', 'published_date'),
        Index('idx_sentiment_priority', 'sentiment', 'priority'),
        Index('idx_keyword_category', 'keyword_categories'),
    )

    def __repr__(self):
        return f"<Article(id={self.id}, title={self.title[:50]}..., source={self.source_name})>"
