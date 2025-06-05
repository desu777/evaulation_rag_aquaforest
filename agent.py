# agent.py v2 - Enhanced Evaluation RAG Agent with GPT Augmentation
from typing import Dict
from workflow import create_enhanced_evaluation_workflow_v2

class EnhancedEvaluationRAGAgentV2:
    def __init__(self):
        self.workflow = create_enhanced_evaluation_workflow_v2()
    
    def ask(self, user_query: str) -> Dict:
        """Ask with enhanced model-based evaluation + GPT augmentation + intent detection"""
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
            "company_context_added": False,
            # 🆕 NEW: Initialize augmentation state
            "best_partial_result": None,
            "best_partial_confidence": 0.0,
            "attempt_confidences": [],
            "has_usable_partial": False,
            "use_augmentation": False,
            "augmentation_used": False,
            "augmentation_confidence": 0.0,
            "augmentation_reasoning": ""
        }
        
        try:
            final_state = self.workflow.invoke(initial_state)
            
            # Enhanced response with augmentation info
            response = {
                "query": user_query,
                "answer": final_state["final_answer"],
                "attempts": final_state["attempt_count"],
                "model_confidence": final_state.get("model_confidence", 0.0),
                "evaluation_log": final_state["evaluation_log"],
                "escalated": final_state.get("escalate", False),
                "attempt_history": final_state["attempt_history"],
                "query_intent": final_state.get("query_intent", "general"),
                "business_type": final_state.get("business_type", "none"),
                "trade_secret_handled": final_state.get("requires_trade_secret_filter", False),
                # 🆕 NEW: Augmentation metrics
                "augmentation_used": final_state.get("augmentation_used", False),
                "augmentation_confidence": final_state.get("augmentation_confidence", 0.0),
                "best_partial_confidence": final_state.get("best_partial_confidence", 0.0),
                "attempt_confidences": final_state.get("attempt_confidences", []),
                "augmentation_reasoning": final_state.get("augmentation_reasoning", "")
            }
            
            # Print enhanced summary
            self._print_enhanced_summary(response)
            
            return response
            
        except Exception as e:
            return {
                "query": user_query,
                "answer": f"Błąd systemu Enhanced Evaluation RAG v2: {e}",
                "attempts": 0,
                "model_confidence": 0.0,
                "escalated": True,
                "evaluation_log": [f"System error: {e}"],
                "query_intent": "error",
                "business_type": "none",
                "trade_secret_handled": False,
                "augmentation_used": False,
                "augmentation_confidence": 0.0,
                "best_partial_confidence": 0.0,
                "attempt_confidences": [],
                "augmentation_reasoning": f"System error: {e}"
            }
    
    def _print_enhanced_summary(self, response: Dict):
        """Print enhanced summary with augmentation info"""
        print(f"\n{'='*50}")
        print(f"📊 ENHANCED RAG v2 SUMMARY")
        print(f"{'='*50}")
        print(f"🎯 Intent: {response['query_intent']} | Business: {response['business_type']}")
        print(f"🔄 Attempts: {response['attempts']}")
        print(f"📈 Confidences: {response['attempt_confidences']}")
        
        if response['augmentation_used']:
            print(f"🧠 GPT AUGMENTATION: ✅ USED")
            print(f"   - Best Partial: {response['best_partial_confidence']}/10")
            print(f"   - Final Confidence: {response['augmentation_confidence']}/10")
            print(f"   - Reasoning: {response['augmentation_reasoning']}")
        elif response['best_partial_confidence'] > 0:
            print(f"🧠 GPT AUGMENTATION: ❌ NOT USED")
            print(f"   - Had Partial: {response['best_partial_confidence']}/10")
            print(f"   - Reason: {response['augmentation_reasoning']}")
        else:
            print(f"🧠 GPT AUGMENTATION: ⚪ NOT APPLICABLE")
        
        print(f"📊 Final Confidence: {response['model_confidence']}/10")
        print(f"🔒 Trade Secret: {response['trade_secret_handled']}")
        print(f"⚠️ Escalated: {response['escalated']}")
        print(f"💬 Answer Length: {len(response['answer'])} chars")
        print(f"{'='*50}")

# Backward compatibility
class EnhancedEvaluationRAGAgent(EnhancedEvaluationRAGAgentV2):
    """Backward compatibility class"""
    def __init__(self):
        print("⚠️ Using legacy agent class - consider upgrading to EnhancedEvaluationRAGAgentV2")
        super().__init__()