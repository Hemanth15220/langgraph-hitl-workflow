import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_MODEL = os.getenv("LLM_MODEL", "mistral")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")

# TMDB API
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "mixtral-8x7b-32768")

# Twitter/X API
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

# LangSmith (optional observability)
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "langgraph-hitl-workflow")
