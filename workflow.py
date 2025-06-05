# workflow.py v2 - Enhanced Workflow Builder with GPT Augmentation
from langgraph.graph import StateGraph, START, END
from state import EnhancedEvaluationRAGStateV2
from intent_detection import analyze_query_intent
from business_handlers import handle_business_query, check_trade_secrets

# Import original nodes we still need
from workflow_nodes import (
    execute_search_attempt,  # Keep original
    generate_evaluation_answer  # Keep original
)

# Import v2 nodes
from workflow_nodes import (
    initialize_evaluation_v2,
    enhanced_evaluate_content_quality_v2,
    gpt_augmentation_mode
)

def create_enhanced_evaluation_workflow_v2():
    """Create enhanced model evaluation-based workflow v2 with GPT augmentation"""
    workflow = StateGraph(EnhancedEvaluationRAGStateV2)
    
    # Add all nodes
    workflow.add_node("initialize_evaluation", initialize_evaluation_v2)
    workflow.add_node("analyze_query_intent", analyze_query_intent)
    workflow.add_node("handle_business_query", handle_business_query)
    workflow.add_node("check_trade_secrets", check_trade_secrets)
    workflow.add_node("execute_search_attempt", execute_search_attempt)
    workflow.add_node("enhanced_evaluate_content_quality", enhanced_evaluate_content_quality_v2)  # v2
    workflow.add_node("gpt_augmentation_mode", gpt_augmentation_mode)  # 🆕 NEW
    workflow.add_node("generate_evaluation_answer", generate_evaluation_answer)
    
    # Linear flow with enhanced routing
    workflow.add_edge(START, "initialize_evaluation")
    workflow.add_edge("initialize_evaluation", "analyze_query_intent")
    
    # Business query routing (unchanged)
    def business_or_trade_secrets(state: EnhancedEvaluationRAGStateV2) -> str:
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
    
    # 🆕 ENHANCED CONDITIONAL ROUTING with augmentation
    def continue_augment_or_finish(state: EnhancedEvaluationRAGStateV2) -> str:
        """Enhanced routing logic with GPT augmentation path"""
        
        # Continue attempts if needed
        if state.get("should_continue"):
            return "execute_search_attempt"
        
        # 🆕 NEW: GPT Augmentation path
        elif state.get("use_augmentation"):
            return "gpt_augmentation_mode"
        
        # Standard finish path
        else:
            return "generate_evaluation_answer"
    
    workflow.add_conditional_edges(
        "enhanced_evaluate_content_quality",
        continue_augment_or_finish,
        {
            "execute_search_attempt": "execute_search_attempt",      # Loop back for next attempt
            "gpt_augmentation_mode": "gpt_augmentation_mode",        # 🆕 Augmentation path
            "generate_evaluation_answer": "generate_evaluation_answer"  # Standard finish
        }
    )
    
    # Augmentation leads directly to END (it sets final_answer)
    workflow.add_edge("gpt_augmentation_mode", END)
    workflow.add_edge("generate_evaluation_answer", END)
    
    return workflow.compile()

# Create workflow instance for backward compatibility
def create_enhanced_evaluation_workflow():
    """Backward compatibility wrapper"""
    print("⚠️ Using legacy workflow name - consider upgrading to create_enhanced_evaluation_workflow_v2()")
    return create_enhanced_evaluation_workflow_v2()