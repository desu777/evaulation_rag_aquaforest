# workflow_nodes.py - Core Workflow Nodes
from datetime import datetime
from langchain_core.messages import SystemMessage
from state import EnhancedEvaluationRAGState
from components import EvaluationRAGComponents
from config import ENHANCED_AQUAFOREST_EXPERT_PROMPT, MAX_REASONING_ATTEMPTS, CONFIDENCE_THRESHOLDS

# Initialize components
components = EvaluationRAGComponents()

def preprocess_query(query: str) -> str:
    """Czyszczenie i normalizacja zapytania"""
    
    # Popraw częste błędy i niejasności
    replacements = {
        "component a": "component strong a",
        "component b": "component strong b", 
        "component c": "component strong c",
        "component 1 2 3": "component 1+2+3",
        "component 123": "component 1+2+3",
        "af power": "af power elixir",
        "probios": "pro bio s",
        "probio": "pro bio",
        "kh+": "kh plus",
        "ca+": "ca plus",
        "mg+": "mg plus",
        "reef salt+": "reef salt plus",
        "ocean guard": "oceanguard",
        "icp test": "af test icp",
        " sps ": " koralowce sps ",
        " lps ": " koralowce lps "
    }
    
    query_lower = query.lower()
    
    # Zastosuj poprawki
    for old, new in replacements.items():
        query_lower = query_lower.replace(old, new)
    
    # Usuń podwójne spacje
    query_lower = " ".join(query_lower.split())
        
    return query_lower

