# 💰 LangGraph Crypto Trends Dashboard

An **AI-powered cryptocurrency market analysis platform** that autonomously researches trending cryptocurrencies, generates engaging Reddit discussions, and publishes insights—all with human-in-the-loop governance.

## 🚀 Features

- **Live Crypto Data**: Real-time cryptocurrency prices and market data from CoinGecko
- **Interactive Dashboard**: Browse top 100+ cryptocurrencies with search and filtering
- **Detailed Analytics**: Market cap, volume, price changes, ATH/ATL data
- **AI-Generated Posts**: Groq LLM generates engaging, informative Reddit-style posts
- **Human Review**: Approve, reject, or select posts before publishing
- **Auto-Publishing**: Simulate publishing to Reddit with r/CryptoTrends
- **Responsive Design**: Beautiful UI that works on all devices

## 🏗️ Architecture

### Workflow Nodes
1. **Trend-Spotter** - Fetches live crypto data from CoinGecko API
2. **Content Creator** - Generates engaging posts using Groq LLM
3. **HITL Node** - Human review and approval interface
4. **Poster** - Publishes to simulated Reddit (r/CryptoTrends)

### Tech Stack
- **Backend**: Flask + Python
- **Frontend**: HTML/CSS/JavaScript
- **LLM**: Groq (mixtral-8x7b-32768)
- **Data**: CoinGecko API (free)
- **Orchestration**: LangGraph (state machine)

## 📋 Setup

### Local Development
```bash
# Clone repo
git clone <repo-url>
cd langgraph-hitl-workflow

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your API keys
# - GROQ_API_KEY (get from https://console.groq.com)
# - TMDB_API_KEY (optional, from https://www.themoviedb.org)
# - TWITTER_BEARER_TOKEN (optional)
