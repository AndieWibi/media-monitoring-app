import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/media_monitoring"
)

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Elasticsearch
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")

# API Keys
LINKEDIN_API_KEY = os.getenv("LINKEDIN_API_KEY")
FACEBOOK_API_KEY = os.getenv("FACEBOOK_API_KEY")
INSTAGRAM_API_KEY = os.getenv("INSTAGRAM_API_KEY")

# Notification
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Application
APP_NAME = "Media Monitoring Platform"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "False") == "True"

# Keywords config
KEYWORDS_CONFIG = "config/keywords.json"

# Scraping
SCRAPE_INTERVAL_MINUTES = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "60"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
