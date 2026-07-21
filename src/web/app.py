import os
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
import requests
from src.workflow.research_graph import run_research_workflow

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_workflow():
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50&page=1&sparkline=false"
        
        for attempt in range(3):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                cryptos = response.json()
                
                formatted_cryptos = [
                    {
                        'id': c.get('id', ''),
                        'title': c.get('name', ''),
                        'symbol': (c.get('symbol') or '').upper(),
                        'price': c.get('current_price') or 0,
                        'market_cap': c.get('market_cap') or 0,
                        'market_cap_rank': c.get('market_cap_rank'),
                        'volume_24h': c.get('total_volume') or 0,
                        'change_24h': c.get('price_change_percentage_24h') or 0,
                        'change_7d': c.get('price_change_percentage_7d') or 0,
                        'image': c.get('image', '')
                    }
                    for c in cryptos if c
                ]
                
                return jsonify({'success': True, 'cryptos': formatted_cryptos})
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    if attempt < 2:
                        import time
                        time.sleep(5 * (attempt + 1))
                    else:
                        raise
                else:
                    raise
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/crypto/<crypto_id>', methods=['GET'])
def get_crypto(crypto_id):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}?localization=false&market_data=true&community_data=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        market_data = data.get('market_data', {})
        
        return jsonify({
            'id': data.get('id', ''),
            'name': data.get('name', ''),
            'symbol': (data.get('symbol') or '').upper(),
            'description': data.get('description', {}).get('en', 'N/A'),
            'image': data.get('image', {}).get('large', ''),
            'price': market_data.get('current_price', {}).get('usd') or 0,
            'market_cap': market_data.get('market_cap', {}).get('usd') or 0,
            'market_cap_rank': data.get('market_cap_rank') or 'N/A',
            'volume_24h': market_data.get('total_volume', {}).get('usd') or 0,
            'change_24h': market_data.get('price_change_percentage_24h') or 0,
            'change_7d': market_data.get('price_change_percentage_7d') or 0,
            'ath': market_data.get('ath', {}).get('usd') or 0,
            'atl': market_data.get('atl', {}).get('usd') or 0,
            'circulating_supply': market_data.get('circulating_supply') or 0,
            'total_supply': market_data.get('total_supply') or 0,
            'max_supply': market_data.get('max_supply') or 0,
            'website': data.get('links', {}).get('homepage', [''])[0] if data.get('links', {}).get('homepage') else '',
            'community_score': data.get('community_score') or 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/research/<crypto_id>', methods=['GET'])
def get_research(crypto_id):
    """Get AI-powered research analysis for a crypto"""
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}?localization=false&market_data=true"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        market_data = data.get('market_data', {})
        
        crypto_data = {
            'name': data.get('name', ''),
            'symbol': (data.get('symbol') or '').upper(),
            'price': market_data.get('current_price', {}).get('usd') or 0,
            'market_cap': market_data.get('market_cap', {}).get('usd') or 0,
            'volume_24h': market_data.get('total_volume', {}).get('usd') or 0,
            'change_24h': market_data.get('price_change_percentage_24h') or 0,
            'ath': market_data.get('ath', {}).get('usd') or 0,
            'atl': market_data.get('atl', {}).get('usd') or 0,
            'description': data.get('description', {}).get('en', 'No description available')[:300]
        }
        
        research_results = run_research_workflow(crypto_data)
        
        return jsonify({
            'success': True,
            'risk_analysis': research_results['risk_analysis'],
            'opportunity_analysis': research_results['opportunity_analysis'],
            'research_synthesis': research_results['research_synthesis']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/best-trades', methods=['GET'])
def get_best_trades():
    """Get best cryptos to buy and sell"""
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=50"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        cryptos = response.json()
        
        formatted_cryptos = [
            {
                'symbol': (c.get('symbol') or '').upper(),
                'price': c.get('current_price') or 0,
                'market_cap': c.get('market_cap') or 0,
                'change_24h': c.get('price_change_percentage_24h') or 0,
                'volume_24h': c.get('total_volume') or 0
            }
            for c in cryptos if c
        ]
        
        from src.agents.trade_advisor import analyze_best_trades
        trades = analyze_best_trades(formatted_cryptos)
        
        return jsonify({'success': True, 'trades': trades})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/compare', methods=['POST'])
def compare_cryptos_endpoint():
    """Compare multiple cryptos"""
    try:
        data = request.json
        crypto_ids = data.get('ids', [])
        
        if len(crypto_ids) < 2:
            return jsonify({'error': 'Need at least 2 cryptos to compare'}), 400
        
        cryptos = []
        for crypto_id in crypto_ids:
            url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={crypto_id}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            result = response.json()
            if result:
                c = result[0]
                cryptos.append({
                    'id': c.get('id', ''),
                    'symbol': (c.get('symbol') or '').upper(),
                    'price': c.get('current_price') or 0,
                    'market_cap': c.get('market_cap') or 0,
                    'change_24h': c.get('price_change_percentage_24h') or 0
                })
        
        from src.agents.comparison_agent import compare_cryptos
        comparison = compare_cryptos(cryptos)
        
        return jsonify({'success': True, 'comparison': comparison, 'cryptos': cryptos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/watchlist', methods=['GET', 'POST', 'DELETE'])
def watchlist():
    """Manage watchlist (stored in request - client handles localStorage)"""
    try:
        if request.method == 'POST':
            data = request.json
            return jsonify({'success': True, 'message': 'Added to watchlist'})
        elif request.method == 'DELETE':
            return jsonify({'success': True, 'message': 'Removed from watchlist'})
        else:
            return jsonify({'watchlist': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
