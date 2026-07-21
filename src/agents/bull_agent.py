"""Bull Agent: Bullish perspective on crypto"""
from groq import Groq
from ..config import GROQ_API_KEY, GROQ_MODEL

def generate_bull_case(crypto):
    """Generate bullish argument"""
    try:
        client = Groq(api_key=GROQ_API_KEY)
        prompt = f"""You are a crypto bull on Reddit. Generate a BULLISH argument for {crypto['title']} ({crypto['symbol']}).

Current price: ${crypto['price']}
24h change: {crypto['change_24h']}%
Market cap: ${crypto['market_cap']}

Write a short, enthusiastic Reddit post (150-200 words) that:
- Lists 3 reasons why this crypto will surge
- Shows excitement and confidence
- Asks a bullish question to spark debate
- Uses phrases: "bullish", "moon", "hodl", "potential"

Make it sound like a real crypto enthusiast!"""
        
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"🚀 {crypto['symbol']} is going to moon! Look at the fundamentals!"
