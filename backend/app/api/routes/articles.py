from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models.article import Article, SentimentEnum, PriorityEnum, SourceTypeEnum
from app.schemas.article import ArticleResponse, ArticleCreate
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/articles", tags=["articles"])


@router.get("/", response_model=List[ArticleResponse])
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    source_type: Optional[str] = None,
    sentiment: Optional[str] = None,
    priority: Optional[str] = None,
    days_back: int = Query(7, ge=1),
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get articles with optional filtering
    """
    query = db.query(Article)
    
    # Date filter
    cutoff_date = datetime.utcnow() - timedelta(days=days_back)
    query = query.filter(Article.published_date >= cutoff_date)
    
    # Source type filter
    if source_type:
        query = query.filter(Article.source_type == source_type)
    
    # Sentiment filter
    if sentiment:
        query = query.filter(Article.sentiment == sentiment)
    
    # Priority filter
    if priority:
        query = query.filter(Article.priority == priority)
    
    # Keyword filter
    if keyword:
        query = query.filter(Article.keywords_matched.contains(keyword))
    
    # Relevance filter
    query = query.filter(Article.is_relevant == True)
    
    # Sort by published date descending
    query = query.order_by(Article.published_date.desc())
    
    total = query.count()
    articles = query.offset(skip).limit(limit).all()
    
    return articles


@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(article_id: int, db: Session = Depends(get_db)):
    """
    Get specific article by ID
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/stats/daily")
def get_daily_stats(
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get daily article statistics
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    stats = db.query(
        Article.published_date.cast(Date).label('date'),
        func.count(Article.id).label('total'),
        func.sum(case([(Article.sentiment == 'positive', 1)], else_=0)).label('positive'),
        func.sum(case([(Article.sentiment == 'negative', 1)], else_=0)).label('negative'),
    ).filter(
        Article.published_date >= cutoff_date,
        Article.is_relevant == True
    ).group_by(
        Article.published_date.cast(Date)
    ).all()
    
    return [{"date": str(s[0]), "total": s[1], "positive": s[2], "negative": s[3]} for s in stats]


@router.get("/trending/keywords")
def get_trending_keywords(
    limit: int = Query(10, ge=1, le=50),
    days: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db)
):
    """
    Get trending keywords from recent articles
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    articles = db.query(Article.keywords_matched).filter(
        Article.published_date >= cutoff_date,
        Article.is_relevant == True
    ).all()
    
    keyword_freq = {}
    for article in articles:
        if article.keywords_matched:
            keywords = article.keywords_matched.split(',')
            for kw in keywords:
                kw = kw.strip()
                keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
    
    sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:limit]
    return [{"keyword": kw, "count": count} for kw, count in sorted_keywords]
