import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
from collections import Counter
import re

# Import our custom modules
from sentiment_analyzer import SentimentAnalyzer
from data_collector import DataCollector
from digest_generator import DigestGenerator

# Page configuration
st.set_page_config(
    page_title="LeapScholar Brand Monitor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with card-based design
st.markdown("""
<style>
    /* Modern CSS Reset and Base Styles */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
    }
    
    /* Header Styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Card Design System */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07), 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.8);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 12px 12px 0 0;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Alert Boxes */
    .alert-box {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        border: 1px solid #feb2b2;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        position: relative;
    }
    
    .alert-box.positive {
        background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
        border-color: #9ae6b4;
    }
    
    /* Mention Cards */
    .mention-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .mention-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    .mention-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .mention-author {
        font-weight: 600;
        font-size: 1.1rem;
        color: #2d3748;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .mention-timestamp {
        font-size: 0.875rem;
        color: #718096;
        font-weight: 400;
    }
    
    .mention-content {
        font-size: 1rem;
        line-height: 1.6;
        color: #2d3748;
        margin: 1rem 0;
        padding: 1rem;
        background: #f7fafc;
        border-radius: 8px;
        border-left: 4px solid #e2e8f0;
        font-weight: 500;
    }
    
    .mention-content.positive {
        border-left-color: #48bb78;
        background: #f0fff4;
        color: #22543d;
    }
    
    .mention-content.negative {
        border-left-color: #f56565;
        background: #fff5f5;
        color: #742a2a;
    }
    
    .mention-content.neutral {
        border-left-color: #a0aec0;
        background: #f7fafc;
        color: #2d3748;
    }
    
    .mention-metrics {
        display: flex;
        gap: 1.5rem;
        align-items: center;
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
    
    .metric-item {
        display: flex;
        align-items: center;
        gap: 0.25rem;
        font-size: 0.875rem;
        color: #718096;
    }
    
    .metric-value {
        font-weight: 600;
        color: #2d3748;
    }
    
    /* Platform Badges */
    .platform-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .platform-twitter {
        background: #1da1f2;
        color: white;
    }
    
    .platform-reddit {
        background: #ff4500;
        color: white;
    }
    
    .platform-linkedin {
        background: #0077b5;
        color: white;
    }
    
    .platform-news {
        background: #34a853;
        color: white;
    }
    
    /* Sentiment Badges */
    .sentiment-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
    }
    
    .sentiment-positive {
        background: #c6f6d5;
        color: #22543d;
    }
    
    .sentiment-negative {
        background: #fed7d7;
        color: #742a2a;
    }
    
    .sentiment-neutral {
        background: #e2e8f0;
        color: #2d3748;
    }
    
    /* Top Metrics Grid */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-item-large {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .metric-value-large {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
    }
    
    /* Pulse Score */
    .pulse-score {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .pulse-value {
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .pulse-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Mood Meter */
    .mood-meter {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .mood-emoji {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .mood-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .mood-score {
        font-size: 1rem;
        color: #718096;
    }
    
    /* Influencer Cards */
    .influencer-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease;
    }
    
    .influencer-card:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-1px);
    }
    
    .influencer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .influencer-name {
        font-weight: 600;
        font-size: 1.1rem;
        color: #2d3748;
    }
    
    .influencer-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 0.75rem;
        background: #f7fafc;
        border-radius: 8px;
    }
    
    .stat-value {
        font-weight: 600;
        color: #2d3748;
        font-size: 1.1rem;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Digest Card */
    .digest-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .digest-content {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #2d3748;
        margin: 1rem 0;
        padding: 1.5rem;
        background: white;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        font-weight: 500;
    }
    
    /* Tweet Suggestions */
    .tweet-suggestion {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #48bb78;
        font-style: italic;
        color: #2d3748;
        font-weight: 500;
    }
    
    .tweet-suggestion.negative {
        border-left-color: #f56565;
        color: #742a2a;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .metrics-grid {
            grid-template-columns: 1fr;
        }
        
        .mention-metrics {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.5rem;
        }
        
        .influencer-stats {
            grid-template-columns: 1fr;
        }
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .metric-card, .mention-card, .influencer-card, .digest-card {
            background: #2d3748;
            color: #e2e8f0;
            border-color: #4a5568;
        }
        
        .mention-content {
            background: #4a5568;
            color: #e2e8f0;
        }
        
        .mention-author, .influencer-name {
            color: #e2e8f0;
        }
        
        .mention-timestamp, .metric-item {
            color: #a0aec0;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize components
@st.cache_resource
def initialize_components():
    return SentimentAnalyzer(), DataCollector(), DigestGenerator()

sentiment_analyzer, data_collector, digest_generator = initialize_components()

# Main header
st.markdown('<h1 class="main-header">🎓 LeapScholar Brand Perception Monitor</h1>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📊 Dashboard Controls")
st.sidebar.markdown("---")

# Time range selector
time_range = st.sidebar.selectbox(
    "📅 Time Range",
    ["Last 24 Hours", "Last 7 Days", "Last 30 Days"],
    index=1
)

# Platform filter
platforms = st.sidebar.multiselect(
    "🌐 Platforms",
    ["Twitter", "Reddit", "LinkedIn", "Google News"],
    default=["Twitter", "Reddit", "LinkedIn", "Google News"]
)

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Load data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_mentions_data():
    return data_collector.get_all_mentions()

mentions_data = load_mentions_data()

# Filter data based on sidebar selections
def filter_data(data, time_range, platforms):
    current_time = datetime.now()
    
    if time_range == "Last 24 Hours":
        cutoff_time = current_time - timedelta(days=1)
    elif time_range == "Last 7 Days":
        cutoff_time = current_time - timedelta(days=7)
    else:  # Last 30 Days
        cutoff_time = current_time - timedelta(days=30)
    
    filtered_data = [
        mention for mention in data
        if mention['timestamp'] >= cutoff_time and mention['platform'] in platforms
    ]
    
    return filtered_data

filtered_mentions = filter_data(mentions_data, time_range, platforms)

# Top Metrics Section
st.markdown('<div class="section-header">📊 Key Metrics Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Key metrics with improved styling
with col1:
    total_mentions = len(filtered_mentions)
    st.markdown(f"""
    <div class="metric-item-large">
        <div class="metric-value-large">{total_mentions}</div>
        <div class="metric-label">Total Mentions</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    positive_mentions = len([m for m in filtered_mentions if m['sentiment'] == 'positive'])
    st.markdown(f"""
    <div class="metric-item-large">
        <div class="metric-value-large" style="color: #48bb78;">{positive_mentions}</div>
        <div class="metric-label">Positive</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    negative_mentions = len([m for m in filtered_mentions if m['sentiment'] == 'negative'])
    st.markdown(f"""
    <div class="metric-item-large">
        <div class="metric-value-large" style="color: #f56565;">{negative_mentions}</div>
        <div class="metric-label">Negative</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    pulse_score = sentiment_analyzer.calculate_brand_pulse_score(filtered_mentions)
    st.markdown(f"""
    <div class="pulse-score">
        <div class="pulse-value">{pulse_score:.1f}</div>
        <div class="pulse-label">Brand Pulse Score</div>
    </div>
    """, unsafe_allow_html=True)

# Alert for sentiment spikes
spike_alert = data_collector.detect_spikes(filtered_mentions)
if spike_alert:
    alert_class = "positive" if spike_alert['type'] == 'positive_spike' else ""
    alert_emoji = "🎉" if spike_alert['type'] == 'positive_spike' else "🚨"
    st.markdown(f"""
    <div class="alert-box {alert_class}">
        <strong>{alert_emoji} SENTIMENT SPIKE DETECTED!</strong><br>
        {spike_alert['percentage']:.1f}% of recent mentions are {spike_alert['type'].replace('_', ' ')} 
        ({spike_alert['count']} out of {spike_alert['total']} mentions)
    </div>
    """, unsafe_allow_html=True)

# Main content area with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Sentiment Overview", 
    "🚨 Flagged Conversations", 
    "🔥 Trending Topics", 
    "👥 Influencer Tracker",
    "📧 Smart Digest"
])

# Tab 1: Sentiment Overview
with tab1:
    st.markdown('<div class="section-header">📊 Brand Sentiment Overview</div>', unsafe_allow_html=True)
    
    if filtered_mentions:
        # Sentiment distribution pie chart
        sentiment_counts = pd.DataFrame([
            {'sentiment': mention['sentiment'], 'count': 1} 
            for mention in filtered_mentions
        ]).groupby('sentiment').count().reset_index()
        
        fig_pie = px.pie(
            sentiment_counts, 
            values='count', 
            names='sentiment',
            color='sentiment',
            color_discrete_map={
                'positive': '#48bb78',
                'negative': '#f56565', 
                'neutral': '#a0aec0'
            },
            title="Sentiment Distribution"
        )
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            title_x=0.5,
            font=dict(size=14)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Sentiment over time
        df_time = pd.DataFrame(filtered_mentions)
        df_time['date'] = pd.to_datetime(df_time['timestamp']).dt.date
        
        daily_sentiment = df_time.groupby(['date', 'sentiment']).size().reset_index(name='count')
        
        fig_line = px.line(
            daily_sentiment,
            x='date',
            y='count',
            color='sentiment',
            color_discrete_map={
                'positive': '#48bb78',
                'negative': '#f56565',
                'neutral': '#a0aec0'
            },
            title="Sentiment Trends Over Time"
        )
        fig_line.update_layout(
            height=400,
            title_x=0.5,
            font=dict(size=14)
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Mood meter
        st.markdown('<div class="section-header">😊 Current Brand Mood</div>', unsafe_allow_html=True)
        avg_sentiment = np.mean([m['compound_score'] for m in filtered_mentions])
        
        if avg_sentiment > 0.3:
            mood_emoji = "😊"
            mood_text = "Very Positive"
            mood_color = "#48bb78"
        elif avg_sentiment > 0.1:
            mood_emoji = "🙂"
            mood_text = "Positive"
            mood_color = "#48bb78"
        elif avg_sentiment < -0.3:
            mood_emoji = "😡"
            mood_text = "Very Negative"
            mood_color = "#f56565"
        elif avg_sentiment < -0.1:
            mood_emoji = "😐"
            mood_text = "Negative"
            mood_color = "#f56565"
        else:
            mood_emoji = "😐"
            mood_text = "Neutral"
            mood_color = "#a0aec0"
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div class="mood-meter">
                <div class="mood-emoji">{mood_emoji}</div>
                <div class="mood-text" style="color: {mood_color};">{mood_text}</div>
                <div class="mood-score">Average Sentiment: {avg_sentiment:.3f}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No mentions found for the selected time range and platforms.")

# Tab 2: Flagged Conversations
with tab2:
    st.markdown('<div class="section-header">🚨 Flagged Conversations</div>', unsafe_allow_html=True)
    
    if filtered_mentions:
        # Get top mentions by engagement
        top_mentions = sorted(filtered_mentions, key=lambda x: x['engagement'], reverse=True)[:10]
        
        # Separate positive and negative high-impact mentions
        high_positive = [m for m in top_mentions if m['sentiment'] == 'positive'][:5]
        high_negative = [m for m in top_mentions if m['sentiment'] == 'negative'][:5]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">🎉 High-Impact Positive Mentions</div>', unsafe_allow_html=True)
            for mention in high_positive:
                platform_class = f"platform-{mention['platform'].lower()}"
                sentiment_class = f"sentiment-{mention['sentiment']}"
                
                st.markdown(f"""
                <div class="mention-card">
                    <div class="mention-header">
                        <div class="mention-author">
                            <span class="platform-badge {platform_class}">{mention['platform']}</span>
                            <strong>{mention['username']}</strong>
                            <span class="sentiment-badge {sentiment_class}">😊 Positive</span>
                        </div>
                        <div class="mention-timestamp">{mention['timestamp'].strftime('%Y-%m-%d %H:%M')}</div>
                    </div>
                    <div class="mention-content positive">{mention['text']}</div>
                    <div class="mention-metrics">
                        <div class="metric-item">
                            ❤️ <span class="metric-value">{mention['likes']}</span> Likes
                        </div>
                        <div class="metric-item">
                            🔄 <span class="metric-value">{mention['retweets']}</span> Shares
                        </div>
                        <div class="metric-item">
                            💬 <span class="metric-value">{mention['comments']}</span> Comments
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-header">⚠️ High-Impact Negative Mentions</div>', unsafe_allow_html=True)
            for mention in high_negative:
                platform_class = f"platform-{mention['platform'].lower()}"
                sentiment_class = f"sentiment-{mention['sentiment']}"
                
                st.markdown(f"""
                <div class="mention-card">
                    <div class="mention-header">
                        <div class="mention-author">
                            <span class="platform-badge {platform_class}">{mention['platform']}</span>
                            <strong>{mention['username']}</strong>
                            <span class="sentiment-badge {sentiment_class}">😠 Negative</span>
                        </div>
                        <div class="mention-timestamp">{mention['timestamp'].strftime('%Y-%m-%d %H:%M')}</div>
                    </div>
                    <div class="mention-content negative">{mention['text']}</div>
                    <div class="mention-metrics">
                        <div class="metric-item">
                            ❤️ <span class="metric-value">{mention['likes']}</span> Likes
                        </div>
                        <div class="metric-item">
                            🔄 <span class="metric-value">{mention['retweets']}</span> Shares
                        </div>
                        <div class="metric-item">
                            💬 <span class="metric-value">{mention['comments']}</span> Comments
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("No mentions found for the selected time range and platforms.")

# Tab 3: Trending Topics
with tab3:
    st.markdown('<div class="section-header">🔥 Trending Topics</div>', unsafe_allow_html=True)
    
    if filtered_mentions:
        # Extract keywords from mentions
        all_text = " ".join([mention['text'].lower() for mention in filtered_mentions])
        
        # Remove common words and extract keywords
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their', 'mine', 'yours', 'his', 'hers', 'ours', 'theirs'}
        
        words = re.findall(r'\b\w+\b', all_text)
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Count keyword frequency
        keyword_counts = Counter(keywords).most_common(20)
        
        if keyword_counts:
            # Create word cloud data
            words, counts = zip(*keyword_counts)
            
            # Create bar chart for trending topics
            fig_topics = px.bar(
                x=counts,
                y=words,
                orientation='h',
                title="Trending Keywords",
                labels={'x': 'Frequency', 'y': 'Keywords'}
            )
            fig_topics.update_layout(
                height=500,
                title_x=0.5,
                font=dict(size=14)
            )
            st.plotly_chart(fig_topics, use_container_width=True)
            
            # Display top keywords in cards
            st.markdown('<div class="section-header">📊 Top Keywords</div>', unsafe_allow_html=True)
            
            # Create a grid of keyword cards
            cols = st.columns(3)
            for i, (word, count) in enumerate(keyword_counts[:12]):
                col_idx = i % 3
                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.2rem; font-weight: 600; color: #2d3748; margin-bottom: 0.5rem;">{word}</div>
                        <div style="font-size: 0.875rem; color: #718096;">{count} mentions</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No trending topics found.")
    else:
        st.info("No mentions found for the selected time range and platforms.")

# Tab 4: Influencer Tracker
with tab4:
    st.markdown('<div class="section-header">👥 Influencer Tracker</div>', unsafe_allow_html=True)
    
    if filtered_mentions:
        # Group by username and calculate metrics
        influencer_data = {}
        for mention in filtered_mentions:
            username = mention['username']
            if username not in influencer_data:
                influencer_data[username] = {
                    'mentions': 0,
                    'total_engagement': 0,
                    'followers': mention.get('followers_count', 0),
                    'platforms': set(),
                    'sentiment_scores': []
                }
            
            influencer_data[username]['mentions'] += 1
            influencer_data[username]['total_engagement'] += mention['engagement']
            influencer_data[username]['platforms'].add(mention['platform'])
            influencer_data[username]['sentiment_scores'].append(mention['compound_score'])
        
        # Calculate average sentiment and create influencer list
        influencers = []
        for username, data in influencer_data.items():
            avg_sentiment = np.mean(data['sentiment_scores'])
            influencers.append({
                'username': username,
                'mentions': data['mentions'],
                'total_engagement': data['total_engagement'],
                'avg_engagement': data['total_engagement'] / data['mentions'],
                'followers': data['followers'],
                'platforms': ', '.join(data['platforms']),
                'avg_sentiment': avg_sentiment
            })
        
        # Sort by total engagement
        influencers.sort(key=lambda x: x['total_engagement'], reverse=True)
        
        # Display top influencers
        st.markdown('<div class="section-header">🏆 Top Influencers by Engagement</div>', unsafe_allow_html=True)
        
        for i, influencer in enumerate(influencers[:10], 1):
            sentiment_emoji = sentiment_analyzer.get_mood_emoji(
                'positive' if influencer['avg_sentiment'] > 0 else 'negative' if influencer['avg_sentiment'] < 0 else 'neutral',
                influencer['avg_sentiment']
            )
            
            st.markdown(f"""
            <div class="influencer-card">
                <div class="influencer-header">
                    <div class="influencer-name">
                        {i}. {influencer['username']} {sentiment_emoji}
                    </div>
                    <div class="mention-timestamp">
                        {influencer['platforms']}
                    </div>
                </div>
                <div class="influencer-stats">
                    <div class="stat-item">
                        <div class="stat-value">{influencer['mentions']}</div>
                        <div class="stat-label">Mentions</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{influencer['total_engagement']}</div>
                        <div class="stat-label">Total Engagement</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{influencer['followers']:,}</div>
                        <div class="stat-label">Followers</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">{influencer['avg_engagement']:.1f}</div>
                        <div class="stat-label">Avg Engagement</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No mentions found for the selected time range and platforms.")

# Tab 5: Smart Digest
with tab5:
    st.markdown('<div class="section-header">📧 Smart Digest Generator</div>', unsafe_allow_html=True)
    
    if filtered_mentions:
        # Generate daily digest
        digest = digest_generator.generate_daily_digest(filtered_mentions)
        
        st.markdown('<div class="section-header">📋 Daily Brand Digest</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="digest-card">
            <div class="digest-content">{digest}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate tweet suggestions
        st.markdown('<div class="section-header">💡 Tweet Suggestions</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">🎉 For Positive Sentiment</div>', unsafe_allow_html=True)
            positive_tweets = digest_generator.generate_tweet_suggestions(filtered_mentions, "positive")
            for i, tweet in enumerate(positive_tweets[:3], 1):
                st.markdown(f"""
                <div class="tweet-suggestion">
                    {i}. {tweet}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-header">⚠️ For Negative Sentiment</div>', unsafe_allow_html=True)
            negative_tweets = digest_generator.generate_tweet_suggestions(filtered_mentions, "negative")
            for i, tweet in enumerate(negative_tweets[:3], 1):
                st.markdown(f"""
                <div class="tweet-suggestion negative">
                    {i}. {tweet}
                </div>
                """, unsafe_allow_html=True)
        
        # Manual refresh button for digest
        if st.button("🔄 Generate New Digest"):
            st.rerun()
    else:
        st.info("No mentions found for the selected time range and platforms.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.8rem; padding: 2rem 0;">
    🎓 LeapScholar Brand Perception Monitor | Built with Streamlit and AI
</div>
""", unsafe_allow_html=True) 