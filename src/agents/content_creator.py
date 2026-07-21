"""Content Creator: Generate Bull vs Bear debate posts"""
from typing import Dict, List, Any
from .bull_agent import generate_bull_case
from .bear_agent import generate_bear_case

def generate_content(trends: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate debate posts from both perspectives"""
    try:
        cryptos = trends.get("trending_films", [])
        if not cryptos:
            return []
        
        posts = []
        
        # Generate posts for top 3 cryptos
        for crypto in cryptos[:3]:
            bull_post = generate_bull_case(crypto)
            bear_post = generate_bear_case(crypto)
            
            # Create debate thread
            debate_post = f"""
🔥 DEBATE: {crypto['title']} ({crypto['symbol']}) - Moon or Bust?

📈 THE BULL CASE:
{bull_post}

---

📉 THE BEAR CASE:
{bear_post}

---

💬 What's YOUR take? Bull or Bear on {crypto['symbol']}?
"""
            
            posts.append({
                "content": debate_post.strip(),
                "platform": "reddit",
                "type": "debate"
            })
        
        return posts if posts else [{"content": "Crypto debate time!", "platform": "reddit", "type": "debate"}]
    
    except Exception as e:
        print(f"Error: {e}")
        return [{"content": "Bull vs Bear debate!", "platform": "reddit", "type": "debate"}]
