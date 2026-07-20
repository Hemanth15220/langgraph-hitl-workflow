"""
Poster Node: Publishes approved content to Twitter/X
"""

import requests
from typing import Dict, Any
from ..config import TWITTER_BEARER_TOKEN

def publish_content(approved_content: Dict[str, Any]) -> Dict[str, Any]:
    """
    Publish approved content to Twitter/X API.
    
    Args:
        approved_content (dict): Approved post from HITL node
        
    Returns:
        dict: Publication result with tweet ID and status
    """
    try:
        if not approved_content or not approved_content.get("approved_posts"):
            return {
                "success": False,
                "error": "No approved content to publish",
                "tweet_id": None
            }
        
        # Get the first approved post
        post = approved_content["approved_posts"][0]
        tweet_text = post.get("content", "")
        
        # Twitter API endpoint
        url = "https://api.twitter.com/2/tweets"
        
        # Bearer Token authentication
        headers = {
            "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        
        # Tweet payload
        payload = {
            "text": tweet_text
        }
        
        # Make request
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 201:
            # Success
            data = response.json()
            return {
                "success": True,
                "tweet_id": data.get("data", {}).get("id"),
                "text": tweet_text,
                "status": "published"
            }
        else:
            # Failure
            return {
                "success": False,
                "error": f"Twitter API error: {response.status_code}",
                "response": response.text,
                "tweet_id": None
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "tweet_id": None
        }
