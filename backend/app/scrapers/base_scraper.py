from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """
    Base class for all media scrapers
    """

    def __init__(self, source_name: str, source_type: str):
        self.source_name = source_name
        self.source_type = source_type
        self.last_scrape = None

    @abstractmethod
    def scrape(self) -> List[Dict]:
        """
        Main scraping method - must be implemented by subclasses
        Returns list of article dictionaries
        """
        pass

    @abstractmethod
    def parse_article(self, item: any) -> Dict:
        """
        Parse individual article from source format to standard format
        """
        pass

    def standardize_article(self, 
                          title: str,
                          content: str,
                          url: str,
                          published_date: datetime,
                          author: str = None,
                          **kwargs) -> Dict:
        """
        Convert article to standard format
        """
        return {
            'title': title,
            'content': content,
            'source_url': url,
            'source_name': self.source_name,
            'source_type': self.source_type,
            'author': author,
            'published_date': published_date,
            'crawled_date': datetime.utcnow(),
            **kwargs
        }

    def log_scrape(self, article_count: int) -> None:
        """
        Log scraping activity
        """
        self.last_scrape = datetime.utcnow()
        logger.info(f"{self.source_name}: Scraped {article_count} articles at {self.last_scrape}")
