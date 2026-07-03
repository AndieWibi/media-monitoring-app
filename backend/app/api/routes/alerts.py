from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.models.alert import Alert, AlertStatusEnum
from app.schemas.alert import AlertResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    severity: Optional[str] = None,
    days_back: int = Query(7, ge=1),
    db: Session = Depends(get_db)
):
    """
    Get alerts with optional filtering
    """
    query = db.query(Alert)
    
    # Date filter
    cutoff_date = datetime.utcnow() - timedelta(days=days_back)
    query = query.filter(Alert.created_date >= cutoff_date)
    
    # Status filter
    if status:
        query = query.filter(Alert.status == status)
    
    # Severity filter
    if severity:
        query = query.filter(Alert.severity == severity)
    
    query = query.order_by(Alert.created_date.desc())
    alerts = query.offset(skip).limit(limit).all()
    
    return alerts


@router.get("/{alert_id}", response_model=AlertResponse)
def get_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Get specific alert by ID
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return alert


@router.put("/{alert_id}/acknowledge")
def acknowledge_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Mark alert as acknowledged
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = AlertStatusEnum.ACKNOWLEDGED
    alert.acknowledged_date = datetime.utcnow()
    db.commit()
    
    return {"message": "Alert acknowledged", "alert_id": alert_id}


@router.put("/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    """
    Mark alert as resolved
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.status = AlertStatusEnum.RESOLVED
    alert.resolved_date = datetime.utcnow()
    db.commit()
    
    return {"message": "Alert resolved", "alert_id": alert_id}
