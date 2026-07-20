"""Content Creator: Generate engaging crypto posts"""
from groq import Groq
from typing import Dict, List, Any
from ..config import GROQ_API_KEY, GROQ_MODEL

def generate_content(trends: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate creative crypto posts"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        cryptos = trends.get("trending_films", [])
        if not cryptos:
            return []
        
        top_cryptos = cryptos[:5]
        crypto_list = "\n".join([f"- {c.get('title')} ({c.get('symbol')}): ${c.get('price')} | 24h: {c.get('change_24h')}% | Market Cap: ${c.get('market_cap')}" for c in top_cryptos])
        
        prompt = f"""You are a crypto analyst posting on Reddit about market trends and opportunities.

Current Top Cryptos:
{crypto_list}

Write 3 engaging Reddit discussion posts that:
1. Compare cryptos with each other (which is outperforming, why)
2. Analyze trends (bullish/bearish signals, market patterns)
3. Ask thought-provoking questions about the market
4. Discuss potential impacts (adoption, regulation, tech updates)
5. Use crypto slang naturally (hodl, bullish, bearish, moon, etc)
6. Add relevant emojis but not excessive
7. Sound like real community discussion, not promotional

Format:
Post 1: [Engaging discussion about trends and analysis]
Post 2: [Comparison between cryptos with market insight]
Post 3: [Question about market impact and future predictions]"""

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = response.choices[0].message.content
        posts = parse_posts(response_text)
        return posts if posts else [{"content": "What are your thoughts on the current market trends?", "platform": "reddit"}]
    
    except Exception as e:
        print(f"Error: {e}")
        return [{"content": "Let's discuss the market trends!", "platform": "reddit"}]

def parse_posts(response_text: str) -> List[Dict[str, str]]:
    """Parse posts from LLM response"""
    posts = []
    current_post = ""
    
    for line in response_text.split("\n"):
        if line.strip().startswith("Post"):
            if current_post:
                posts.append({"content": current_post.strip(), "platform": "reddit"})
            current_post = ""
        else:
            if line.strip():
                current_post += " " + line.strip()
    
    if current_post:
        posts.append({"content": current_post.strip(), "platform": "reddit"})
    
    return posts[:3] if posts else [{"content": "What's your take on the market?", "platform": "reddit"}]
