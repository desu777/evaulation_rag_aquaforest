# state.py v2 - Enhanced State Definitions with GPT Augmentation
from typing import List, Dict, TypedDict, Annotated, Optional
import operator

# === ENHANCED EVALUATION STATE DEFINITION V2 ===
class EnhancedEvaluationRAGStateV2(TypedDict):
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
    
    # Intent & Business Logic
    query_intent: str  # "dosage", "business", "production", "general", "problem_solving"
    business_type: str  # "partnership", "distribution", "technical_support", "none"
    requires_trade_secret_filter: bool
    confidence_threshold_override: float
    company_context_added: bool
    
    # 🆕 NEW: GPT Augmentation Features
    best_partial_result: Optional[Dict]  # Best result with confidence 5.0+
    best_partial_confidence: float  # Confidence of best partial result
    attempt_confidences: Annotated[List[float], operator.add]  # Track all confidences
    has_usable_partial: bool  # Flag for augmentation eligibility
    use_augmentation: bool  # Trigger augmentation mode
    augmentation_used: bool  # Track if augmentation was applied
    augmentation_confidence: float  # Final augmented confidence
    augmentation_reasoning: str  # Why augmentation was used/failed