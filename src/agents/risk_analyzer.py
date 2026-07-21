from groq import Groq
import os

def analyze_risks(crypto_name, crypto_symbol, price, market_cap, volume_24h, volatility):
    """Analyze risks for a cryptocurrency"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Analyze the risks for {crypto_name} ({crypto_symbol}):

Price: ${price:,.2f}
Market Cap: ${market_cap:,.0f}
24h Volume: ${volume_24h:,.0f}
Implied Volatility: {volatility:.1f}%

Provide a JSON response with:
{{
    "risk_score": 1-10,
    "risks": ["risk1", "risk2", "risk3"],
    "main_concern": "primary risk",
    "severity": "low/medium/high"
}}

Be concise and analytical."""

    message = client.messages.create(
        model="llama-3.1-8b-instant",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    try:
        response_text = message.content[0].text
        # Extract JSON from response
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        json_str = response_text[start:end]
        return json.loads(json_str)
    except:
        return {
            "risk_score": 5,
            "risks": ["Market volatility", "Regulatory uncertainty"],
            "main_concern": "Market conditions",
            "severity": "medium"
        }
