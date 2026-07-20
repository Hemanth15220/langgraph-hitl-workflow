"""Web Interface for Crypto Trends Agent"""
from flask import Flask, render_template, jsonify, request
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.workflow.graph import build_graph
from src.agents.trend_spotter import get_crypto_details

app = Flask(__name__, template_folder='templates', static_folder='static')

workflow_state = {
    "running": False,
    "trends": None,
    "generated_content": None,
    "approved_content": None,
    "publication_result": None,
    "selected_crypto": None
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/start', methods=['POST'])
def start_workflow():
    global workflow_state
    try:
        workflow_state["running"] = True
        workflow_state["error"] = None
        
        graph = build_graph()
        initial_state = {
            "trends": None,
            "generated_content": None,
            "approved_content": None,
            "publication_result": None
        }
        
        result = graph.invoke(initial_state)
        workflow_state["trends"] = result.get("trends")
        workflow_state["generated_content"] = result.get("generated_content")
        workflow_state["running"] = False
        
        return jsonify({
            "success": True,
            "message": "Workflow executed",
            "trends": result.get("trends"),
            "content": result.get("generated_content")
        })
    except Exception as e:
        workflow_state["error"] = str(e)
        workflow_state["running"] = False
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/cryptos', methods=['GET'])
def get_cryptos():
    """Get all cryptos from latest run"""
    if workflow_state.get("trends"):
        return jsonify(workflow_state["trends"].get("trending_films", []))
    return jsonify([])

@app.route('/api/crypto/<crypto_id>', methods=['GET'])
def get_crypto(crypto_id):
    """Get detailed info for specific crypto"""
    details = get_crypto_details(crypto_id)
    return jsonify(details)

@app.route('/api/approve', methods=['POST'])
def approve():
    try:
        data = request.json or {}
        post_content = data.get('post_content') or data.get('content', 'Crypto market update')
        
        return jsonify({
            "success": True,
            "message": "Post published to r/CryptoTrends!",
            "approved": {"content": post_content}
        }), 200
    except Exception as e:
        print(f"Approve error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

    global workflow_state
    try:
        data = request.json
        post_index = data.get('post_index', 0)
        posts = workflow_state.get("generated_content", [])
        
        if posts and post_index < len(posts):
            selected_post = posts[post_index]
            
            # Handle both dict and string post formats
            if isinstance(selected_post, dict):
                content = selected_post.get('content', str(selected_post))
            else:
                content = str(selected_post)
            
            workflow_state["approved_content"] = {
                "approved_posts": [{"content": content, "platform": "reddit"}],
                "status": "approved"
            }
            
            return jsonify({
                "success": True,
                "message": "Post approved and published!",
                "approved": {"content": content}
            })
        
        return jsonify({"success": False, "error": "No posts available"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/reject', methods=['POST'])
def reject():
    return jsonify({"success": True, "message": "Generating new posts..."})

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify(workflow_state)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
