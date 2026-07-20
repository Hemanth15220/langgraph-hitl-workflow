"""
Human-in-the-Loop (HITL) Node: Pauses execution for human review and approval
"""

from typing import Dict, List, Any

def human_review(generated_content: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Placeholder for human review and approval of generated content.
    
    In production, this would use LangGraph's interrupt() to pause execution
    and wait for human input. For now, returns approved content for demo.
    
    Args:
        generated_content (list): Generated posts from Content Creator node
        
    Returns:
        dict: Approved content with human decision metadata
    """
    if not generated_content:
        return {
            "approved_posts": [],
            "status": "rejected",
            "reason": "No content to review"
        }
    
    # For demo: auto-approve first post (in production, human would decide)
    selected_post = generated_content[0]
    
    return {
        "approved_posts": [selected_post],
        "status": "approved",
        "reason": "Human approved",
        "selected_index": 0
    }


def display_for_review(posts: List[Dict[str, str]]) -> str:
    """
    Format posts for human review display.
    
    Args:
        posts (list): Posts to display
        
    Returns:
        str: Formatted display string
    """
    display = "\n" + "="*60 + "\n"
    display += "🔍 HUMAN REVIEW - Generated Social Media Posts\n"
    display += "="*60 + "\n\n"
    
    for i, post in enumerate(posts, 1):
        display += f"Post {i}:\n"
        display += f"Content: {post.get('content', 'N/A')}\n"
        display += f"Platform: {post.get('platform', 'twitter')}\n"
        display += "-" * 60 + "\n\n"
    
    return display
