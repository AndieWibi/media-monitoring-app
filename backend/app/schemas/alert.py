from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AlertCreate(BaseModel):
    alert_type: str
    title: str
    description: str
    article_id: Optional[int] = None
    severity: str
    related_keywords: Optional[str] = None

    class Config:
        from_attributes = True


class AlertResponse(BaseModel):
    id: int
    alert_type: str
    title: str
    description: str
    severity: str
    status: str
    created_date: datetime
    related_keywords: Optional[str]

    class Config:
        from_attributes = True
