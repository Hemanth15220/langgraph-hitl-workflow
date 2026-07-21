"""Bear Agent: Bearish perspective on crypto"""
from groq import Groq
from ..config import GROQ_API_KEY, GROQ_MODEL

def generate_bear_case(crypto):
    """Generate bearish argument"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"""You are a cautious crypto analyst on Reddit. Generate a BEARISH argument for {crypto['title']} ({crypto['symbol']}).

Current price: ${crypto['price']}
24h change: {crypto['change_24h']}%
Market cap: ${crypto['market_cap']}

Write a short, skeptical Reddit post (150-200 words) that:
- Lists 3 risks or concerns with this crypto
- Shows caution and due diligence
- Asks critical questions
- Uses phrases: "bearish", "risk", "caution", "regulation", "volatility"

Make it sound like a real crypto researcher questioning the hype!"""
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Hold up - there are serious risks with {crypto['symbol']} we need to discuss"
