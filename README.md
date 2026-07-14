# LangGraph HITL Workflow

Production-grade LangGraph workflow demonstrating stateful content generation with human-in-the-loop control and interrupt-based governance.

## Project Overview

An **autonomous content agent** that:
1. **Researches** global film trends from TMDB
2. **Generates** engaging social media posts using Groq LLM
3. **Pauses** for human review/approval using LangGraph's interrupt() primitive
4. **Publishes** approved content to Twitter/X
5. **Observes** the entire workflow via LangSmith

**Tech Stack:** LangGraph + Groq + TMDB + Twitter API (all free tier, open-source)

---

## Setup Status ✅

### Completed Tasks
- ✅ Project structure created
- ✅ Python virtual environment set up
- ✅ All dependencies installed
- ✅ API keys configured (TMDB, Groq, Twitter/X, LangSmith)
- ✅ Git repository initialized and committed

### Current Environment
- **Platform:** GitHub Codespaces
- **Python:** 3.x (venv activated)
- **LLM:** Groq (mixtral-8x7b-32768)
- **Dependencies:** See requirements.txt

---

## Project Structure

