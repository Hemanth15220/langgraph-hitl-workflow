"""
Content Creator Node: Synthesizes trend data into engaging social media posts
"""

from groq import Groq
from typing import Dict, List, Any
from ..config import GROQ_API_KEY, GROQ_MODEL

def generate_content(trends: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Generate engaging social media posts from film trends using Groq LLM.
    
    Args:
        trends (dict): Trend data from Trend-Spotter node
        
    Returns:
        list: List of generated posts with content and metadata
    """
    try:
        # Initialize Groq client
        client = Groq(api_key=GROQ_API_KEY)
        
        # Extract film titles and data
        films = trends.get("trending_films", [])
        if not films:
            return []
        
        # Create a prompt for the LLM
        film_list = "\n".join([f"- {f['title']} (Rating: {f['rating']}/10)" for f in films[:3]])
        
        prompt = f"""You are a creative social media manager specializing in film entertainment content.

Based on these trending films right now:
{film_list}

Generate 3 short, engaging Twitter-style posts (max 280 characters each) that:
1. Are catchy and appeal to film enthusiasts worldwide
2. Use emojis appropriately (1-2 per post)
3. Create curiosity or excitement about cinema
4. Are natural and conversational

Format your response as:
Post 1: [content]
Post 2: [content]
Post 3: [content]
"""
        
        # Call Groq API using chat.completions
        chat_completion = client.chat.completions.create(
            model=GROQ_MODEL,
            max_tokens=500,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        # Parse response
        response_text = chat_completion.choices[0].message.content
        posts = parse_posts(response_text)
        
        return posts
    
    except Exception as e:
        print(f"Error generating content: {e}")
        return []


def parse_posts(response_text: str) -> List[Dict[str, str]]:
    """
    Parse LLM response into structured post data.
    
    Args:
        response_text (str): Raw response from LLM
        
    Returns:
        list: List of posts with content and metadata
    """
    posts = []
    lines = response_text.split("\n")
    
    for line in lines:
        if line.strip().startswith("Post"):
            # Extract content after the colon
            content = line.split(":", 1)[-1].strip()
            if content:
                posts.append({
                    "content": content,
                    "platform": "twitter",
                    "character_count": len(content)
                })
    
    return posts if posts else [{"content": "Check out the trending films this week!", "platform": "twitter", "character_count": 0}]
