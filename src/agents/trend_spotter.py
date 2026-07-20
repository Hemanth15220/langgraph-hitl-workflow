"""Trend-Spotter: Fetch top 100 cryptocurrencies"""
import requests
from typing import Dict, Any

def get_global_trends() -> Dict[str, Any]:
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "sparkline": False,
            "price_change_percentage": "24h,7d"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        trending_cryptos = []
        for coin in data:
            trending_cryptos.append({
                "id": coin.get("id"),
                "title": coin.get("name"),
                "symbol": coin.get("symbol", "").upper(),
                "price": coin.get("current_price", 0),
                "market_cap": coin.get("market_cap"),
                "market_cap_rank": coin.get("market_cap_rank"),
                "volume_24h": coin.get("total_volume"),
                "change_24h": coin.get("price_change_percentage_24h", 0),
                "change_7d": coin.get("price_change_percentage_7d", 0),
                "image": coin.get("image")
            })
        
        return {
            "trending_films": trending_cryptos,
            "total_cryptos": len(data),
            "source": "CoinGecko Real-Time API",
            "timestamp": "Real-time"
        }
    except Exception as e:
        print(f"Error: {e}")
        return {"trending_films": [], "error": str(e)}

def get_crypto_details(crypto_id: str) -> Dict[str, Any]:
    """Get detailed info for a specific crypto"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}"
        params = {"localization": False}
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        return {
            "id": data.get("id"),
            "name": data.get("name"),
            "symbol": data.get("symbol", "").upper(),
            "price": data.get("market_data", {}).get("current_price", {}).get("usd", 0),
            "market_cap": data.get("market_data", {}).get("market_cap", {}).get("usd"),
            "volume_24h": data.get("market_data", {}).get("total_volume", {}).get("usd"),
            "ath": data.get("market_data", {}).get("ath", {}).get("usd"),
            "atl": data.get("market_data", {}).get("atl", {}).get("usd"),
            "description": data.get("description", {}).get("en", ""),
            "image": data.get("image", {}).get("large")
        }
    except Exception as e:
        return {"error": str(e)}
