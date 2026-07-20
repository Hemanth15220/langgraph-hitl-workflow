"""
Workflow Graph: Orchestrates the content generation pipeline using LangGraph
"""

from langgraph.graph import StateGraph
from typing import TypedDict
from ..agents.trend_spotter import get_global_trends
from ..agents.content_creator import generate_content
from ..agents.hitl_node import human_review
from ..agents.poster import publish_content

class ContentState(TypedDict):
    """Shared state across all workflow nodes"""
    # From Trend-Spotter
    trends: Optional[dict]
    
    # From Content-Creator
    generated_content: Optional[list]
    
    # From HITL
    approved_content: Optional[dict]
    
    # From Poster
    publication_result: Optional[dict]

class ContentState(TypedDict):
    """State shared across all nodes in the workflow"""
    trends: dict
    generated_content: dict
    approved_content: dict
    publication_result: dict

def trend_spotter_node(state: ContentState) -> ContentState:
    """Wrapper for Trend-Spotter node"""
    trends = get_global_trends()
    state["trends"] = trends
    return state

def content_creator_node(state: ContentState) -> ContentState:
    """Wrapper for Content-Creator node"""
    generated = generate_content(state["trends"])
    state["generated_content"] = generated
    return state

def hitl_node(state: ContentState) -> ContentState:
    """Wrapper for HITL node"""
    approved = human_review(state["generated_content"])
    state["approved_content"] = approved
    return state

def poster_node(state: ContentState) -> ContentState:
    """Wrapper for Poster node"""
    result = publish_content(state["approved_content"])
    state["publication_result"] = result
    return state

def build_graph():
    """
    Build the main workflow graph with all nodes.
    
    Flow:
    START → Trend-Spotter → Content-Creator → HITL → Poster → END
    
    Returns:
        CompiledGraph: Compiled and ready-to-run state graph
    """
    graph = StateGraph(ContentState)
    
    # Add all nodes to the graph
    graph.add_node("trend_spotter", trend_spotter_node)
    graph.add_node("content_creator", content_creator_node)
    graph.add_node("hitl", hitl_node)
    graph.add_node("poster", poster_node)
    
    # Define the flow (edges between nodes)
    graph.add_edge("trend_spotter", "content_creator")
    graph.add_edge("content_creator", "hitl")
    graph.add_edge("hitl", "poster")
    graph.add_edge("poster", END)
    
    # Set entry point
    graph.set_entry_point("trend_spotter")
    
    # Compile the graph
    return graph.compile()



