# Real-time Dashboard Guide

## Overview

The real-time dashboard provides live monitoring of palm oil industry media coverage with:
- **WebSocket-powered updates** - Live streaming of metrics every 5 minutes
- **Sentiment trend visualization** - Track sentiment shifts across positive/negative/neutral/mixed
- **Trending keywords** - Real-time ranking of most mentioned topics (CPO pricing, RSPO, NGO campaigns)
- **Source distribution** - Monitor coverage across national, international, and social media
- **Priority distribution** - Visual breakdown of critical/high/medium/low priority articles
- **Historical data** - Access to 24+ hours of metric history for trend analysis

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React)                         │
│  - App.jsx (main dashboard)                                 │
│  - Components: SentimentTrend, TrendingKeywords, etc        │
│  - WebSocket client for real-time updates                   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ├─── REST Endpoints ──────┐
                     │    (initial load)       │
                     │                         │
                     └─── WebSocket Endpoint ──┤
                          (live updates)       │
                                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                          │
│  - routes/dashboard.py (WebSocket & REST endpoints)         │
│  - services/realtime_aggregator.py (metric computation)     │
│  - services/websocket_manager.py (connection management)    │
└────────┬───────────────────────────────────────────────────┘
         │
         ├─── PostgreSQL ──────── articles, alerts, metrics
         │
         ├─── Redis ────────---- Celery task queue
         │
         └─── Celery Task ────── tasks/aggregation_tasks.py
              (runs every 5 min)  - Aggregates metrics
                                  - Broadcasts to WebSocket
                                  - Stores in database
```

## Backend Components

### 1. RealtimeMetric Model (`models/realtime_metric.py`)

Stores aggregated metrics in PostgreSQL for historical analysis:

```python
class RealtimeMetric(Base):
    __tablename__ = "realtime_metrics"
    
    metric_type: SENTIMENT_TREND, KEYWORD_FREQUENCY, SOURCE_DISTRIBUTION, etc
    timestamp: when the metric was computed
    data: JSON payload (e.g., {"keyword": "CPO", "count": 42})
    category: category context (e.g., "market_policy")
    window_minutes: aggregation window (e.g., 5)
```

### 2. RealtimeAggregator Service (`services/realtime_aggregator.py`)

Computes real-time metrics from article data:

```python
aggregator = RealtimeAggregator(db, window_minutes=5)

# Individual aggregations
sentiment_trend = aggregator.aggregate_sentiment_trend()
keywords = aggregator.aggregate_keyword_frequency(limit=15)
sources = aggregator.aggregate_source_distribution()
priorities = aggregator.aggregate_priority_distribution()

# All at once
all_metrics = aggregator.aggregate_all_metrics()

# Store & retrieve
aggregator.store_metrics(all_metrics)
history = aggregator.get_metric_history("sentiment_trend", hours_back=24)
```

### 3. WebSocketManager (`services/websocket_manager.py`)

Manages WebSocket connections and broadcasting:

```python
manager = WebSocketManager()

# Lifecycle
await manager.connect(websocket)
manager.disconnect(websocket)

# Broadcasting
await manager.broadcast({"type": "metrics_update", "metrics": [...]})

# Send to specific client
await manager.send_personal(websocket, {"type": "pong"})
```

### 4. Celery Tasks (`tasks/aggregation_tasks.py`)

Scheduled periodic tasks:

```python
@shared_task
def aggregate_and_broadcast_metrics():
    """Runs every 5 minutes"""
    # 1. Compute all metrics
    # 2. Store in database
    # 3. Broadcast to WebSocket clients

@shared_task
def cleanup_old_metrics(days_to_keep=7):
    """Runs daily"""
    # Archive metrics older than retention period
```

## Frontend Components

### 1. App.jsx (Main Dashboard)

- Fetches initial metrics on load
- Establishes WebSocket connection
- Renders metric components
- Updates state on WebSocket messages

### 2. Component Tree

```
App.jsx
├── Dashboard.jsx (header & info)
├── SentimentTrend.jsx (sentiment distribution over time)
├── TrendingKeywords.jsx (top keywords ranked)
├── SourceDistribution.jsx (coverage by source type)
└── PriorityDistribution.jsx (articles by priority level)
```

## API Endpoints

### REST Endpoints (HTTP GET)

```
GET /api/dashboard/metrics/current
  - Returns current snapshot of all metrics
  - Used for initial dashboard load
  Response: {
    "timestamp": "2024-01-15T10:30:00Z",
    "sentiment_trend": {...},
    "trending_keywords": [...],
    "source_distribution": [...],
    "priority_distribution": [...]
  }

GET /api/dashboard/metrics/sentiment?hours_back=24
  - Historical sentiment trend data for charting

