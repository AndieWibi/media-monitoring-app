import json
import re
from typing import List, Dict, Tuple
from app.config import KEYWORDS_CONFIG


class KeywordMatcher:
    """
    Advanced keyword matching service with support for:
    - Boolean operators (AND, OR, NOT)
    - Phrase matching
    - Context-aware matching
    - Exclusion lists
    """

    def __init__(self, config_path: str = "config/keywords.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.keywords = self.config['monitoring_keywords']

    def is_relevant(self, text: str, title: str = "") -> Tuple[bool, List[str], List[str]]:
        """
        Determine if text is relevant based on keyword matching
        Returns: (is_relevant, matched_keywords, matched_categories)
        """
        combined_text = f"{title} {text}".lower()
        matched_keywords = []
        matched_categories = []

        for category, config in self.keywords.items():
            if self._matches_category(combined_text, config, category):
                matched_categories.append(category)
                matched_keywords.extend(self._extract_matched_keywords(combined_text, config))

        # Check exclusions
        if self._contains_exclusions(combined_text):
            return False, [], []

        is_relevant = len(matched_categories) > 0
        return is_relevant, list(set(matched_keywords)), matched_categories

    def _matches_category(self, text: str, config: Dict, category: str) -> bool:
        """
        Check if text matches the category pattern
        Logic: At least one keyword AND at least one context keyword
        """
        has_keyword = any(
            self._keyword_exists(text, kw)
            for kw in config.get('keywords', [])
        )
        
        has_context = any(
            self._keyword_exists(text, ctx)
            for ctx in config.get('context_keywords', [])
        )
        
        return has_keyword and has_context

    def _keyword_exists(self, text: str, keyword: str) -> bool:
        """
        Check if keyword exists in text with word boundaries
        """
        keyword_lower = keyword.lower()
        pattern = r'\b' + re.escape(keyword_lower) + r'\b'
        return re.search(pattern, text) is not None

    def _extract_matched_keywords(self, text: str, config: Dict) -> List[str]:
        """
        Extract all matched keywords from text
        """
        matched = []
        for keyword in config.get('keywords', []):
            if self._keyword_exists(text, keyword):
                matched.append(keyword)
        return matched

    def _contains_exclusions(self, text: str) -> bool:
        """
        Check if text contains exclusion keywords
        """
        exclusions = set()
        for config in self.keywords.values():
            exclusions.update(config.get('exclude_keywords', []))
        
        for exclusion in exclusions:
            if self._keyword_exists(text, exclusion):
                return True
        return False

    def extract_phrases(self, text: str, num_phrases: int = 5) -> List[str]:
        """
        Extract key phrases from text
        """
        # Simple implementation - can be enhanced with NLP
        sentences = text.split('.')
        phrases = [s.strip() for s in sentences if len(s.strip()) > 20][:num_phrases]
        return phrases

    def get_priority(self, matched_categories: List[str], sentiment: str = "neutral") -> str:
        """
        Determine priority based on matched categories and sentiment
        """
        critical_keywords = [
            'sustainability_environmental',
        ]
        
        if any(cat in critical_keywords for cat in matched_categories):
            if sentiment in ['negative', 'mixed']:
                return 'critical'
            return 'high'
        
        if sentiment == 'negative':
            return 'high'
        elif sentiment == 'positive':
            return 'low'
        
        return 'medium'
