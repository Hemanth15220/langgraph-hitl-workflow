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
        
        prompt = f"""You're a casual Redditor who loves movies and wants to start discussions about trending films.

Based on these trending films right now:
{film_list}

Write 3 casual Reddit post titles/content (like you're sharing with friends on r/FilmTrendBot):
- Keep it conversational and natural
- Use Reddit style (e.g., "Just watched...", "Has anyone seen...", "TIL...", etc.)
- Add emojis naturally (not forced)
- Make people want to discuss/comment

Format your response as:
Post 1: [casual title/content]
Post 2: [casual title/content]
Post 3: [casual title/content]
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
