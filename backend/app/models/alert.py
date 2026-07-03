from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from datetime import datetime
import enum
from app.database import Base


class AlertTypeEnum(str, enum.Enum):
    KEYWORD_MATCH = "keyword_match"
    SENTIMENT_CHANGE = "sentiment_change"
    SPIKE_DETECTION = "spike_detection"
    CRITICAL_NEWS = "critical_news"
    TREND_ALERT = "trend_alert"


class AlertStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    DISMISSED = "dismissed"


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(Enum(AlertTypeEnum), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    article_id = Column(Integer, nullable=True, index=True)
    related_keywords = Column(String(500))  # JSON serialized list
    severity = Column(String(50))  # critical, high, medium, low
    status = Column(Enum(AlertStatusEnum), default=AlertStatusEnum.ACTIVE, index=True)
    created_date = Column(DateTime, default=datetime.utcnow, index=True)
    acknowledged_date = Column(DateTime)
    resolved_date = Column(DateTime)
    
    # Notification tracking
    email_sent = Column(Boolean, default=False)
    slack_sent = Column(Boolean, default=False)
    teams_sent = Column(Boolean, default=False)
    
    metadata = Column(Text)  # JSON serialized additional data

    def __repr__(self):
        return f"<Alert(id={self.id}, type={self.alert_type}, status={self.status})>"
