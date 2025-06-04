# intent_detection.py - Smart Intent Analysis
from state import EnhancedEvaluationRAGState

def analyze_query_intent(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Smart intent detection with pattern matching"""
    
    query = state['original_query'].lower()
    
    # Pattern-based detection (faster than LLM)
    intent = "general"
    business_type = "none"
    trade_secret = False
    threshold = 7.0
    
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
        intent = "problem_solving"
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
    
    print(f"🎯 Detected intent: {intent}, business: {business_type}, trade_secret: {trade_secret}")
    
    return {
        **state,
        "query_intent": intent,
        "business_type": business_type,
        "requires_trade_secret_filter": trade_secret,
        "confidence_threshold_override": threshold,
        "company_context_added": True
    }