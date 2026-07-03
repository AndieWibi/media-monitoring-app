from textblob import TextBlob
from typing import Tuple
import numpy as np


class SentimentAnalyzer:
    """
    Service for analyzing sentiment of articles
    Uses TextBlob for initial analysis, can be extended with transformers
    """

    def __init__(self):
        self.sentiment_mapping = {
            'positive': 'positive',
            'negative': 'negative',
            'neutral': 'neutral',
            'mixed': 'mixed'
        }

    def analyze(self, text: str, title: str = "") -> Tuple[str, float]:
        """
        Analyze sentiment of text
        Returns: (sentiment_category, sentiment_score)
        sentiment_score: -1.0 (negative) to 1.0 (positive)
        """
        combined_text = f"{title}. {text}"
        
        blob = TextBlob(combined_text)
        polarity = blob.sentiment.polarity  # -1 to 1
        
        sentiment_category = self._categorize_sentiment(polarity)
        
        return sentiment_category, float(polarity)

    def _categorize_sentiment(self, polarity: float) -> str:
        """
        Categorize polarity score into sentiment categories
        """
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'

    def analyze_batch(self, texts: list, titles: list = None) -> list:
        """
        Analyze sentiment for multiple texts
        """
        if titles is None:
            titles = [""] * len(texts)
        
        results = []
        for text, title in zip(texts, titles):
            sentiment, score = self.analyze(text, title)
            results.append({
                'sentiment': sentiment,
                'score': score
            })
        
        return results

    def detect_sentiment_shift(self, previous_score: float, current_score: float, threshold: float = 0.3) -> bool:
        """
        Detect if there's a significant shift in sentiment
        """
        shift = abs(current_score - previous_score)
        return shift > threshold
