# agent.py v3 - Enhanced Evaluation RAG Agent with Dynamic Optimization
from typing import Dict, List
from workflow import create_enhanced_evaluation_workflow_v2

class EnhancedEvaluationRAGAgentV2:
    def __init__(self):
        self.workflow = create_enhanced_evaluation_workflow_v2()
    
    def ask(self, user_query: str) -> Dict:
        """Ask with enhanced model-based evaluation + GPT augmentation + Dynamic Optimization"""
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
            # GPT Augmentation state (v2)
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
            
            # Enhanced response with dynamic optimization info
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
                # GPT Augmentation metrics (v2)
                "augmentation_used": final_state.get("augmentation_used", False),
                "augmentation_confidence": final_state.get("augmentation_confidence", 0.0),
                "best_partial_confidence": final_state.get("best_partial_confidence", 0.0),
                "attempt_confidences": final_state.get("attempt_confidences", []),
                "augmentation_reasoning": final_state.get("augmentation_reasoning", ""),
                # 🆕 NEW: Dynamic Optimization metrics
                "optimization_performance": self._analyze_optimization_performance(final_state),
                "semantic_enhancement": self._analyze_semantic_enhancement(final_state),
                "query_evolution": self._extract_query_evolution(final_state)
            }
            
            # Print enhanced summary with dynamic optimization
            self._print_enhanced_summary(response)
            
            return response
            
        except Exception as e:
            return {
                "query": user_query,
                "answer": f"Błąd systemu Enhanced Evaluation RAG v3: {e}",
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
                "augmentation_reasoning": f"System error: {e}",
                "optimization_performance": {"error": str(e)},
                "semantic_enhancement": {"error": str(e)},
                "query_evolution": []
            }
    
    def _analyze_optimization_performance(self, final_state: Dict) -> Dict:
        """🚀 Analyze dynamic optimization performance"""
        attempt_history = final_state.get("attempt_history", [])
        
        if not attempt_history:
            return {"status": "no_attempts", "performance": "unknown"}
        
        # Count dynamic optimizations
        dynamic_attempts = sum(1 for attempt in attempt_history 
                             if attempt.get("optimization_type") == "dynamic_llm_based")
        
        # Analyze query transformations
        transformations = [attempt.get("optimized_query", "") for attempt in attempt_history]
        unique_transformations = len(set(transformations))
        
        # Performance assessment
        if dynamic_attempts == len(attempt_history):
            status = "full_dynamic"
        elif dynamic_attempts > 0:
            status = "partial_dynamic"
        else:
            status = "static_fallback"
        
        return {
            "status": status,
            "dynamic_attempts": dynamic_attempts,
            "total_attempts": len(attempt_history),
            "unique_transformations": unique_transformations,
            "performance": "excellent" if dynamic_attempts == len(attempt_history) else "mixed"
        }
    
    def _analyze_semantic_enhancement(self, final_state: Dict) -> Dict:
        """🎯 Analyze semantic enhancement quality"""
        attempt_history = final_state.get("attempt_history", [])
        original_query = final_state.get("original_query", "")
        
        if not attempt_history:
            return {"quality": "no_data", "enhancement_detected": False}
        
        # Analyze semantic expansion
        original_words = set(original_query.lower().split())
        enhanced_words = set()
        
        for attempt in attempt_history:
            optimized_query = attempt.get("optimized_query", "")
            enhanced_words.update(optimized_query.lower().split())
        
        new_semantic_words = enhanced_words - original_words
        enhancement_ratio = len(new_semantic_words) / len(original_words) if original_words else 0
        
        # Quality assessment
        if enhancement_ratio > 1.5:
            quality = "excellent"
        elif enhancement_ratio > 1.0:
            quality = "good"
        elif enhancement_ratio > 0.5:
            quality = "moderate"
        else:
            quality = "minimal"
        
        return {
            "quality": quality,
            "enhancement_ratio": round(enhancement_ratio, 2),
            "new_semantic_words": len(new_semantic_words),
            "enhancement_detected": enhancement_ratio > 0.3,
            "sample_enhancements": list(new_semantic_words)[:5]
        }
    
    def _extract_query_evolution(self, final_state: Dict) -> List[Dict]:
        """🔄 Extract query evolution pathway"""
        attempt_history = final_state.get("attempt_history", [])
        attempt_confidences = final_state.get("attempt_confidences", [])
        
        evolution = []
        for i, attempt in enumerate(attempt_history):
            confidence = attempt_confidences[i] if i < len(attempt_confidences) else 0.0
            evolution.append({
                "attempt": attempt.get("attempt", i+1),
                "query": attempt.get("optimized_query", ""),
                "confidence": confidence,
                "optimization_type": attempt.get("optimization_type", "unknown"),
                "results_count": attempt.get("results_count", 0)
            })
        
        return evolution
    
    def _print_enhanced_summary(self, response: Dict):
        """Print enhanced summary with dynamic optimization info"""
        print(f"\n{'='*50}")
        print(f"📊 ENHANCED RAG v3 SUMMARY")
        print(f"{'='*50}")
        print(f"🎯 Intent: {response['query_intent']} | Business: {response['business_type']}")
        print(f"🔄 Attempts: {response['attempts']}")
        print(f"📈 Confidences: {response['attempt_confidences']}")
        
        # 🆕 Dynamic Optimization Summary
        opt_perf = response.get('optimization_performance', {})
        semantic_enh = response.get('semantic_enhancement', {})
        
        print(f"🚀 DYNAMIC OPTIMIZATION: {opt_perf.get('status', 'unknown').upper()}")
        print(f"   - Dynamic attempts: {opt_perf.get('dynamic_attempts', 0)}/{opt_perf.get('total_attempts', 0)}")
        print(f"   - Semantic quality: {semantic_enh.get('quality', 'unknown')}")
        print(f"   - Enhancement ratio: {semantic_enh.get('enhancement_ratio', 0)}")
        if semantic_enh.get('sample_enhancements'):
            print(f"   - Sample enhancements: {', '.join(semantic_enh['sample_enhancements'][:3])}")
        
        # GPT Augmentation Summary
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
        
        # Query Evolution Summary
        query_evolution = response.get('query_evolution', [])
        if query_evolution:
            print(f"\n🔄 QUERY EVOLUTION:")
            for i, evolution in enumerate(query_evolution):
                opt_type = evolution.get('optimization_type', 'unknown')
                confidence = evolution.get('confidence', 0)
                query_preview = evolution.get('query', '')[:50] + '...' if len(evolution.get('query', '')) > 50 else evolution.get('query', '')
                print(f"   {i+1}. [{opt_type}] '{query_preview}' → {confidence}/10")
        
        print(f"{'='*50}")

# Backward compatibility
class EnhancedEvaluationRAGAgent(EnhancedEvaluationRAGAgentV2):
    """Backward compatibility class"""
    def __init__(self):
        print("⚠️ Using legacy agent class - consider upgrading to EnhancedEvaluationRAGAgentV2")
        super().__init__()