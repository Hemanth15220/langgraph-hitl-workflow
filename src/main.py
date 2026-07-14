"""
Main entry point for the LangGraph HITL Workflow
"""

from workflow.graph import build_graph

def main():
    """Initialize and run the content generation workflow"""
    print("🚀 Starting LangGraph HITL Workflow...")
    
    # Build the workflow graph
    graph = build_graph()
    print("✅ Workflow graph built successfully")
    
    # TODO: Initialize state and execute the graph
    # - Set up initial state with empty/default values
    # - Run graph.invoke() with the state
    # - Handle streaming updates if needed
    # - Log results

if __name__ == "__main__":
    main()
