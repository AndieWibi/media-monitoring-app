from celery import shared_task
from app.database import SessionLocal
from app.services.realtime_aggregator import RealtimeAggregator
from app.services.websocket_manager import manager
import logging
import asyncio
import json

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def aggregate_and_broadcast_metrics(self):
    """
    Periodic task (every 5 minutes) to:
    1. Compute all real-time metrics
    2. Store in database
    3. Broadcast to WebSocket clients
    """
    db = SessionLocal()
    
    try:
        aggregator = RealtimeAggregator(db, window_minutes=5)
        
        # Compute all metrics
        metrics = aggregator.aggregate_all_metrics()
        
        # Store metrics for historical analysis
        aggregator.store_metrics(metrics)
        
        # Prepare broadcast payload
        broadcast_data = {
            "type": "metrics_update",
            "metrics": metrics
        }
        
        # Broadcast to all connected WebSocket clients
        # Note: asyncio.run() needed since Celery tasks are synchronous
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        loop.run_until_complete(manager.broadcast(broadcast_data))
        
        logger.info("Metrics aggregated, stored, and broadcasted successfully")
        
    except Exception as e:
        logger.error(f"Error in aggregation task: {str(e)}")
        raise
    finally:
        db.close()


@shared_task(bind=True)
def cleanup_old_metrics(self, days_to_keep: int = 7):
    """
    Periodic task (daily) to archive old metrics beyond retention period
    Keeps database size manageable while maintaining historical data
    """
    db = SessionLocal()
    
    try:
        from datetime import datetime, timedelta
        from app.models.realtime_metric import RealtimeMetric
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        # Mark old metrics as archived
        db.query(RealtimeMetric).filter(
            RealtimeMetric.timestamp < cutoff_date,
            RealtimeMetric.is_archived == False
        ).update({"is_archived": True})
        
        db.commit()
        
        logger.info(f"Archived metrics older than {days_to_keep} days")
        
    except Exception as e:
        logger.error(f"Error in cleanup task: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()