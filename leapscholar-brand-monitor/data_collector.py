import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import requests
from bs4 import BeautifulSoup
import time

class DataCollector:
    def __init__(self):
        self.brand_keywords = ['leapscholar', 'leap scholar', 'leap-scholar', 'leap_scholar']
        
    def generate_mock_data(self, days_back=7):
        """Generate realistic mock data for demonstration"""
        mentions = []
        
        # Sample positive mentions
        positive_texts = [
            "Just got accepted to my dream university thanks to @LeapScholar! Their guidance was incredible! 🎓",
            "LeapScholar's study abroad program is amazing. Highly recommend for anyone looking to study overseas!",
            "The LeapScholar team helped me navigate the entire application process. Couldn't be happier!",
            "Finally got my student visa! LeapScholar made everything so much easier. Thank you!",
            "LeapScholar's scholarship opportunities are incredible. They really care about students' success.",
            "Amazing experience with LeapScholar. Their counselors are so knowledgeable and supportive!",
            "Thanks to LeapScholar, I'm now studying at my dream university abroad! Life-changing experience.",
            "LeapScholar's application guidance was spot-on. Got into my top choice university!",
            "The LeapScholar community is so supportive. Met amazing people through their programs!",
            "LeapScholar's resources are top-notch. They really know how to help students succeed."
        ]
        
        # Sample negative mentions
        negative_texts = [
            "LeapScholar's fees are way too high for what they offer. Not worth it.",
            "Disappointed with LeapScholar's customer service. They never respond to emails.",
            "LeapScholar promised guaranteed admission but I got rejected. Waste of money.",
            "The LeapScholar app keeps crashing. Very frustrating experience.",
            "LeapScholar's counselors seem inexperienced. Not getting the help I need.",
            "LeapScholar's website is confusing and hard to navigate.",
            "They promised scholarship but I didn't get anything. LeapScholar is misleading.",
            "LeapScholar's response time is terrible. Takes days to get a reply.",
            "The LeapScholar program didn't live up to expectations. Overpriced.",
            "LeapScholar's study materials are outdated and not helpful."
        ]
        
        # Sample neutral mentions
        neutral_texts = [
            "Looking into LeapScholar for study abroad options. Anyone have experience?",
            "LeapScholar seems to have good reviews. Might try their services.",
            "Saw an ad for LeapScholar today. Anyone know if they're legit?",
            "LeapScholar offers study abroad programs. Need to research more.",
            "Considering LeapScholar for university applications. Any thoughts?",
            "LeapScholar has various programs. Need to compare with other options.",
            "Heard about LeapScholar from a friend. Looking into their services.",
            "LeapScholar appears in many search results for study abroad.",
            "LeapScholar's website has information about different countries.",
            "Checking out LeapScholar's social media presence."
        ]
        
        platforms = ['Twitter', 'Reddit', 'LinkedIn', 'Google News']
        usernames = ['student_life', 'study_abroad_2024', 'university_hopeful', 'global_learner', 
                    'academic_advisor', 'education_expert', 'student_success', 'abroad_bound',
                    'scholarship_hunter', 'international_student']
        
        current_time = datetime.now()
        
        for i in range(50):  # Generate 50 mentions
            # Random date within the last week
            days_ago = random.randint(0, days_back)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            
            mention_time = current_time - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # Randomly select sentiment and text
            sentiment_choice = random.choices(['positive', 'negative', 'neutral'], weights=[0.4, 0.2, 0.4])[0]
            
            if sentiment_choice == 'positive':
                text = random.choice(positive_texts)
                compound_score = random.uniform(0.1, 0.8)
            elif sentiment_choice == 'negative':
                text = random.choice(negative_texts)
                compound_score = random.uniform(-0.8, -0.1)
            else:
                text = random.choice(neutral_texts)
                compound_score = random.uniform(-0.1, 0.1)
            
            # Generate engagement metrics
            likes = random.randint(0, 500)
            retweets = random.randint(0, 100)
            comments = random.randint(0, 50)
            engagement = likes + retweets * 2 + comments * 3
            
            # Generate follower count
            followers_count = random.randint(100, 100000)
            
            mention = {
                'id': f"mention_{i}",
                'text': text,
                'platform': random.choice(platforms),
                'username': random.choice(usernames),
                'timestamp': mention_time,
                'likes': likes,
                'retweets': retweets,
                'comments': comments,
                'engagement': engagement,
                'followers_count': followers_count,
                'sentiment': sentiment_choice,
                'compound_score': compound_score,
                'url': f"https://{random.choice(platforms).lower()}.com/status/{i}"
            }
            
            mentions.append(mention)
        
        return mentions
    
    def scrape_twitter(self, query, count=100):
        """Scrape Twitter mentions (mock implementation)"""
        # In a real implementation, you would use Twitter API or twint
        # For now, return mock data
        return self.generate_mock_data()
    
    def scrape_reddit(self, subreddits, count=100):
        """Scrape Reddit mentions (mock implementation)"""
        # In a real implementation, you would use PRAW
        # For now, return mock data
        return self.generate_mock_data()
    
    def scrape_google_news(self, query, count=50):
        """Scrape Google News mentions (mock implementation)"""
        # In a real implementation, you would use SerpAPI or similar
        # For now, return mock data
        return self.generate_mock_data()
    
    def get_all_mentions(self):
        """Get mentions from all platforms"""
        all_mentions = []
        
        # Collect from different platforms
        twitter_mentions = self.scrape_twitter("LeapScholar")
        reddit_mentions = self.scrape_reddit(["studyabroad", "college", "universities"])
        news_mentions = self.scrape_google_news("LeapScholar")
        
        all_mentions.extend(twitter_mentions)
        all_mentions.extend(reddit_mentions)
        all_mentions.extend(news_mentions)
        
        # Sort by timestamp
        all_mentions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return all_mentions
    
    def detect_spikes(self, mentions_data, window_hours=24):
        """Detect sentiment spikes in the last 24 hours"""
        current_time = datetime.now()
        recent_mentions = [
            mention for mention in mentions_data 
            if (current_time - mention['timestamp']).total_seconds() < window_hours * 3600
        ]
        
        if not recent_mentions:
            return None
        
        # Calculate sentiment distribution
        positive_count = sum(1 for m in recent_mentions if m['sentiment'] == 'positive')
        negative_count = sum(1 for m in recent_mentions if m['sentiment'] == 'negative')
        total_count = len(recent_mentions)
        
        # Detect spikes (if more than 60% of recent mentions are positive/negative)
        if positive_count / total_count > 0.6:
            return {
                'type': 'positive_spike',
                'percentage': (positive_count / total_count) * 100,
                'count': positive_count,
                'total': total_count
            }
        elif negative_count / total_count > 0.6:
            return {
                'type': 'negative_spike',
                'percentage': (negative_count / total_count) * 100,
                'count': negative_count,
                'total': total_count
            }
        
        return None 