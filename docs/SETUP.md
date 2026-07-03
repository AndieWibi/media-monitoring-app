# Setup and Installation Guide

## Prerequisites

- Docker and Docker Compose
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Elasticsearch 8+

## Quick Start with Docker

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/media-monitoring-app.git
cd media-monitoring-app
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Elasticsearch search engine
- FastAPI backend

### 4. Initialize Database

```bash
docker-compose exec backend python -m app.database init_db
```

### 5. Access the Application

- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Local Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Database

Make sure PostgreSQL is running and update `.env`:

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/media_monitoring
```

### 4. Run Migrations

```bash
alembic upgrade head
```

### 5. Start Backend Server

```bash
uvicorn app.main:app --reload
```

## Configuration

### Keywords Configuration

Edit `config/keywords.json` to customize monitoring keywords.

### Scraper Configuration

Configure specific scrapers in `backend/app/scrapers/` directory.

## Running Tests

```bash
pytest backend/tests/ -v --cov=app
```

## Deployment

For production deployment, see [DEPLOYMENT.md](./DEPLOYMENT.md)
