from groq import Groq
import os

def synthesize_research(crypto_name, crypto_symbol, description, risk_data, opportunity_data):
    """Synthesize all research into comprehensive analysis"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""Create a comprehensive research report for {crypto_name} ({crypto_symbol}):

Description: {description[:300]}

Risk Analysis:
- Risk Score: {risk_data.get('risk_score', 5)}/10
- Main Concern: {risk_data.get('main_concern', 'N/A')}

Opportunity Analysis:
- Opportunity Score: {opportunity_data.get('opportunity_score', 5)}/10
- Upside Potential: {opportunity_data.get('upside_potential', 'N/A')}

Provide a JSON response with:
{{
    "investment_thesis": "2-3 sentence thesis",
    "key_metrics": ["metric1", "metric2", "metric3"],
    "timeline": "6-12 month outlook",
    "verdict": "BUY/HOLD/SELL for long-term investors"
}}

Be concise and professional."""

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
            "investment_thesis": "Unable to generate analysis at this time",
            "key_metrics": [],
            "timeline": "6-12 months",
            "verdict": "HOLD"
        }
