# agent.py - Enhanced Evaluation RAG Agent
from typing import Dict
from workflow import create_enhanced_evaluation_workflow

class EnhancedEvaluationRAGAgent:
    def __init__(self):
        self.workflow = create_enhanced_evaluation_workflow()
    
    def ask(self, user_query: str) -> Dict:
        """Ask with enhanced model-based evaluation + intent detection"""
        print(f"\n💬 User: {user_query}")
        print("=" * 70)
        
        initial_state = {
            "original_query": user_query,
            "current_query": "",
            "attempt_count": 0,
            "attempt_history": [],
            "search_results": [],
            "model_confidence": 0.0,
            "all_results": [],
            "evaluation_log": [],
            "final_answer": "",
            "should_continue": True,
            "escalate": False,
            "query_intent": "general",
            "business_type": "none",
            "requires_trade_secret_filter": False,
            "confidence_threshold_override": 7.0,
            "company_context_added": False
        }
        
        try:
            final_state = self.workflow.invoke(initial_state)
            
            return {
                "query": user_query,
                "answer": final_state["final_answer"],
                "attempts": final_state["attempt_count"],
                "model_confidence": final_state.get("model_confidence", 0.0),
                "evaluation_log": final_state["evaluation_log"],
                "escalated": final_state.get("escalate", False),
                "attempt_history": final_state["attempt_history"],
                "query_intent": final_state.get("query_intent", "general"),
                "business_type": final_state.get("business_type", "none"),
                "trade_secret_handled": final_state.get("requires_trade_secret_filter", False)
            }
            
        except Exception as e:
            return {
                "query": user_query,
                "answer": f"Błąd systemu Enhanced Evaluation RAG: {e}",
                "attempts": 0,
                "model_confidence": 0.0,
                "escalated": True,
                "evaluation_log": [f"System error: {e}"],
                "query_intent": "error",
                "business_type": "none",
                "trade_secret_handled": False
            }