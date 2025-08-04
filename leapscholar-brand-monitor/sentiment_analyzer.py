import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re
from datetime import datetime, timedelta

class SentimentAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        
    def clean_text(self, text):
        """Clean text for sentiment analysis"""
        if not text or not isinstance(text, str):
            return ""
        
        # Remove URLs, mentions, and special characters
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'@\w+|#\w+', '', text)
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower().strip()
        
        return text
    
    def analyze_sentiment(self, text):
        """Analyze sentiment using both VADER and TextBlob"""
        cleaned_text = self.clean_text(text)
        
        if not cleaned_text:
            return {
                'compound': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 1,
                'sentiment': 'neutral',
                'confidence': 0
            }
        
        # VADER analysis
        vader_scores = self.vader_analyzer.polarity_scores(cleaned_text)
        
        # TextBlob analysis
        blob = TextBlob(cleaned_text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # Combine scores
        compound_score = (vader_scores['compound'] + textblob_polarity) / 2
        confidence = (1 - textblob_subjectivity) * 0.5 + 0.5  # Higher confidence for less subjective text
        
        # Determine sentiment category
        if compound_score >= 0.05:
            sentiment = 'positive'
        elif compound_score <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'compound': compound_score,
            'positive': vader_scores['pos'],
            'negative': vader_scores['neg'],
            'neutral': vader_scores['neu'],
            'sentiment': sentiment,
            'confidence': confidence,
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity
        }
    
    def get_mood_emoji(self, sentiment, compound_score):
        """Get mood emoji based on sentiment"""
        if sentiment == 'positive':
            if compound_score > 0.5:
                return "😊"
            else:
                return "🙂"
        elif sentiment == 'negative':
            if compound_score < -0.5:
                return "😡"
            else:
                return "😐"
        else:
            return "😐"
    
    def calculate_brand_pulse_score(self, mentions_data):
        """Calculate Brand Pulse Score (0-100) based on volume, positivity, and influencer impact"""
        if not mentions_data:
            return 0
        
        total_mentions = len(mentions_data)
        positive_mentions = sum(1 for mention in mentions_data if mention.get('sentiment') == 'positive')
        negative_mentions = sum(1 for mention in mentions_data if mention.get('sentiment') == 'negative')
        
        # Calculate positivity ratio
        positivity_ratio = positive_mentions / total_mentions if total_mentions > 0 else 0
        
        # Calculate engagement score (simplified)
        total_engagement = sum(mention.get('engagement', 0) for mention in mentions_data)
        avg_engagement = total_engagement / total_mentions if total_mentions > 0 else 0
        
        # Calculate influencer impact (mentions with high follower counts)
        influencer_mentions = sum(1 for mention in mentions_data 
                               if mention.get('followers_count', 0) > 10000)
        influencer_ratio = influencer_mentions / total_mentions if total_mentions > 0 else 0
        
        # Combine scores (40% volume, 40% positivity, 20% influencer impact)
        volume_score = min(total_mentions / 100, 1) * 40  # Cap at 100 mentions
        positivity_score = positivity_ratio * 40
        influencer_score = influencer_ratio * 20
        
        pulse_score = volume_score + positivity_score + influencer_score
        
        return min(pulse_score, 100)  # Cap at 100 