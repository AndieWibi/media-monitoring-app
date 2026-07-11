import json
from datetime import datetime, timedelta
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from app.models.article import Article, SentimentEnum, SourceTypeEnum
from app.models.realtime_metric import RealtimeMetric, MetricTypeEnum
import logging

logger = logging.getLogger(__name__)


class RealtimeAggregator:
    """
    Service for computing real-time metrics for dashboard display
    Aggregates data from articles and alerts at configurable intervals
    """

    def __init__(self, db: Session, window_minutes: int = 5):
        self.db = db
        self.window_minutes = window_minutes

    def aggregate_sentiment_trend(self) -> dict:
        """
        Get sentiment distribution over the last hour (5-min intervals)
        Returns: List of sentiment counts grouped by time windows
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        
        # Query articles grouped by 5-minute windows
        results = self.db.query(
            func.date_trunc(f'{self.window_minutes} minutes', Article.published_date).label('time_bucket'),
            Article.sentiment,
            func.count(Article.id).label('count')
        ).filter(
            Article.published_date >= cutoff_time,
            Article.is_relevant == True
        ).group_by(
            func.date_trunc(f'{self.window_minutes} minutes', Article.published_date),
            Article.sentiment
        ).all()

        # Organize data
        sentiment_data = {}
        for row in results:
            time_key = row[0].isoformat() if row[0] else None
            sentiment = row[1].value if row[1] else "unknown"
            count = row[2]
            
            if time_key not in sentiment_data:
                sentiment_data[time_key] = {}
            sentiment_data[time_key][sentiment] = count

        return {
            "type": MetricTypeEnum.SENTIMENT_TREND.value,
            "timestamp": datetime.utcnow().isoformat(),
            "data": sentiment_data,
            "window_minutes": self.window_minutes
        }

    def aggregate_keyword_frequency(self, limit: int = 15, hours_back: int = 24) -> dict:
        """
        Get top trending keywords from recent articles
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        articles = self.db.query(Article.keywords_matched).filter(
            Article.published_date >= cutoff_time,
            Article.is_relevant == True,
            Article.keywords_matched != None
        ).all()

        keyword_freq = {}
        for article in articles:
            if article.keywords_matched:
                keywords = [kw.strip() for kw in article.keywords_matched.split(',')]
                for kw in keywords:
                    keyword_freq[kw] = keyword_freq.get(kw, 0) + 1

        # Sort and limit
        sorted_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        return {
            "type": MetricTypeEnum.KEYWORD_FREQUENCY.value,
            "timestamp": datetime.utcnow().isoformat(),
            "data": [{"keyword": kw, "count": count} for kw, count in sorted_keywords],
            "hours_back": hours_back
        }

    def aggregate_source_distribution(self) -> dict:
        """
        Distribution of articles by source type
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        results = self.db.query(
            Article.source_type,
            func.count(Article.id).label('count')
        ).filter(
            Article.published_date >= cutoff_time,
            Article.is_relevant == True
        ).group_by(
            Article.source_type
        ).all()

        data = [{"source": row[0].value, "count": row[1]} for row in results]
        
        return {
            "type": MetricTypeEnum.SOURCE_DISTRIBUTION.value,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }

    def aggregate_priority_distribution(self) -> dict:
        """
        Distribution of articles by priority level
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        
        results = self.db.query(
            Article.priority,
            func.count(Article.id).label('count')
        ).filter(
            Article.published_date >= cutoff_time,
            Article.is_relevant == True
        ).group_by(
            Article.priority
        ).all()

        data = [{"priority": row[0].value, "count": row[1]} for row in results]
        
        return {
            "type": MetricTypeEnum.PRIORITY_DISTRIBUTION.value,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }

    def aggregate_all_metrics(self) -> list:
        """
        Compute all metrics at once
        Returns list of metric dicts ready for storage or WebSocket broadcast
        """
        metrics = []
        
        try:
            metrics.append(self.aggregate_sentiment_trend())
            metrics.append(self.aggregate_keyword_frequency())
            metrics.append(self.aggregate_source_distribution())
            metrics.append(self.aggregate_priority_distribution())
            
            logger.info(f"Aggregated {len(metrics)} realtime metrics")
        except Exception as e:
            logger.error(f"Error aggregating metrics: {str(e)}")

        return metrics

    def store_metrics(self, metrics: list) -> None:
        """
        Store computed metrics in database for historical analysis
        """
        try:
            for metric_data in metrics:
                metric = RealtimeMetric(
                    metric_type=metric_data['type'],
                    data=json.dumps(metric_data['data']),
                    window_minutes=metric_data.get('window_minutes', self.window_minutes)
                )
                self.db.add(metric)
            
            self.db.commit()
            logger.info(f"Stored {len(metrics)} metrics to database")
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error storing metrics: {str(e)}")

    def get_metric_history(self, metric_type: str, hours_back: int = 24, limit: int = 288) -> list:
        """
        Retrieve historical metrics for charting (5-min intervals = 288 per day)
        """
        cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
        
        results = self.db.query(RealtimeMetric).filter(
            RealtimeMetric.metric_type == metric_type,
            RealtimeMetric.timestamp >= cutoff_time,
            RealtimeMetric.is_archived == False
        ).order_by(
            RealtimeMetric.timestamp.asc()
        ).limit(limit).all()

        return [
            {
                "timestamp": m.timestamp.isoformat(),
                "data": json.loads(m.data),
                "metric_type": m.metric_type
            }
            for m in results
        ]