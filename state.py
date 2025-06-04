# state.py - State Definitions
from typing import List, Dict, TypedDict, Annotated
import operator

# === ENHANCED EVALUATION STATE DEFINITION ===
class EnhancedEvaluationRAGState(TypedDict):
    # Input
    original_query: str
    current_query: str
    
    # Multi-attempt tracking
    attempt_count: int
    attempt_history: Annotated[List[Dict], operator.add]
    
    # Search results per attempt
    search_results: List[Dict]
    model_confidence: float
    all_results: Annotated[List[List[Dict]], operator.add]
    
    # Evaluation logs
    evaluation_log: Annotated[List[str], operator.add]
    
    # Output control
    final_answer: str
    should_continue: bool
    escalate: bool
    
    # NEW: Intent & Business Logic
    query_intent: str  # "dosage", "business", "production", "general", "problem_solving"
    business_type: str  # "partnership", "distribution", "technical_support", "none"
    requires_trade_secret_filter: bool
    confidence_threshold_override: float
    company_context_added: bool