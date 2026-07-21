from groq import Groq
import os
import json

def analyze_best_trades(cryptos_list):
    """Analyze which cryptos are best to buy and sell"""
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        crypto_data = "\n".join([
            f"{c['symbol']}: Price=${c['price']:,.0f}, MCap=${c['market_cap']:,.0f}, Change24h={c['change_24h']:.1f}%"
            for c in cryptos_list[:20]
        ])
        
        prompt = f"""Analyze top 20 cryptos and recommend BEST 3 to BUY and BEST 3 to SELL:

{crypto_data}

Return valid JSON only (no markdown, no extra text):
{{
    "best_buys": [
        {{"symbol": "BTC", "reason": "Strong recovery potential", "price_target": "$50,000"}},
        {{"symbol": "ETH", "reason": "DeFi ecosystem growth", "price_target": "$3,000"}},
        {{"symbol": "SOL", "reason": "High adoption rate", "price_target": "$150"}}
    ],
    "best_sells": [
        {{"symbol": "XYZ", "reason": "Overvalued signals", "target_profit": "20%"}},
        {{"symbol": "ABC", "reason": "Declining volume trend", "target_profit": "15%"}},
        {{"symbol": "DEF", "reason": "Regulatory risks ahead", "target_profit": "10%"}}
    ],
    "market_outlook": "Market shows cautious optimism with emerging opportunities."
}}"""
        
        message = client.messages.create(
            model="llama-3.1-8b-instant",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        start = response_text.find('{')
        end = response_text.rfind('}') + 1
        
        if start == -1 or end <= start:
            raise ValueError("No JSON found in response")
        
        json_str = response_text[start:end]
        return json.loads(json_str)
    except Exception as e:
        print(f"Trade advisor error: {e}")
        return {
            "best_buys": [
                {"symbol": "BTC", "reason": "Market leader with strong fundamentals", "price_target": "$50,000+"},
                {"symbol": "ETH", "reason": "DeFi backbone, strong ecosystem", "price_target": "$3,000+"},
                {"symbol": "SOL", "reason": "High-speed blockchain, growing adoption", "price_target": "$150+"}
            ],
            "best_sells": [
                {"symbol": "Monitor portfolio", "reason": "Take profits on 30%+ gains", "target_profit": "Lock in gains"},
                {"symbol": "Reduce risk", "reason": "Exit highly volatile positions", "target_profit": "Secure capital"},
                {"symbol": "Diversify", "reason": "Don't concentrate in one asset", "target_profit": "Balance portfolio"}
            ],
            "market_outlook": "Market dynamics are shifting. Focus on fundamentals and risk management."
        }
