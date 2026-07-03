# API Documentation

## Base URL

```
http://localhost:8000/api
```

## Endpoints

### Articles

#### List Articles

```
GET /api/articles
```

**Query Parameters:**
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10, max=100): Number of results
- `source_type` (string, optional): Filter by source type
- `sentiment` (string, optional): Filter by sentiment (positive, negative, neutral, mixed)
- `priority` (string, optional): Filter by priority (critical, high, medium, low)
- `days_back` (int, default=7): Number of days to look back
- `keyword` (string, optional): Filter by keyword

**Response:**

```json
[
  {
    "id": 1,
    "title": "Article Title",
    "source_name": "kompas.com",
    "source_type": "national_media",
    "published_date": "2024-01-15T10:30:00Z",
    "sentiment": "negative",
    "priority": "high",
    "keywords_matched": "CPO, ekspor sawit",
    "engagement_count": 150,
    "summary": "Article summary...",
    "source_url": "https://kompas.com/article"
  }
]
```

#### Get Article Details

```
GET /api/articles/{article_id}
```

**Response:** Full article object with content and metadata

#### Get Daily Statistics

```
GET /api/articles/stats/daily
```

**Query Parameters:**
- `days` (int, default=7): Number of days to analyze

**Response:**

```json
[
  {
    "date": "2024-01-15",
    "total": 42,
    "positive": 8,
    "negative": 15
  }
]
```

#### Get Trending Keywords

```
GET /api/articles/trending/keywords
```

**Query Parameters:**
- `limit` (int, default=10): Number of keywords to return
- `days` (int, default=7): Analysis period in days

**Response:**

```json
[
  {
    "keyword": "CPO",
    "count": 150
  },
  {
    "keyword": "ekspor sawit",
    "count": 142
  }
]
```

### Alerts

#### List Alerts

```
GET /api/alerts
```

**Query Parameters:**
- `skip` (int, default=0): Pagination offset
- `limit` (int, default=10): Number of results
- `status` (string, optional): Filter by status (active, acknowledged, resolved, dismissed)
- `severity` (string, optional): Filter by severity (critical, high, medium, low)
- `days_back` (int, default=7): Analysis period

#### Get Alert Details

```
GET /api/alerts/{alert_id}
```

#### Acknowledge Alert

```
PUT /api/alerts/{alert_id}/acknowledge
```

**Response:**

```json
{
  "message": "Alert acknowledged",
  "alert_id": 1
}
```

#### Resolve Alert

```
PUT /api/alerts/{alert_id}/resolve
```

**Response:**

```json
{
  "message": "Alert resolved",
  "alert_id": 1
}
```

## Error Responses

### 404 Not Found

```json
{
  "detail": "Article not found"
}
```

### 400 Bad Request

```json
{
  "detail": "Invalid query parameters"
}
```

## Rate Limiting

API endpoints are rate-limited to 100 requests per minute per IP address.

## Authentication

Currently, the API is open access. For production deployment, implement API key authentication.