def initialize_evaluation(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Node 1: Initialize evaluation with preprocessing"""
    
    # Preprocess query to fix common issues
    original_query = state["original_query"]
    preprocessed_query = preprocess_query(original_query)
    
    if preprocessed_query != original_query.lower():
        print(f"🔧 Query preprocessed: '{original_query}' → '{preprocessed_query}'")
    
    print(f"\n🏁 STARTING Enhanced Model Evaluation")
    print(f"📝 Query: {preprocessed_query}")
    
    return {
        **state,
        "original_query": preprocessed_query,  # Use preprocessed version
        "current_query": "",
        "attempt_count": 0,
        "attempt_history": [],
        "search_results": [],
        "model_confidence": 0.0,
        "all_results": [],
        "evaluation_log": [f"Starting evaluation for: '{preprocessed_query}'"],
        "final_answer": "",
        "should_continue": True,
        "escalate": False
    }

def execute_search_attempt(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Node 2: Execute search with improved query optimization"""
    attempt = state["attempt_count"] + 1
    print(f"\n🔍 ATTEMPT {attempt}/3")
    
    # Get previous evaluations for context
    previous_evaluations = state["evaluation_log"]
    
    # Optimize query for this attempt - MUCH simpler now
    optimized_query = components.optimize_query_for_attempt(
        state['original_query'], 
        attempt, 
        previous_evaluations
    )
    
    print(f"🔧 Query: {optimized_query}")
    
    # Search with optimized query and dynamic top_k
    results = components.search_knowledge(optimized_query, attempt=attempt)
    
    print(f"📊 Found {len(results)} results")
    
    # Log attempt details
    attempt_info = {
        "attempt": attempt,
        "query": optimized_query,
        "results_count": len(results),
        "timestamp": datetime.now().isoformat()
    }
    
    evaluation_entry = f"Attempt {attempt}: '{optimized_query}' → {len(results)} results found"
    
    return {
        **state,
        "current_query": optimized_query,
        "attempt_count": attempt,
        "search_results": results,
        "attempt_history": state["attempt_history"] + [attempt_info],
        "all_results": state["all_results"] + [results],
        "evaluation_log": state["evaluation_log"] + [evaluation_entry]
    }

def enhanced_evaluate_content_quality(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Node 3: Enhanced evaluation with smart fallbacks and dynamic thresholds"""
    attempt = state["attempt_count"]
    results = state["search_results"]
    
    print(f"🤖 Model evaluating content quality...")
    
    # Get dynamic threshold based on intent - NEW!
    query_intent = state.get("query_intent", "general")
    confidence_threshold = CONFIDENCE_THRESHOLDS.get(query_intent, 7.0)
    
    # Override if manually set (business/trade secrets use custom thresholds)
    if "confidence_threshold_override" in state:
        confidence_threshold = state["confidence_threshold_override"]
    
    print(f"🎯 Intent: {query_intent} → Threshold: {confidence_threshold}")
    
    # Model evaluates content (ignoring Pinecone scores)
    confidence, reasoning = components.evaluate_content_quality(
        state["original_query"], 
        results
    )
    
    print(f"📊 Model confidence: {confidence}/10 (threshold: {confidence_threshold})")
    print(f"💭 Reasoning: {reasoning[:100]}...")
    
    evaluation_entry = f"Model evaluation: {confidence}/10 - {reasoning[:50]}..."
    
    # Dosage-specific fallback (instead of escalation!)
    if (state["query_intent"] == "dosage" and 
        confidence < confidence_threshold and 
        attempt >= MAX_REASONING_ATTEMPTS):
        
        print(f"💊 DOSAGE FALLBACK: Providing intelligent dosage guidance")
        
        dosage_fallback = get_dosage_fallback(state['original_query'])
        
        return {
            **state, 
            "final_answer": dosage_fallback,
            "should_continue": False,
            "model_confidence": 7.0,  # Good fallback response
            "evaluation_log": state["evaluation_log"] + [evaluation_entry + " | Intelligent dosage fallback used"]
        }
    
    # Standard confidence evaluation with dynamic threshold
    if confidence >= confidence_threshold:
        status = "EXCELLENT" if confidence >= 9.0 else "GOOD"
        print(f"✅ {status} content quality ({confidence}/10) - generating answer")
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": False,
            "evaluation_log": state["evaluation_log"] + [evaluation_entry]
        }
        
    elif attempt >= MAX_REASONING_ATTEMPTS:
        print(f"⚠️ Max attempts reached ({attempt}) - escalating")
        evaluation_entry += f" | Max attempts reached (threshold: {confidence_threshold})"
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": False, 
            "escalate": True,
            "evaluation_log": state["evaluation_log"] + [evaluation_entry]
        }
        
    else:
        print(f"🤔 Content quality insufficient ({confidence}/{confidence_threshold}) - continuing reasoning")
        evaluation_entry += f" | Insufficient quality, continuing (attempt {attempt}/{MAX_REASONING_ATTEMPTS})"
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": True,
            "evaluation_log": state["evaluation_log"] + [evaluation_entry]
        }

def generate_evaluation_answer(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Node 4: Generate final answer based on evaluated content"""
    
    if state.get("escalate"):
        escalation_response = """Przepraszam, nie udało mi się znaleźć wystarczająco precyzyjnych informacji na Twoje pytanie w bazie wiedzy Aquaforest.

🔍 **Możesz spróbować:**
1. Zadać pytanie bardziej szczegółowo
2. Sprawdzić instrukcję na opakowaniu produktu
3. Skontaktować się z naszymi ekspertami

📞 **Kontakt z ekspertami**: (+48) 14 691 79 79 (pon-pt, 8:00-16:00)
🌐 **Formularz kontaktowy**: https://aquaforest.eu/pl/kontakt/

Nasi specjaliści z przyjemnością odpowiedzą na wszystkie pytania! 🌊"""
        
        return {**state, "final_answer": escalation_response}
    
    results = state["search_results"]
    if not results:
        return {
            **state,
            "final_answer": "Nie znalazłem informacji na ten temat. Czy możesz sprecyzować pytanie?"
        }
    
    # Build context from evaluated results
    context = ""
    product_links = []
    
    for i, result in enumerate(results[:3]):
        context += f"\n--- ŹRÓDŁO {i+1} ---\n"
        context += f"Tytuł: {result['title']}\n"
        context += f"Typ: {result.get('content_type', 'unknown')}\n"
        context += f"Treść: {result['full_content']}\n"
        
        if result['content_type'] == 'product' and result['url']:
            product_links.append(f"• {result['title']}: {result['url']}")
    
    # Add evaluation context
    evaluation_summary = "\n".join(state["evaluation_log"])
    
    answer_prompt = f"""
    {ENHANCED_AQUAFOREST_EXPERT_PROMPT}
    
    === KONTEKST WYSZUKIWANIA ===
    Reasoning attempts: {state['attempt_count']}
    Model confidence achieved: {state['model_confidence']}/10
    Query intent: {state['query_intent']}
    Evaluation history: {evaluation_summary}
    
    === ZWERYFIKOWANE ŹRÓDŁA ===
    {context}
    
    === PYTANIE UŻYTKOWNIKA ===
    "{state['original_query']}"
    
    === INSTRUKCJE ===
    1. **TYLKO FACTS** - używaj wyłącznie informacji z kontekstu
    2. **ZERO IMPROVISATION** - nie dodawaj ogólnej wiedzy
    3. **AQUAFOREST FOCUS** - priorytet dla produktów AF
    4. **CONVERSATIONAL** - naturalny, przyjazny ton
    5. **PRACTICAL** - konkretne kroki, dawki, parametry
    
    ODPOWIEDŹ EKSPERTA AQUAFOREST:
    """
    
    try:
        response = components.llm.invoke([SystemMessage(content=answer_prompt)])
        answer = response.content
        
        # Add product links if relevant
        if product_links and len(product_links) <= 3:
            answer += f"\n\n🛒 **PRODUKTY AQUAFOREST:**\n" + "\n".join(product_links)
        
        return {**state, "final_answer": answer}
        
    except Exception as e:
        return {**state, "final_answer": f"Przepraszam, wystąpił błąd. Spróbuj ponownie."}

def get_dosage_fallback(original_query: str) -> str:
    """Inteligentny fallback dla pytań o dawkowanie"""
    
    query_lower = original_query.lower()
    
    base_response = """📦 **Dokładne dawkowanie znajdziesz na opakowaniu produktu**

Nie znalazłem szczegółowych informacji o dawkowaniu w bazie, ale oto ogólne wytyczne Aquaforest:"""

    # Ogólne zasady dawkowania dla typowych produktów
    general_guidelines = {
        "component": """
🔹 **Component 1+2+3**: Zazwyczaj 5-25ml/100L dziennie
   - Rozpocznij od 5ml/100L każdego komponentu
   - Zwiększaj stopniowo obserwując KH, Ca, Mg
   - Dawkuj równe ilości każdego komponentu
   - Testuj parametry co 2-3 dni podczas dostosowywania""",
   
        "power elixir": """
🔹 **AF Power Elixir**: Zazwyczaj 1-10ml/100L dziennie
   - Małe akwarium: 1-2ml/100L
   - Średnie akwarium: 3-5ml/100L
   - Duże akwarium z SPS: 5-10ml/100L
   - Podziel dawkę na 2-3 porcje dziennie""",
   
        "pro bio": """
🔹 **Pro Bio S**: Zazwyczaj 1-2 krople/100L dziennie
   - Monitoruj NO3 i PO4 regularnie
   - Zwiększaj dawkę stopniowo co tydzień
   - Stosuj razem z AF -NP PRO jeśli nutrienty spadają za szybko
   - W przypadku dużej bioobciążenia może być potrzebne więcej""",
   
        "vitality": """
🔹 **AF Vitality**: 2-5ml/100L 2-3 razy w tygodniu
   - Dawkuj wieczorem po wygaszeniu światła
   - Obserwuj reakcję koralowców (polipowanie)
   - Dostosuj częstotliwość do reakcji zwierząt""",
   
        "energy": """
🔹 **AF Energy**: 2-10ml/100L dziennie
   - Rozpocznij od najmniejszej dawki
   - Zwiększaj stopniowo obserwując koralowce
   - Najlepiej dawkować w kilku porcjach dziennie""",
   
        "kh pro": """
🔹 **KH Pro**: Dawkuj według potrzeb alkaliczności
   - 1ml KH Pro zwiększa alkaliczność o ~0.36 dKH na 100L
   - Cel: 7-9 dKH dla rafy mieszanej
   - Dawkuj powoli, maksymalnie 1 dKH wzrost na dobę"""
    }
    
    # Sprawdź czy pytanie dotyczy znanego produktu
    for key, guideline in general_guidelines.items():
        if key in query_lower:
            base_response += guideline
            break
    else:
        # Ogólne wytyczne jeśli produkt nierozpoznany
        base_response += """
🔹 **Ogólne zasady dawkowania Aquaforest**:
   - Zawsze rozpocznij od najmniejszej zalecanej dawki na etykiecie
   - Zwiększaj dawkę stopniowo co 3-7 dni
   - Obserwuj reakcję mieszkańców akwarium
   - Testuj parametry wody regularnie podczas dostosowywania"""

    base_response += """

⚠️ **WAŻNE ZASADY BEZPIECZEŃSTWA**:
- Zawsze przeczytaj instrukcję na opakowaniu
- Nie przekraczaj maksymalnych dawek
- W razie wątpliwości - mniej znaczy więcej!
- Monitoruj zwierzęta przez kilka dni po zmianie dawkowania

📞 **Pomoc techniczna**: (+48) 14 691 79 79 (pon-pt, 8:00-16:00)
🌐 **Instrukcje online**: https://aquaforest.eu/pl/produkty/
📧 **Kontakt**: https://aquaforest.eu/pl/kontakt/"""
    
    return base_response