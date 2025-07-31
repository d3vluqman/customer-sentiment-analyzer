"""
Sentiment Analysis Engine
Provides hybrid sentiment analysis using multiple models
"""

import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np


class SentimentAnalyzer:
    """Advanced sentiment analyzer using multiple models"""

    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()

        # Custom keyword dictionaries for e-commerce context
        self.positive_keywords = {
            "excellent": 0.8,
            "amazing": 0.7,
            "fantastic": 0.7,
            "perfect": 0.8,
            "love": 0.6,
            "great": 0.5,
            "good": 0.4,
            "nice": 0.3,
            "awesome": 0.7,
            "wonderful": 0.6,
            "outstanding": 0.8,
            "superb": 0.7,
            "brilliant": 0.6,
            "recommend": 0.5,
            "satisfied": 0.4,
            "happy": 0.5,
            "pleased": 0.4,
            "quality": 0.3,
            "fast": 0.3,
            "quick": 0.3,
            "efficient": 0.4,
        }

        self.negative_keywords = {
            "terrible": -0.8,
            "awful": -0.7,
            "horrible": -0.8,
            "bad": -0.5,
            "poor": -0.4,
            "worst": -0.8,
            "hate": -0.7,
            "disappointed": -0.6,
            "useless": -0.7,
            "broken": -0.6,
            "defective": -0.7,
            "cheap": -0.4,
            "slow": -0.3,
            "expensive": -0.3,
            "overpriced": -0.5,
            "waste": -0.6,
            "regret": -0.5,
            "problem": -0.4,
            "issue": -0.3,
            "difficult": -0.3,
        }

    def analyze_sentiment(self, text):
        """
        Perform comprehensive sentiment analysis

        Args:
            text (str): Input text to analyze

        Returns:
            dict: Analysis results with scores and confidence
        """
        if not text or not text.strip():
            return self._empty_result()

        # Clean text
        cleaned_text = self._preprocess_text(text)

        # TextBlob analysis
        blob = TextBlob(cleaned_text)
        textblob_sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        # VADER analysis
        vader_scores = self.vader_analyzer.polarity_scores(cleaned_text)
        vader_sentiment = vader_scores["compound"]

        # Custom keyword analysis
        keyword_sentiment = self._keyword_analysis(cleaned_text)

        # Combine scores with weights
        overall_sentiment = self._combine_scores(
            textblob_sentiment, vader_sentiment, keyword_sentiment
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            textblob_sentiment, vader_sentiment, keyword_sentiment
        )

        return {
            "overall_sentiment": overall_sentiment,
            "textblob_sentiment": textblob_sentiment,
            "vader_sentiment": vader_sentiment,
            "keyword_sentiment": keyword_sentiment,
            "subjectivity": subjectivity,
            "confidence": confidence,
            "text_length": len(text),
            "word_count": len(text.split()),
        }

    def _preprocess_text(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        # Handle negations (simple approach)
        text = re.sub(r"n't", " not", text)
        text = re.sub(r"won't", "will not", text)
        text = re.sub(r"can't", "cannot", text)

        return text

    def _keyword_analysis(self, text):
        """Perform keyword-based sentiment analysis"""
        words = text.split()
        positive_score = 0
        negative_score = 0

        for word in words:
            # Remove punctuation
            clean_word = re.sub(r"[^\w]", "", word)

            if clean_word in self.positive_keywords:
                positive_score += self.positive_keywords[clean_word]
            elif clean_word in self.negative_keywords:
                negative_score += self.negative_keywords[clean_word]

        # Normalize by text length
        total_words = len(words)
        if total_words == 0:
            return 0

        net_score = (positive_score + negative_score) / total_words

        # Clamp to [-1, 1] range
        return max(-1, min(1, net_score))

    def _combine_scores(self, textblob_score, vader_score, keyword_score):
        """Combine multiple sentiment scores with weights"""
        # Weights for different models
        textblob_weight = 0.4
        vader_weight = 0.4
        keyword_weight = 0.2

        combined = (
            textblob_score * textblob_weight
            + vader_score * vader_weight
            + keyword_score * keyword_weight
        )

        return combined

    def _calculate_confidence(self, textblob_score, vader_score, keyword_score):
        """Calculate confidence based on agreement between models"""
        scores = [textblob_score, vader_score, keyword_score]

        # Calculate standard deviation (lower = more agreement = higher confidence)
        std_dev = np.std(scores)

        # Convert to confidence (0-1 scale)
        # Lower standard deviation = higher confidence
        max_std = 1.0  # Maximum possible standard deviation
        confidence = 1 - (std_dev / max_std)

        # Ensure confidence is between 0.1 and 1.0
        confidence = max(0.1, min(1.0, confidence))

        return confidence

    def _empty_result(self):
        """Return empty analysis result"""
        return {
            "overall_sentiment": 0.0,
            "textblob_sentiment": 0.0,
            "vader_sentiment": 0.0,
            "keyword_sentiment": 0.0,
            "subjectivity": 0.0,
            "confidence": 0.0,
            "text_length": 0,
            "word_count": 0,
        }

    def get_sentiment_label(self, score):
        """Convert sentiment score to human-readable label"""
        if score > 0.1:
            return "Positive"
        elif score < -0.1:
            return "Negative"
        else:
            return "Neutral"

    def get_intensity_label(self, score):
        """Get intensity label for sentiment score"""
        abs_score = abs(score)
        if abs_score >= 0.7:
            return "Very Strong"
        elif abs_score >= 0.5:
            return "Strong"
        elif abs_score >= 0.3:
            return "Moderate"
        elif abs_score >= 0.1:
            return "Weak"
        else:
            return "Neutral"
