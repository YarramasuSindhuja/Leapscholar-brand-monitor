import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Brand settings
    BRAND_NAME = "LeapScholar"
    BRAND_KEYWORDS = ['leapscholar', 'leap scholar', 'leap-scholar', 'leap_scholar']
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    # Reddit API
    REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
    REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
    REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'LeapScholarBrandMonitor/1.0')
    
    # SerpAPI for Google News
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
    
    # Email alerts
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', 'marketing@leapscholar.com')
    
    # Dashboard settings
    DEFAULT_TIME_RANGE = "Last 7 Days"
    DEFAULT_PLATFORMS = ["Twitter", "Reddit", "LinkedIn", "Google News"]
    
    # Sentiment analysis settings
    SENTIMENT_THRESHOLD = 0.05
    SPIKE_DETECTION_THRESHOLD = 0.6  # 60% of mentions must be positive/negative to trigger alert
    
    # Data collection settings
    MAX_MENTIONS_PER_PLATFORM = 100
    CACHE_DURATION_MINUTES = 5
    
    # Influencer settings
    MIN_FOLLOWER_COUNT = 10000  # Minimum followers to be considered an influencer
    MIN_ENGAGEMENT_THRESHOLD = 50  # Minimum engagement to flag as high-impact 