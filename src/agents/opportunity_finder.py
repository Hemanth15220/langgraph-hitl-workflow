from groq import Groq
import os

def find_opportunities(crypto_name, crypto_symbol, price, market_cap, change_24h, ath, atl):
    """Find investment opportunities for a cryptocurrency"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    from_ath = ((ath - price) / ath * 100) if ath > 0 else 0
    from_atl = ((price - atl) / atl * 100) if atl > 0 else 0
    
    prompt = f"""Analyze investment opportunities for {crypto_name} ({crypto_symbol}):

Current Price: ${price:,.2f}
Market Cap: ${market_cap:,.0f}
24h Change: {change_24h:.2f}%
Distance from ATH: {from_ath:.1f}%
Distance from ATL: {from_atl:.1f}%

Provide a JSON response with:
{{
    "opportunity_score": 1-10,
    "catalysts": ["catalyst1", "catalyst2", "catalyst3"],
    "upside_potential": "low/medium/high",
    "entry_point": "description of when to buy",
    "target_price_range": "next 6-12 months estimate"
}}

Be concise and analytical."""

    message = client.messages.create(
        model="llama-3.1-8b-instant",
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    try:
        response_text = message.content[0].text
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        json_str = response_text[start:end]
        return json.loads(json_str)
    except:
        return {
            "opportunity_score": 5,
            "catalysts": ["Market adoption", "Technology development"],
            "upside_potential": "medium",
            "entry_point": "On market dips",
            "target_price_range": "20-40% upside potential"
        }
