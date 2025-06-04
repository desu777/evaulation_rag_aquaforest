# workflow_nodes.py - Core Workflow Nodes
from datetime import datetime
from langchain_core.messages import SystemMessage
from state import EnhancedEvaluationRAGState
from components import EvaluationRAGComponents
from config import ENHANCED_AQUAFOREST_EXPERT_PROMPT, MAX_REASONING_ATTEMPTS

# Initialize components
components = EvaluationRAGComponents()

def initialize_evaluation(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Node 1: Initialize evaluation-based reasoning"""
    print(f"🧠 ENHANCED EVALUATION RAG: {state['original_query']}")
    print("🎯 Model-based quality assessment + Intent detection")
    
    return {
        **state,
        "current_query": state['original_query'],
        "attempt_count": 0,
        "attempt_history": [],
        "all_results": [],
        "evaluation_log": [f"Starting evaluation for: '{state['original_query']}'"],
        "should_continue": True,
        "escalate": False,
        "query_intent": "general",
        "business_type": "none",
        "requires_trade_secret_filter": False,
        "confidence_threshold_override": 7.0,
        "company_context_added": False
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
    
    # Search with optimized query (no score filtering!)
    results = components.search_knowledge(optimized_query)
    
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
        "attempt_history": [attempt_info],
        "all_results": [results],
        "evaluation_log": [evaluation_entry]
    }

def enhanced_evaluate_content_quality(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Node 3: Enhanced evaluation with smart fallbacks"""
    attempt = state["attempt_count"]
    results = state["search_results"]
    
    print(f"🤖 Model evaluating content quality...")
    
    # Get dynamic threshold based on intent
    confidence_threshold = state.get("confidence_threshold_override", 7.0)
    
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
        
        print(f"💊 DOSAGE FALLBACK: Providing packaging instructions")
        
        dosage_fallback = f"""Nie znalazłem szczegółowych informacji o dawkowaniu w bazie wiedzy Aquaforest.

📦 **Instrukcje dawkowania znajdują się na opakowaniu produktu**
- Zawsze sprawdź etykietę przed użyciem
- Rozpocznij od najmniejszej zalecanej dawki  
- Obserwuj reakcję akwarium i dostosuj dawkę

💡 **Ogólne zasady Aquaforest:**
- Dawki na etykiecie są bezpieczne dla standardowych akwariów
- W przypadku wątpliwości skonsultuj z doświadczonym akwarystą
- Regularnie testuj parametry wody po dodaniu preparatu

📞 **Pomoc techniczna**: (+48) 14 691 79 79 (pon-pt, 8:00-16:00)

🌐 **Więcej informacji**: https://aquaforest.eu/pl/kontakt/"""
        
        return {
            **state, 
            "final_answer": dosage_fallback,
            "should_continue": False,
            "model_confidence": 7.0,  # Good fallback response
            "evaluation_log": [evaluation_entry + " | Dosage fallback used"]
        }
    
    # Standard confidence evaluation
    if confidence >= confidence_threshold:
        status = "EXCELLENT" if confidence >= 9.0 else "GOOD"
        print(f"✅ {status} content quality ({confidence}/10) - generating answer")
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": False,
            "evaluation_log": [evaluation_entry]
        }
        
    elif attempt >= MAX_REASONING_ATTEMPTS:
        print(f"⚠️ Max attempts reached ({attempt}) - escalating")
        evaluation_entry += f" | Max attempts reached"
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": False, 
            "escalate": True,
            "evaluation_log": [evaluation_entry]
        }
        
    else:
        print(f"🤔 Content quality insufficient ({confidence}/10) - continuing reasoning")
        evaluation_entry += f" | Insufficient quality, continuing"
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": True,
            "evaluation_log": [evaluation_entry]
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