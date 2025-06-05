# intent_detection.py - Enhanced Intent Analysis with LLM Support
from state import EnhancedEvaluationRAGStateV2
from dynamic_query_optimizer import DynamicQueryOptimizer

# Lazy initialization to avoid import-time API key issues
_dynamic_optimizer = None

def get_dynamic_optimizer():
    """Get or create dynamic optimizer instance"""
    global _dynamic_optimizer
    if _dynamic_optimizer is None:
        try:
            _dynamic_optimizer = DynamicQueryOptimizer()
        except Exception as e:
            print(f"⚠️ Warning: Dynamic optimizer initialization failed: {e}")
            return None
    return _dynamic_optimizer

def analyze_query_intent(state: EnhancedEvaluationRAGStateV2) -> EnhancedEvaluationRAGStateV2:
    """
    🎯 ENHANCED INTENT DETECTION with LLM support for edge cases
    
    Combines pattern-based detection with LLM reasoning for complex queries
    """
    
    query = state['original_query'].lower()
    intent = "general"
    business_type = "none"
    trade_secret = False
    threshold = 7.0
    
    # 🔍 PATTERN-BASED DETECTION (fast for common cases)
    # Business patterns
    business_patterns = [
        "współpraca", "dystrybucja", "partnership", "zostać dystrybutorem", 
        "nawiązać współpracę", "przedstawiciel", "dealer", "sprzedaż hurtowa",
        "wholesale", "biznes", "firma", "współpracować", "dołączyć",
        "reprezentować", "sprzedawać produkty"
    ]
    
    if any(phrase in query for phrase in business_patterns):
        intent = "business"
        business_type = "partnership"
        threshold = 9.0  # High threshold for business
        
    # Trade secret patterns  
    production_patterns = [
        "jak powstaje", "jak jest produkowany", "sposób produkcji", 
        "receptura", "skład szczegółowy", "jak wytwarzany", "proces produkcji",
        "jak robią", "jak się robi", "technologia", "metoda produkcji",
        "składniki dokładne", "jak tworzy", "jak wytwarza"
    ]
    
    if any(phrase in query for phrase in production_patterns):
        intent = "production" 
        trade_secret = True
        threshold = 5.0  # Will be handled by trade secret filter
        
    # Dosage patterns
    dosage_patterns = [
        "dawkowanie", "dawka", "ile", "jak stosować", "dozowanie", 
        "aplikacja", "ile ml", "proporcje", "stosunek", "jak używać",
        "częstotliwość", "jak często", "ilość", "miara", "porcja"
    ]
    
    if any(phrase in query for phrase in dosage_patterns):
        intent = "dosage"
        threshold = 6.0  # Lower threshold, will use fallback
        
    # Problem solving patterns
    problem_patterns = [
        "problem", "jak pozbyć", "jak usunąć", "jak obniżyć", 
        "co robić", "porada", "rozwiązanie", "pomoc", "jak walczyć",
        "jak zlikwidować", "jak zapobiec", "jak leczyć", "ratunku"
    ]
    
    if any(phrase in query for phrase in problem_patterns):
        intent = "troubleshooting"
        threshold = 6.5
        
    # Support patterns
    support_patterns = [
        "pomoc", "wsparcie", "nie działa", "błąd", "awaria",
        "nie wiem", "jak zacząć", "porady", "instrukcja"
    ]
    
    if any(phrase in query for phrase in support_patterns):
        intent = "support"
        business_type = "technical_support"
        threshold = 6.5
    
    # 🧠 ENHANCED LLM DETECTION for ambiguous cases
    if intent == "general":
        print(f"🧠 Using LLM for ambiguous intent detection...")
        dynamic_optimizer = get_dynamic_optimizer()
        
        if dynamic_optimizer is not None:
            try:
                llm_intent = dynamic_optimizer.detect_intent_with_llm(state['original_query'])
                
                # Map LLM intents to our system intents with thresholds
                intent_mapping = {
                    "technical": ("technical", 6.5),
                    "product": ("product_info", 7.0),
                    "troubleshooting": ("troubleshooting", 6.5),
                    "setup": ("setup", 6.0),
                    "maintenance": ("maintenance", 6.5),
                    "general": ("general", 7.0)
                }
                
                if llm_intent in intent_mapping:
                    intent, threshold = intent_mapping[llm_intent]
                else:
                    intent = "general"
                    threshold = 7.0
                
                print(f"🎯 LLM detected intent: {llm_intent} → mapped to: {intent}")
            except Exception as e:
                print(f"⚠️ LLM intent detection failed: {e}")
                intent = "general"
                threshold = 7.0
        else:
            print(f"⚠️ Dynamic optimizer not available, using general intent")
            intent = "general"
            threshold = 7.0
    
    print(f"🎯 Enhanced Intent Detection:")
    print(f"   📝 Query: '{state['original_query']}'")
    print(f"   🎯 Intent: {intent}")
    print(f"   🏢 Business: {business_type}")
    print(f"   🔒 Trade Secret: {trade_secret}")
    print(f"   📊 Threshold: {threshold}")
    
    return {
        **state,
        "query_intent": intent,
        "business_type": business_type,
        "requires_trade_secret_filter": trade_secret,
        "confidence_threshold_override": threshold,
        "company_context_added": True
    }