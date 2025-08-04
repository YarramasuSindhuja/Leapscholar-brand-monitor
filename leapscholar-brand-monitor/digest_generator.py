from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Optional OpenAI import
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI package not installed. AI features will use fallback methods.")

class DigestGenerator:
    def __init__(self):
        # Make OpenAI client optional - only initialize if API key is available
        self.openai_client = None
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                try:
                    self.openai_client = openai.OpenAI(api_key=api_key)
                except Exception as e:
                    print(f"Warning: Could not initialize OpenAI client: {e}")
                    self.openai_client = None
            else:
                print("No OpenAI API key found. AI features will use fallback methods.")
        else:
            print("OpenAI package not available. AI features will use fallback methods.")
        
    def generate_daily_digest(self, mentions_data, brand_name="LeapScholar"):
        """Generate a 100-word daily digest of top conversations"""
        if not mentions_data:
            return "No mentions found for today."
        
        # Get today's mentions
        today = datetime.now().date()
        today_mentions = [
            mention for mention in mentions_data 
            if mention['timestamp'].date() == today
        ]
        
        if not today_mentions:
            return "No mentions found for today."
        
        # Categorize mentions
        positive_mentions = [m for m in today_mentions if m['sentiment'] == 'positive']
        negative_mentions = [m for m in today_mentions if m['sentiment'] == 'negative']
        neutral_mentions = [m for m in today_mentions if m['sentiment'] == 'neutral']
        
        # Get top mentions by engagement
        top_mentions = sorted(today_mentions, key=lambda x: x['engagement'], reverse=True)[:5]
        
        # Prepare data for AI
        summary_data = {
            'total_mentions': len(today_mentions),
            'positive_count': len(positive_mentions),
            'negative_count': len(negative_mentions),
            'neutral_count': len(neutral_mentions),
            'top_mentions': [
                {
                    'text': mention['text'][:100] + "..." if len(mention['text']) > 100 else mention['text'],
                    'sentiment': mention['sentiment'],
                    'engagement': mention['engagement'],
                    'platform': mention['platform']
                }
                for mention in top_mentions
            ]
        }
        
        # Try OpenAI if available, otherwise use fallback
        if self.openai_client:
            try:
                # Generate digest using OpenAI
                prompt = f"""
                Create a concise 100-word daily brand digest for {brand_name} based on today's social media mentions.
                
                Summary data:
                - Total mentions: {summary_data['total_mentions']}
                - Positive: {summary_data['positive_count']}
                - Negative: {summary_data['negative_count']}
                - Neutral: {summary_data['neutral_count']}
                
                Top mentions:
                {chr(10).join([f"- {mention['text']} ({mention['sentiment']}, {mention['engagement']} engagement)" for mention in summary_data['top_mentions']])}
                
                Write a professional, executive-friendly summary that highlights key insights, sentiment trends, and any urgent matters that need attention. Keep it under 100 words.
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a professional brand monitoring analyst. Write concise, actionable summaries."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                
                return response.choices[0].message.content.strip()
                
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._generate_fallback_digest(summary_data, brand_name)
        else:
            # Use fallback if OpenAI is not available
            return self._generate_fallback_digest(summary_data, brand_name)
    
    def _generate_fallback_digest(self, summary_data, brand_name):
        """Generate a fallback digest without OpenAI"""
        total = summary_data['total_mentions']
        positive = summary_data['positive_count']
        negative = summary_data['negative_count']
        
        if total == 0:
            return f"No mentions found for {brand_name} today."
        
        positivity_rate = (positive / total) * 100 if total > 0 else 0
        negativity_rate = (negative / total) * 100 if total > 0 else 0
        
        if positivity_rate > 70:
            mood = "very positive"
        elif positivity_rate > 50:
            mood = "positive"
        elif negativity_rate > 50:
            mood = "concerning"
        else:
            mood = "mixed"
        
        return f"Today's {brand_name} brand digest: {total} total mentions with {positive} positive, {negative} negative. Overall sentiment is {mood}. Top engagement came from {summary_data['top_mentions'][0]['platform'] if summary_data['top_mentions'] else 'various platforms'}."
    
    def generate_tweet_suggestions(self, mentions_data, sentiment_type="negative"):
        """Generate tweet suggestions for responding to sentiment spikes"""
        if not mentions_data:
            return []
        
        # Get recent mentions of the specified sentiment
        recent_mentions = [
            mention for mention in mentions_data 
            if mention['sentiment'] == sentiment_type and 
            (datetime.now() - mention['timestamp']).days <= 1
        ]
        
        if not recent_mentions:
            return []
        
        # Get common themes from negative mentions
        if sentiment_type == "negative":
            themes = self._extract_negative_themes(recent_mentions)
        else:
            themes = self._extract_positive_themes(recent_mentions)
        
        # Try OpenAI if available, otherwise use fallback
        if self.openai_client:
            try:
                # Generate tweet suggestions using OpenAI
                prompt = f"""
                Generate 3 professional tweet suggestions for {sentiment_type} sentiment about LeapScholar.
                
                Common themes from recent mentions:
                {chr(10).join([f"- {theme}" for theme in themes[:5]])}
                
                Create empathetic, professional responses that address concerns while maintaining brand voice.
                Format each tweet as a separate line starting with "Tweet: "
                """
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a social media manager for LeapScholar. Create professional, empathetic responses."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=300,
                    temperature=0.8
                )
                
                suggestions = response.choices[0].message.content.strip().split('\n')
                return [s.replace("Tweet: ", "").strip() for s in suggestions if s.strip()]
                
            except Exception as e:
                print(f"OpenAI API error: {e}")
                return self._generate_fallback_tweets(sentiment_type, themes)
        else:
            # Use fallback if OpenAI is not available
            return self._generate_fallback_tweets(sentiment_type, themes)
    
    def _extract_negative_themes(self, mentions):
        """Extract common themes from negative mentions"""
        themes = []
        for mention in mentions:
            text = mention['text'].lower()
            if 'fee' in text or 'cost' in text or 'expensive' in text:
                themes.append("Pricing concerns")
            elif 'service' in text or 'support' in text or 'response' in text:
                themes.append("Customer service issues")
            elif 'app' in text or 'website' in text or 'platform' in text:
                themes.append("Technical issues")
            elif 'promise' in text or 'guarantee' in text:
                themes.append("Expectation management")
            else:
                themes.append("General dissatisfaction")
        return list(set(themes))
    
    def _extract_positive_themes(self, mentions):
        """Extract common themes from positive mentions"""
        themes = []
        for mention in mentions:
            text = mention['text'].lower()
            if 'university' in text or 'admission' in text or 'accepted' in text:
                themes.append("University admissions success")
            elif 'visa' in text or 'immigration' in text:
                themes.append("Visa and immigration support")
            elif 'scholarship' in text or 'financial' in text:
                themes.append("Scholarship assistance")
            elif 'counselor' in text or 'guidance' in text:
                themes.append("Counseling and guidance")
            else:
                themes.append("General satisfaction")
        return list(set(themes))
    
    def _generate_fallback_tweets(self, sentiment_type, themes):
        """Generate fallback tweet suggestions"""
        if sentiment_type == "negative":
            return [
                "We hear your concerns and are committed to improving our services. Please reach out to our support team for immediate assistance.",
                "Thank you for your feedback. We're continuously working to enhance our platform and provide better experiences for our students.",
                "We understand your frustration and want to help resolve any issues you're facing. Let's connect to find the best solution."
            ]
        else:
            return [
                "Thank you for your kind words! We're thrilled to be part of your study abroad journey.",
                "Your success stories inspire us every day. We're honored to help students achieve their dreams.",
                "We're so grateful for your trust in LeapScholar. Here's to many more success stories!"
            ] 