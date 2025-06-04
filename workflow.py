# workflow.py - Enhanced Workflow Builder
from langgraph.graph import StateGraph, START, END
from state import EnhancedEvaluationRAGState
from intent_detection import analyze_query_intent
from business_handlers import handle_business_query, check_trade_secrets
from workflow_nodes import (
    initialize_evaluation,
    execute_search_attempt,
    enhanced_evaluate_content_quality,
    generate_evaluation_answer
)

def create_enhanced_evaluation_workflow():
    """Create enhanced model evaluation-based workflow"""
    workflow = StateGraph(EnhancedEvaluationRAGState)
    
    # Add all nodes
    workflow.add_node("initialize_evaluation", initialize_evaluation)
    workflow.add_node("analyze_query_intent", analyze_query_intent)
    workflow.add_node("handle_business_query", handle_business_query)
    workflow.add_node("check_trade_secrets", check_trade_secrets)
    workflow.add_node("execute_search_attempt", execute_search_attempt)
    workflow.add_node("enhanced_evaluate_content_quality", enhanced_evaluate_content_quality)
    workflow.add_node("generate_evaluation_answer", generate_evaluation_answer)
    
    # Linear flow with enhanced routing
    workflow.add_edge(START, "initialize_evaluation")
    workflow.add_edge("initialize_evaluation", "analyze_query_intent")
    
    # Business query routing
    def business_or_trade_secrets(state: EnhancedEvaluationRAGState) -> str:
        if state["business_type"] in ["partnership", "technical_support"]:
            return "handle_business_query"
        elif state.get("requires_trade_secret_filter"):
            return "check_trade_secrets"
        else:
            return "execute_search_attempt"
    
    workflow.add_conditional_edges(
        "analyze_query_intent",
        business_or_trade_secrets,
        {
            "handle_business_query": "handle_business_query",
            "check_trade_secrets": "check_trade_secrets",
            "execute_search_attempt": "execute_search_attempt"
        }
    )
    
    # Business and trade secret responses go directly to END
    workflow.add_edge("handle_business_query", END)
    workflow.add_edge("check_trade_secrets", END)
    
    # Search flow continues
    workflow.add_edge("execute_search_attempt", "enhanced_evaluate_content_quality")
    
    # Conditional routing from evaluation (with loop for multiple attempts)
    def continue_or_finish(state: EnhancedEvaluationRAGState) -> str:
        if state.get("should_continue"):
            return "execute_search_attempt"  # Loop back for next attempt
        else:
            return "generate_evaluation_answer"  # Finish
    
    workflow.add_conditional_edges(
        "enhanced_evaluate_content_quality",
        continue_or_finish,
        {
            "execute_search_attempt": "execute_search_attempt",
            "generate_evaluation_answer": "generate_evaluation_answer"
        }
    )
    
    workflow.add_edge("generate_evaluation_answer", END)
    
    return workflow.compile()