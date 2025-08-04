# 🚀 Quick Start Guide

## Immediate Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Dashboard
```bash
python run.py
```
OR
```bash
streamlit run app.py
```

### 3. Access Dashboard
Open your browser and go to: `http://localhost:8501`

## 🎯 What You'll See

### Dashboard Overview
- **Top Metrics**: Total mentions, positive/negative counts, Brand Pulse Score
- **Spike Alerts**: Automatic detection of sentiment spikes
- **5 Main Tabs**: Sentiment Overview, Flagged Conversations, Trending Topics, Influencer Tracker, Smart Digest

### Key Features to Explore

#### 📊 Sentiment Overview Tab
- **Pie Chart**: Visual breakdown of positive/negative/neutral mentions
- **Line Chart**: Sentiment trends over time
- **Mood Meter**: Emoji-based sentiment indicator (😡 😐 😊)

#### 🚨 Flagged Conversations Tab
- **High-Impact Positive**: Top positive mentions by engagement
- **High-Impact Negative**: Top negative mentions requiring attention
- **Platform Breakdown**: See engagement across Twitter, Reddit, LinkedIn, Google News

#### 🔥 Trending Topics Tab
- **Keyword Analysis**: Most mentioned terms and phrases
- **Bar Charts**: Visual representation of trending topics
- **Topic Clustering**: Grouped related conversations

#### 👥 Influencer Tracker Tab
- **Top Influencers**: Users with highest engagement and follower counts
- **Sentiment by Influencer**: How each influencer feels about LeapScholar
- **Platform Distribution**: Which platforms your influencers use most

#### 📧 Smart Digest Tab
- **Daily Summary**: AI-generated 100-word brand digest
- **Tweet Suggestions**: Ready-to-use response suggestions
- **Sentiment-Specific**: Different suggestions for positive vs negative sentiment

## 🎛️ Dashboard Controls

### Sidebar Options
- **Time Range**: Last 24 Hours, Last 7 Days, Last 30 Days
- **Platform Filter**: Select specific platforms to monitor
- **Refresh Button**: Update data manually

### Interactive Features
- **Hover Charts**: Get detailed information on hover
- **Filter Data**: Use sidebar controls to filter results
- **Export Ready**: All data can be exported for further analysis

## 📊 Understanding the Metrics

### Brand Pulse Score (0-100)
- **40% Volume**: Number of mentions relative to baseline
- **40% Positivity**: Percentage of positive mentions
- **20% Influencer Impact**: Effect of high-follower accounts

### Sentiment Categories
- **Positive**: Compound score > 0.05
- **Negative**: Compound score < -0.05
- **Neutral**: Compound score between -0.05 and 0.05

### Engagement Metrics
- **Likes**: Direct positive reactions
- **Retweets/Shares**: Amplification of content
- **Comments**: Direct engagement and discussion

## 🔧 Customization

### For Different Brands
1. Edit `config.py` to change brand name and keywords
2. Update `data_collector.py` with your brand's keywords
3. Modify `sentiment_analyzer.py` for custom sentiment thresholds

### For Different Platforms
1. Add new platform methods in `data_collector.py`
2. Update platform list in sidebar
3. Add platform-specific data processing

## 🚨 Troubleshooting

### Common Issues
- **Port 8501 in use**: Change port in `run.py` or kill existing process
- **Missing packages**: Run `pip install -r requirements.txt`
- **API errors**: Check `.env` file for correct API keys

### Performance Tips
- **Cache data**: Dashboard caches data for 5 minutes
- **Filter data**: Use sidebar filters to reduce data load
- **Refresh selectively**: Use refresh button instead of full page reload

## 🎯 Next Steps

### For Production Use
1. **Add API Keys**: Create `.env` file with real API keys
2. **Connect Real Data**: Replace mock data with actual API calls
3. **Set Up Alerts**: Configure email alerts for sentiment spikes
4. **Deploy**: Host on Streamlit Cloud or your own server

### For Advanced Features
1. **Competitor Analysis**: Add competitor tracking
2. **Advanced Analytics**: Implement machine learning predictions
3. **Team Access**: Add user authentication and role-based access
4. **Mobile App**: Create native mobile application

## 📞 Support

- **Documentation**: Check `README.md` for detailed information
- **Issues**: Report problems via GitHub issues
- **Features**: Suggest new features via GitHub issues

---

**🎓 Ready to monitor your brand perception intelligently!** 