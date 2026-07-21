from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any
import asyncio
from src.agents.risk_analyzer import analyze_risks
from src.agents.opportunity_finder import find_opportunities
from src.agents.comparison_agent import compare_cryptos
from src.agents.research_synthesizer import synthesize_research

class ResearchState(TypedDict):
    crypto: Dict[str, Any]
    risk_analysis: Dict[str, Any]
    opportunity_analysis: Dict[str, Any]
    research_synthesis: Dict[str, Any]

def run_risk_analyzer(state: ResearchState) -> ResearchState:
    """Run risk analysis"""
    crypto = state['crypto']
    volatility = abs(crypto.get('change_24h', 0))
    
    result = analyze_risks(
        crypto['name'],
        crypto['symbol'],
        crypto['price'],
        crypto['market_cap'],
        crypto['volume_24h'],
        volatility
    )
    
    state['risk_analysis'] = result
    return state

def run_opportunity_finder(state: ResearchState) -> ResearchState:
    """Run opportunity analysis"""
    crypto = state['crypto']
    
    result = find_opportunities(
        crypto['name'],
        crypto['symbol'],
        crypto['price'],
        crypto['market_cap'],
        crypto['change_24h'],
        crypto.get('ath', crypto['price']),
        crypto.get('atl', crypto['price'])
    )
    
    state['opportunity_analysis'] = result
    return state

def run_synthesizer(state: ResearchState) -> ResearchState:
    """Synthesize all research"""
    crypto = state['crypto']
    
    result = synthesize_research(
        crypto['name'],
        crypto['symbol'],
        crypto.get('description', 'N/A'),
        state.get('risk_analysis', {}),
        state.get('opportunity_analysis', {})
    )
    
    state['research_synthesis'] = result
    return state

def build_research_graph():
    """Build the research workflow graph"""
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("risk_analyzer", run_risk_analyzer)
    workflow.add_node("opportunity_finder", run_opportunity_finder)
    workflow.add_node("synthesizer", run_synthesizer)
    
    workflow.set_entry_point("risk_analyzer")
    
    workflow.add_edge("risk_analyzer", "opportunity_finder")
    workflow.add_edge("opportunity_finder", "synthesizer")
    workflow.add_edge("synthesizer", "__end__")
    
    return workflow.compile()

def run_research_workflow(crypto_data: Dict[str, Any]) -> Dict[str, Any]:
    """Run complete research workflow for a crypto"""
    graph = build_research_graph()
    
    initial_state = ResearchState(
        crypto=crypto_data,
        risk_analysis={},
        opportunity_analysis={},
        research_synthesis={}
    )
    
    final_state = graph.invoke(initial_state)
    
    return {
        'crypto': final_state['crypto'],
        'risk_analysis': final_state['risk_analysis'],
        'opportunity_analysis': final_state['opportunity_analysis'],
        'research_synthesis': final_state['research_synthesis']
    }
