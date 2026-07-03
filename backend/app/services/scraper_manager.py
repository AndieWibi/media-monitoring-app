from typing import List, Dict, Optional
from datetime import datetime
import logging
from app.scrapers.base_scraper import BaseScraper

logger = logging.getLogger(__name__)


class ScraperManager:
    """
    Manages multiple media scrapers and coordinates data collection
    """

    def __init__(self):
        self.scrapers: Dict[str, BaseScraper] = {}
        self.scrape_history = []

    def register_scraper(self, name: str, scraper: BaseScraper) -> None:
        """
        Register a new scraper
        """
        self.scrapers[name] = scraper
        logger.info(f"Registered scraper: {name}")

    def scrape_all(self) -> List[Dict]:
        """
        Execute all registered scrapers and collect articles
        """
        articles = []
        
        for name, scraper in self.scrapers.items():
            try:
                logger.info(f"Starting scraper: {name}")
                scraper_articles = scraper.scrape()
                articles.extend(scraper_articles)
                logger.info(f"Completed scraper: {name}, collected {len(scraper_articles)} articles")
            except Exception as e:
                logger.error(f"Error in scraper {name}: {str(e)}")
                continue
        
        self.scrape_history.append({
            'timestamp': datetime.utcnow(),
            'total_articles': len(articles),
            'scrapers_run': len(self.scrapers)
        })
        
        return articles

    def scrape_source(self, source_name: str) -> Optional[List[Dict]]:
        """
        Execute a specific scraper by source name
        """
        if source_name not in self.scrapers:
            logger.warning(f"Scraper not found: {source_name}")
            return None
        
        try:
            return self.scrapers[source_name].scrape()
        except Exception as e:
            logger.error(f"Error scraping {source_name}: {str(e)}")
            return None

    def get_scraper_status(self) -> Dict:
        """
        Get status of all registered scrapers
        """
        return {
            'total_scrapers': len(self.scrapers),
            'scraper_names': list(self.scrapers.keys()),
            'last_scrape': self.scrape_history[-1] if self.scrape_history else None
        }
