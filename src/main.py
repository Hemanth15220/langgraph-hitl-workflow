"""
Main entry point for the LangGraph HITL Workflow
"""

import json
from src.workflow.graph import build_graph

def main():
    """Initialize and run the content generation workflow"""
    print("\n" + "="*60)
    print("🚀 LangGraph HITL Workflow - Starting")
    print("="*60 + "\n")
    
    try:
        # Build the workflow graph
        print("📊 Building workflow graph...")
        graph = build_graph()
        print("✅ Graph built successfully\n")
        
        # Initialize state
        initial_state = {
            "trends": None,
            "generated_content": None,
            "approved_content": None,
            "publication_result": None
        }
        
        # Run the graph
        print("▶️  Executing workflow...\n")
        result = graph.invoke(initial_state)
        
        # Display results
        print("\n" + "="*60)
        print("📋 WORKFLOW RESULTS")
        print("="*60 + "\n")
        
        # Trends
        if result.get("trends"):
            print("🎬 Trends Found:")
            trends = result["trends"].get("trending_films", [])
            for film in trends[:3]:
                print(f"  - {film.get('title')} (Rating: {film.get('rating')}/10)")
            print()
        
        # Generated Content
        if result.get("generated_content"):
            print("✍️  Generated Posts:")
            posts = result["generated_content"]
            for i, post in enumerate(posts[:3], 1):
                print(f"  Post {i}: {post.get('content', 'N/A')[:80]}...")
            print()
        
        # Approved Content
        if result.get("approved_content"):
            print("✅ Approved Content:")
            approved = result["approved_content"].get("approved_posts", [])
            if approved:
                print(f"  Status: {result['approved_content'].get('status', 'N/A')}")
                print(f"  Content: {approved[0].get('content', 'N/A')[:80]}...")
            print()
        
        # Publication Result
        if result.get("publication_result"):
            pub = result["publication_result"]
            print("📤 Publication Result:")
            print(f"  Success: {pub.get('success', False)}")
            if pub.get('tweet_id'):
                print(f"  Tweet ID: {pub.get('tweet_id')}")
            if pub.get('error'):
                print(f"  Error: {pub.get('error')}")
            print()
        
        print("="*60)
        print("✅ Workflow completed successfully!")
        print("="*60 + "\n")
        
        return result
    
    except Exception as e:
        print(f"\n❌ Error during workflow execution: {e}\n")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()
