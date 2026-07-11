from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum
from datetime import datetime
import enum
from app.database import Base


class MetricTypeEnum(str, enum.Enum):
    SENTIMENT_TREND = "sentiment_trend"
    KEYWORD_FREQUENCY = "keyword_frequency"
    SOURCE_DISTRIBUTION = "source_distribution"
    PRIORITY_DISTRIBUTION = "priority_distribution"
    ALERT_COUNT = "alert_count"


class RealtimeMetric(Base):
    __tablename__ = "realtime_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_type = Column(Enum(MetricTypeEnum), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Data payload (JSON serialized)
    data = Column(Text, nullable=False)  # JSON: {"keyword": "CPO", "count": 42, ...}
    
    # Category/keyword context
    category = Column(String(255), index=True)  # e.g., "market_policy", "sustainability_environmental"
    keyword = Column(String(255), index=True)   # e.g., "Harga CPO", "RSPO"
    
    # Sentiment context
    sentiment = Column(String(50))  # "positive", "negative", "neutral", "mixed"
    
    # Aggregation window
    window_minutes = Column(Integer, default=5)  # 5-min, 15-min, hourly aggregations
    
    # Cleanup flag
    is_archived = Column(String(50), default=False)

    def __repr__(self):
        return f"<RealtimeMetric(id={self.id}, type={self.metric_type}, timestamp={self.timestamp})>"