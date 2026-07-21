from groq import Groq
import os

def compare_cryptos(crypto_list):
    """Compare multiple cryptocurrencies"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    comparison_data = "\n".join([
        f"{c['symbol']}: Price=${c['price']:,.2f}, Market Cap=${c['market_cap']:,.0f}, Change={c['change_24h']:.2f}%"
        for c in crypto_list
    ])
    
    prompt = f"""Compare these cryptocurrencies and identify the best for different investor types:

{comparison_data}

Provide a JSON response with:
{{
    "best_for_growth": {{"crypto": "symbol", "reason": "why"}},
    "best_for_stability": {{"crypto": "symbol", "reason": "why"}},
    "best_risk_reward": {{"crypto": "symbol", "reason": "why"}},
    "summary": "brief comparison summary"
}}

Be concise and analytical."""

    message = client.messages.create(
        model="llama-3.1-8b-instant",
        max_tokens=300,
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
            "best_for_growth": {"crypto": "N/A", "reason": "Unable to analyze"},
            "best_for_stability": {"crypto": "N/A", "reason": "Unable to analyze"},
            "best_risk_reward": {"crypto": "N/A", "reason": "Unable to analyze"},
            "summary": "Comparison data unavailable"
        }