GET /api/dashboard/metrics/keywords?hours_back=24
  - Historical trending keywords

GET /api/dashboard/metrics/sources?hours_back=24
  - Historical source distribution

GET /api/dashboard/metrics/priorities?hours_back=24
  - Historical priority distribution
```

### WebSocket Endpoint

```
WS /api/dashboard/ws/metrics
  - Subscribe to real-time metric updates
  - Client message: {"type": "subscribe", "metric_type": "all"}
  - Server broadcast: {
      "type": "metrics_update",
      "metrics": [
        {"type": "sentiment_trend", "data": {...}},
        {"type": "keyword_frequency", "data": [...]},
        ...
      ]
    }
```

## Setup & Deployment

### Backend Setup

1. **Add to main.py**
   ```python
   from app.api.routes import dashboard
   app.include_router(dashboard.router)
   ```

2. **Run migrations**
   ```bash
   alembic revision --autogenerate -m "Add realtime_metrics table"
   alembic upgrade head
   ```

3. **Start Celery worker**
   ```bash
   celery -A app.tasks.aggregation_tasks worker --loglevel=info --beat
   ```

4. **Start FastAPI**
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server**
   ```bash
   npm start
   ```
   Opens http://localhost:3000

### Docker Setup

```bash
# Add to docker-compose.yml
services:
  celery-worker:
    build:
      context: ./backend
    command: celery -A app.tasks.aggregation_tasks worker --loglevel=info --beat
    environment:
      DATABASE_URL: postgresql://media_user:media_password@postgres:5432/media_monitoring
      REDIS_URL: redis://redis:6379/0
    depends_on:
      - postgres
      - redis

  frontend:
    build:
      context: ./frontend
    ports:
      - "3000:3000"
    environment:
      REACT_APP_API_URL: http://localhost:8000
```

## Example: Monitoring CPO Pricing vs Sentiment

1. **Articles are scraped** from media sources mentioning "Harga CPO", "CPO price", etc.

2. **Every 5 minutes, Celery task runs:**
   ```python
   # Compute sentiment distribution
   - Positive (e.g., "CPO prices up") → count
   - Negative (e.g., "CPO prices crash") → count
   
   # Compute trending keywords
   - "Harga CPO" → 87 mentions
   - "ekspor sawit" → 42 mentions
   - "BPDPKS" → 28 mentions
   ```

3. **Metrics are stored in database:**
   ```python
   RealtimeMetric(
     metric_type="sentiment_trend",
     data={"2024-01-15T10:30:00": {"positive": 8, "negative": 15}},
     timestamp="2024-01-15T10:35:00"
   )
   ```

4. **WebSocket broadcasts to clients:**
   ```javascript
   // Frontend receives real-time update
   {
     "type": "metrics_update",
     "metrics": [
       {
         "type": "sentiment_trend",
         "data": {...}
       }
     ]
   }
   ```

5. **Dashboard visualizes:**
   - Sentiment chart shows trend over last hour
   - Trending keywords show CPO ranks #1 with 87 mentions
   - Negative sentiment spike = CRITICAL alert

## Performance Considerations

- **Metric aggregation:** O(n) where n = articles in last 24h (typically <10K)
- **WebSocket broadcast:** O(m) where m = connected clients (typically <100)
- **Database storage:** ~5KB per metric update × 288 per day = ~1.4MB/day
- **Data retention:** 7-day default keeps ~10MB per 1000 daily updates

## Customization

### Change Aggregation Interval

In `tasks/aggregation_tasks.py`:
```python
# Change from 5 to 15 minutes
aggregator = RealtimeAggregator(db, window_minutes=15)
```

### Add Custom Metrics

1. Add to `MetricTypeEnum` in `models/realtime_metric.py`
2. Add method to `RealtimeAggregator` class
3. Call in `aggregate_all_metrics()`

### Filter by Category

In any component, add filter:
```python
# Only show CPO-related keywords
keywords = [kw for kw in trending if "CPO" in kw["keyword"]]
```

## Troubleshooting

**WebSocket not connecting:**
- Check CORS settings in `app.main.py`
- Verify WebSocket URL matches your deployment host
- Check browser console for connection errors

**Metrics not updating:**
- Verify Celery worker is running: `celery inspect active`
- Check Redis is accessible: `redis-cli ping`
- Check PostgreSQL database has `realtime_metrics` table

**High memory usage:**
- Reduce data retention: `cleanup_old_metrics(days_to_keep=3)`
- Increase aggregation window: `window_minutes=15`
- Archive old metrics more frequently

## Future Enhancements

- [ ] Add ChartJS/Recharts for interactive graphs
- [ ] Real-time alert notifications when thresholds exceeded
- [ ] Custom metric definitions (user-configured)
- [ ] Export to CSV/PDF
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Mobile-responsive improvements