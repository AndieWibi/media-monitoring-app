from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.realtime_aggregator import RealtimeAggregator
from app.services.websocket_manager import manager
import json
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.websocket("/ws/metrics")
async def websocket_metrics_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time metrics streaming
    
    Client connects and receives continuous updates of:
    - Sentiment trends
    - Keyword frequencies
    - Source distributions
    - Priority distributions
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Receive client messages (heartbeat, subscribe to specific metrics, etc.)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message.get("type") == "ping":
                await manager.send_personal(websocket, {"type": "pong"})
            elif message.get("type") == "subscribe":
                # Client can subscribe to specific metric types
                metric_type = message.get("metric_type")
                logger.info(f"Client subscribed to {metric_type}")
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket disconnected")


@router.get("/metrics/current")
def get_current_metrics(db: Session = Depends(get_db)):
    """
    GET current snapshot of all metrics
    Useful for initial dashboard load
    """
    aggregator = RealtimeAggregator(db, window_minutes=5)
    
    metrics = {
        "timestamp": aggregator.aggregate_sentiment_trend()["timestamp"],
        "sentiment_trend": aggregator.aggregate_sentiment_trend(),
        "trending_keywords": aggregator.aggregate_keyword_frequency(limit=15),
        "source_distribution": aggregator.aggregate_source_distribution(),
        "priority_distribution": aggregator.aggregate_priority_distribution()
    }
    
    return metrics


@router.get("/metrics/sentiment")
def get_sentiment_history(
    hours_back: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Get historical sentiment trend data for charting
    """
    aggregator = RealtimeAggregator(db)
    history = aggregator.get_metric_history(
        metric_type="sentiment_trend",
        hours_back=hours_back,
        limit=hours_back * 12  # 5-min intervals
    )
    
    return {
        "metric_type": "sentiment_trend",
        "hours_back": hours_back,
        "data": history
    }


@router.get("/metrics/keywords")
def get_keywords_history(
    hours_back: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Get historical trending keywords data
    """
    aggregator = RealtimeAggregator(db)
    history = aggregator.get_metric_history(
        metric_type="keyword_frequency",
        hours_back=hours_back,
        limit=hours_back * 12
    )
    
    return {
        "metric_type": "keyword_frequency",
        "hours_back": hours_back,
        "data": history
    }


@router.get("/metrics/sources")
def get_sources_history(
    hours_back: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Get historical source distribution data
    """
    aggregator = RealtimeAggregator(db)
    history = aggregator.get_metric_history(
        metric_type="source_distribution",
        hours_back=hours_back,
        limit=hours_back * 12
    )
    
    return {
        "metric_type": "source_distribution",
        "hours_back": hours_back,
        "data": history
    }


@router.get("/metrics/priorities")
def get_priorities_history(
    hours_back: int = Query(24, ge=1, le=168),
    db: Session = Depends(get_db)
):
    """
    Get historical priority distribution data
    """
    aggregator = RealtimeAggregator(db)
    history = aggregator.get_metric_history(
        metric_type="priority_distribution",
        hours_back=hours_back,
        limit=hours_back * 12
    )
    
    return {
        "metric_type": "priority_distribution",
        "hours_back": hours_back,
        "data": history
    }
