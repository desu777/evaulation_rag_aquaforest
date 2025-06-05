# workflow_nodes.py v2 - Enhanced Workflow Nodes with GPT Augmentation
import re
from typing import List
from datetime import datetime
from langchain_core.messages import SystemMessage
from state import EnhancedEvaluationRAGStateV2
from components import EvaluationRAGComponents
from config import ENHANCED_AQUAFOREST_EXPERT_PROMPT, MAX_REASONING_ATTEMPTS

# Initialize components
components = EvaluationRAGComponents()

def initialize_evaluation_v2(state: EnhancedEvaluationRAGStateV2) -> EnhancedEvaluationRAGStateV2:
    """Node 1: Initialize enhanced evaluation with partial tracking"""
    print(f"🧠 ENHANCED EVALUATION RAG v2: {state['original_query']}")
    print("🎯 Model-based quality assessment + GPT Augmentation + Intent detection")
    
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
        "company_context_added": False,
        # 🆕 NEW: Initialize augmentation tracking
        "best_partial_result": None,
        "best_partial_confidence": 0.0,
        "attempt_confidences": [],
        "has_usable_partial": False,
        "use_augmentation": False,
        "augmentation_used": False,
        "augmentation_confidence": 0.0,
        "augmentation_reasoning": ""
    }

def enhanced_evaluate_content_quality_v2(state: EnhancedEvaluationRAGStateV2) -> EnhancedEvaluationRAGStateV2:
    """Node 3: Enhanced evaluation with partial result tracking and augmentation logic"""
    attempt = state["attempt_count"]
    results = state["search_results"]
    
    print(f"🤖 Model evaluating content quality (attempt {attempt})...")
    
    # Model evaluates content (ignoring Pinecone scores)
    confidence, reasoning = components.evaluate_content_quality(
        state["original_query"], 
        results
    )
    
    print(f"📊 Attempt {attempt} confidence: {confidence}/10")
    print(f"💭 Reasoning: {reasoning[:100]}...")
    
    # 🆕 TRACK BEST PARTIAL RESULT (5.0+)
    current_best = state.get("best_partial_confidence", 0.0)
    if confidence >= 5.0 and confidence > current_best:
        print(f"💾 Storing new best partial result: {confidence}/10 (previous: {current_best}/10)")
        best_partial = {
            "confidence": confidence,
            "reasoning": reasoning,
            "results": results,
            "attempt": attempt,
            "query": state["current_query"],
            "timestamp": datetime.now().isoformat()
        }
        
        # Update state with new best partial
        state = {
            **state,
            "best_partial_result": best_partial,
            "best_partial_confidence": confidence,
            "has_usable_partial": True
        }
    
    # Track attempt confidence
    attempt_confidences = state.get("attempt_confidences", [])
    attempt_confidences.append(confidence)
    
    # Get dynamic threshold based on intent
    confidence_threshold = state.get("confidence_threshold_override", 7.0)
    
    evaluation_entry = f"Model evaluation: {confidence}/10 - {reasoning[:50]}..."
    
    # DOSAGE-SPECIFIC FALLBACK (unchanged)
    if (state["query_intent"] == "dosage" and 
        confidence < confidence_threshold and 
        attempt >= MAX_REASONING_ATTEMPTS):
        
        print(f"💊 DOSAGE FALLBACK: Providing packaging instructions")
        return generate_dosage_fallback(state, evaluation_entry)
    
    # STANDARD CONFIDENCE EVALUATION
    if confidence >= confidence_threshold:
        status = "EXCELLENT" if confidence >= 9.0 else "GOOD"
        print(f"✅ {status} content quality ({confidence}/10) - generating answer")
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": False,
            "attempt_confidences": attempt_confidences,
            "evaluation_log": [evaluation_entry]
        }
    
    # CHECK FOR MAX ATTEMPTS REACHED
    elif attempt >= MAX_REASONING_ATTEMPTS:
        print(f"⚠️ Max attempts reached ({attempt}) - checking augmentation eligibility...")
        return check_augmentation_eligibility(state, confidence, evaluation_entry, attempt_confidences)
    
    # CONTINUE REASONING  
    else:
        print(f"🤔 Content quality insufficient ({confidence}/10) - continuing reasoning")
        evaluation_entry += f" | Insufficient quality, continuing"
        return {
            **state, 
            "model_confidence": confidence,
            "should_continue": True,
            "attempt_confidences": attempt_confidences,
            "evaluation_log": [evaluation_entry]
        }

def check_augmentation_eligibility(state: EnhancedEvaluationRAGStateV2, 
                                 current_confidence: float, 
                                 evaluation_entry: str,
                                 attempt_confidences: List[float]) -> EnhancedEvaluationRAGStateV2:
    """🆕 Decide: GPT Augmentation vs Standard Escalation"""
    
    has_partial = state.get("has_usable_partial", False)
    best_confidence = state.get("best_partial_confidence", 0.0)
    query_intent = state.get("query_intent", "general")
    
    # Protected query types (no augmentation)
    protected_intents = ["business", "dosage", "production"]
    
    print(f"🔍 Augmentation check:")
    print(f"   - Has partial: {has_partial} (best: {best_confidence}/10)")
    print(f"   - Query intent: {query_intent}")
    print(f"   - Protected: {query_intent in protected_intents}")
    
    # AUGMENTATION CONDITIONS
    if (has_partial and 
        best_confidence >= 5.0 and 
        query_intent not in protected_intents):
        
        print(f"🧠 TRIGGERING GPT AUGMENTATION (partial: {best_confidence}/10)")
        evaluation_entry += f" | Max attempts reached - triggering GPT augmentation with partial {best_confidence}/10"
        
        return {
            **state,
            "should_continue": False,
            "escalate": False,
            "use_augmentation": True,  # 🆕 Trigger augmentation
            "model_confidence": current_confidence,
            "attempt_confidences": attempt_confidences,
            "augmentation_reasoning": f"Using partial result from attempt {state['best_partial_result']['attempt']} with confidence {best_confidence}/10",
            "evaluation_log": [evaluation_entry]
        }
    
    # STANDARD ESCALATION
    else:
        reason = "no usable partial" if not has_partial else f"protected intent: {query_intent}"
        print(f"⚠️ Standard escalation ({reason})")
        evaluation_entry += f" | Max attempts reached - escalating ({reason})"
        
        return {
            **state, 
            "model_confidence": current_confidence,
            "should_continue": False, 
            "escalate": True,
            "attempt_confidences": attempt_confidences,
            "evaluation_log": [evaluation_entry]
        }

def gpt_augmentation_mode(state: EnhancedEvaluationRAGStateV2) -> EnhancedEvaluationRAGStateV2:
    """🆕 NEW: GPT Knowledge Augmentation with safety controls"""
    print(f"🧠 GPT AUGMENTATION MODE ACTIVATED")
    
    partial = state["best_partial_result"]
    best_confidence = state["best_partial_confidence"]
    
    print(f"📚 Using partial result from attempt {partial['attempt']} (confidence: {best_confidence}/10)")
    
    # Build context from best partial result
    partial_content = ""
    for i, result in enumerate(partial["results"][:3]):
        partial_content += f"--- ŹRÓDŁO {i+1} ---\n"
        partial_content += f"Tytuł: {result['title']}\n"
        partial_content += f"Typ: {result.get('content_type', 'unknown')}\n"
        partial_content += f"Treść: {result['full_content'][:400]}...\n\n"
    
    # Controlled augmentation prompt
    augmentation_prompt = f"""
    {ENHANCED_AQUAFOREST_EXPERT_PROMPT}
    
    === TRYB AUGMENTACJI WIEDZY ===
    
    Masz częściową wiedzę z bazy Aquaforest (confidence: {best_confidence}/10), 
    ale jest niewystarczająca do pełnej odpowiedzi na pytanie użytkownika.
    
    CZĘŚCIOWA WIEDZA Z BAZY AQUAFOREST:
    {partial_content}
    
    PYTANIE UŻYTKOWNIKA: "{state['original_query']}"
    
    ZADANIE - CONTROLLED AUGMENTATION:
    1. 🎯 Wykorzystaj znalezione treści jako FOUNDATION - to jest najważniejsze
    2. 🧠 Dopełnij brakującą wiedzę domenową z zakresu akwarystyki/Aquaforest
    3. 🛡️ Pozostań w kontekście znalezionych treści - NIE odchodź od tematu
    4. ❌ NIE dodawaj informacji sprzecznych z treściami z bazy
    5. 📝 Jasno zaznacz co pochodzi z bazy, a co jest uzupełnieniem
    6. ⚠️ Jeśli nie możesz bezpiecznie uzupełnić - powiedz to wprost
    7. 🔗 Zawsze dodaj kontakt do ekspertów dla weryfikacji
    
    STRUKTURA ODPOWIEDZI:
    **Na podstawie dostępnych informacji Aquaforest:**
    [konkretne treści z bazy RAG]
    
    **Dodatkowo w kontekście akwarystyki:**
    [bezpieczne uzupełnienie domenowe, jeśli możliwe]
    
    **⚠️ Dla potwierdzenia szczegółów skontaktuj się z ekspertami:**
    📞 Telefon: (+48) 14 691 79 79 (pon-pt, 8:00-16:00)
    🌐 Kontakt: https://aquaforest.eu/pl/kontakt/
    
    ODPOWIEDŹ EKSPERTA AQUAFOREST:
    """
    
    try:
        print(f"🎯 Generating augmented response...")
        response = components.llm.invoke([SystemMessage(content=augmentation_prompt)])
        augmented_answer = response.content.strip()
        
        print(f"📝 Generated augmented response ({len(augmented_answer)} chars)")
        
        # 🆕 SECOND EVALUATION - czy augmentacja jest bezpieczna i skuteczna?
        second_confidence, second_reasoning = evaluate_augmented_response(
            augmented_answer, 
            state["original_query"], 
            partial_content
        )
        
        print(f"🔍 Second evaluation: {second_confidence}/10")
        print(f"💭 Second reasoning: {second_reasoning[:100]}...")
        
        # Safety checks
        safety_passed = passes_safety_checks(augmented_answer, partial_content)
        print(f"🛡️ Safety checks: {'PASSED' if safety_passed else 'FAILED'}")
        
        # Final decision
        if second_confidence >= 7.0 and safety_passed:
            print(f"✅ AUGMENTATION SUCCESS! Using augmented response")
            return {
                **state,
                "final_answer": augmented_answer,
                "model_confidence": second_confidence,
                "augmentation_used": True,
                "augmentation_confidence": second_confidence,
                "should_continue": False,
                "escalate": False,
                "evaluation_log": [f"GPT augmentation successful: {second_confidence}/10 | {second_reasoning[:50]}..."]
            }
        else:
            reason = f"Low confidence: {second_confidence}/10" if second_confidence < 7.0 else "Safety check failed"
            print(f"❌ AUGMENTATION FAILED: {reason}")
            return {
                **state,
                "escalate": True,
                "should_continue": False,
                "augmentation_used": False,
                "augmentation_reasoning": f"Augmentation failed: {reason}",
                "evaluation_log": [f"GPT augmentation failed: {reason} | {second_reasoning[:50]}..."]
            }
            
    except Exception as e:
        print(f"❌ AUGMENTATION ERROR: {e}")
        return {
            **state,
            "escalate": True,
            "should_continue": False,
            "augmentation_used": False,
            "augmentation_reasoning": f"Augmentation error: {str(e)}",
            "evaluation_log": [f"GPT augmentation error: {str(e)}"]
        }

def evaluate_augmented_response(augmented_response: str, 
                              original_query: str, 
                              partial_content: str) -> tuple[float, str]:
    """🔍 Second evaluation for augmented responses"""
    
    eval_prompt = f"""
    Oceń jakość tej augmentowanej odpowiedzi na skali 1-10:
    
    PYTANIE UŻYTKOWNIKA: "{original_query}"
    
    AUGMENTOWANA ODPOWIEDŹ:
    {augmented_response}
    
    ORYGINALNA WIEDZA Z BAZY:
    {partial_content[:500]}...
    
    === KRYTERIA OCENY ===
    
    🎯 **RELEVANCE** (czy odpowiada na pytanie):
    - 1-3: Nie odpowiada na pytanie użytkownika
    - 4-6: Częściowo odpowiada, ale niepełne  
    - 7-8: Dobrze odpowiada na pytanie
    - 9-10: Perfekcyjnie odpowiada na pytanie
    
    📊 **CONSISTENCY** (spójność z bazą wiedzy):
    - 1-3: Sprzeczne z bazową wiedzą
    - 4-6: Częściowo spójne, niektóre niezgodności
    - 7-8: W pełni spójne z bazą
    - 9-10: Doskonale wykorzystuje bazę jako foundation
    
    🛡️ **SAFETY** (bezpieczeństwo, brak halucynacji):
    - 1-3: Wyraźne halucynacje, wymyślone fakty
    - 4-6: Ogólnikowe, ale bezpieczne
    - 7-8: Faktyczne, bez halucynacji  
    - 9-10: Bardzo precyzyjne i bezpieczne
    
    🔧 **ACTIONABILITY** (praktyczność):
    - 1-3: Brak konkretnych wskazówek
    - 4-6: Ogólne porady
    - 7-8: Konkretne, actionable steps
    - 9-10: Bardzo precyzyjne instrukcje
    
    ⚠️ **PENALTY FACTORS** (obniż ocenę za):
    - Wymyślone konkretne liczby/dawki/produkty
    - Informacje sprzeczne z bazą wiedzy
    - Brak kontaktu do ekspertów (powinien być!)
    - Zbyt długie lub zbyt krótkie odpowiedzi
    
    RESPOND IN FORMAT:
    CONFIDENCE: [number 1-10]
    REASONING: [brief explanation why this rating]
    """
    
    try:
        response = components.llm.invoke([SystemMessage(content=eval_prompt)])
        evaluation_text = response.content
        
        # Extract confidence score
        confidence_match = re.search(r'CONFIDENCE:\s*([1-9]|10)', evaluation_text)
        reasoning_match = re.search(r'REASONING:\s*(.+)', evaluation_text, re.DOTALL)
        
        confidence = float(confidence_match.group(1)) if confidence_match else 3.0
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"
        
        return confidence, reasoning
        
    except Exception as e:
        print(f"❌ Second evaluation error: {e}")
        return 3.0, f"Evaluation failed: {e}"

def passes_safety_checks(augmented_response: str, original_content: str) -> bool:
    """🛡️ Safety checks for augmented responses"""
    
    # Check 1: Reasonable length (not too short/long)
    if len(augmented_response) < 150 or len(augmented_response) > 2500:
        print(f"⚠️ Safety fail: Length {len(augmented_response)} chars (should be 150-2500)")
        return False
    
    # Check 2: Contains reference to contacting experts (mandatory for safety)
    contact_keywords = ["kontakt", "ekspert", "691 79 79", "aquaforest.eu", "telefon"]
    has_contact_ref = any(keyword in augmented_response.lower() for keyword in contact_keywords)
    if not has_contact_ref:
        print(f"⚠️ Safety fail: No expert contact reference")
        return False
    
    # Check 3: Contains foundation reference (should mention base knowledge)
    foundation_keywords = ["na podstawie", "dostępnych informacji", "z bazy", "aquaforest"]
    has_foundation_ref = any(keyword in augmented_response.lower() for keyword in foundation_keywords)
    if not has_foundation_ref:
        print(f"⚠️ Safety fail: No foundation reference")
        return False
    
    # Check 4: Basic structure check (should have multiple sections)
    if augmented_response.count('\n') < 3:
        print(f"⚠️ Safety fail: Poor structure (too few sections)")
        return False
    
    print(f"✅ Safety checks passed")
    return True

def generate_dosage_fallback(state: EnhancedEvaluationRAGStateV2, evaluation_entry: str) -> EnhancedEvaluationRAGStateV2:
    """💊 Generate dosage fallback response"""
    
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

def execute_search_attempt(state: EnhancedEvaluationRAGStateV2) -> EnhancedEvaluationRAGStateV2:
    """Node 2: Execute search attempt with query optimization"""
    attempt = state["attempt_count"] + 1
    original_query = state["original_query"]
    
    print(f"🔍 Search attempt {attempt}/{MAX_REASONING_ATTEMPTS}")
    
    # Optimize query based on attempt number and previous evaluations
    previous_evaluations = state.get("evaluation_log", [])
    optimized_query = components.optimize_query_for_attempt(
        original_query, 
        attempt, 
        previous_evaluations
    )
    
    print(f"🎯 Optimized query: '{optimized_query}'")
    
    # Progressive search expansion - więcej wyników w kolejnych próbach
    search_k_values = {
        1: 8,   # Pierwsza próba - focused search
        2: 12,  # Druga próba - broader search  
        3: 16   # Trzecia próba - widest search
    }
    top_k = search_k_values.get(attempt, 8)
    
    print(f"📡 Search strategy: top_k={top_k} (progressive expansion)")
    
    # Execute search
    search_results = components.search_knowledge(optimized_query, top_k=top_k)
    
    print(f"📚 Found {len(search_results)} results")
    
    # Track attempt history
    attempt_info = {
        "attempt": attempt,
        "optimized_query": optimized_query,
        "results_count": len(search_results),
        "timestamp": datetime.now().isoformat()
    }
    
    # Update state
    attempt_history = state.get("attempt_history", [])
    attempt_history.append(attempt_info)
    
    all_results = state.get("all_results", [])
    all_results.append(search_results)
    
    return {
        **state,
        "attempt_count": attempt,
        "current_query": optimized_query,
        "search_results": search_results,
        "attempt_history": attempt_history,
        "all_results": all_results,
        "evaluation_log": [f"Attempt {attempt}: '{optimized_query}' → {len(search_results)} results found (top_k={top_k})"]
    }

def generate_evaluation_answer(state: EnhancedEvaluationRAGStateV2) -> EnhancedEvaluationRAGStateV2:
    """Node 4: Generate final answer based on search results"""
    
    # Check if we should escalate instead
    if state.get("escalate", False):
        escalation_response = f"""Przepraszam, ale nie znalazłem wystarczających informacji w bazie wiedzy Aquaforest aby odpowiedzieć na Twoje pytanie: "{state['original_query']}"

📞 **Skontaktuj się bezpośrednio z naszymi ekspertami:**
- **Telefon**: (+48) 14 691 79 79 (pon-pt, 8:00-16:00)
- **Website**: https://aquaforest.eu/pl/kontakt/

🧠 **Nasi specjaliści pomogą Ci z:**
- Szczegółowym doradztwem technicznym
- Interpretacją wyników testów  
- Optymalizacją parametrów akwarium
- Rozwiązywaniem problemów hodowlanych

**Przygotuj do rozmowy:**
- Model i pojemność akwarium
- Aktualne parametry wody  
- Stosowane produkty Aquaforest
- Opis problemu lub pytania

Czekamy na Twój telefon! 🌊"""
        
        return {
            **state,
            "final_answer": escalation_response,
            "should_continue": False
        }
    
    # Generate answer from good quality results
    results = state["search_results"]
    query = state["original_query"]
    confidence = state["model_confidence"]
    
    print(f"📝 Generating final answer (confidence: {confidence}/10)")
    
    # Prepare context from search results
    context = ""
    for i, result in enumerate(results[:4]):  # Top 4 results
        context += f"\n--- ŹRÓDŁO {i+1} ---\n"
        context += f"Tytuł: {result['title']}\n"
        context += f"Typ: {result.get('content_type', 'unknown')}\n"
        context += f"Treść: {result['full_content']}\n"
        if result.get('url'):
            context += f"URL: {result['url']}\n"
    
    # Generate comprehensive answer
    answer_prompt = f"""
    {ENHANCED_AQUAFOREST_EXPERT_PROMPT}
    
    === GENEROWANIE ODPOWIEDZI EKSPERTA ===
    
    PYTANIE UŻYTKOWNIKA: "{query}"
    
    ŹRÓDŁA Z BAZY WIEDZY AQUAFOREST:
    {context}
    
    ZADANIE:
    Napisz kompletną, profesjonalną odpowiedź jako ekspert Aquaforest wykorzystując dostępne źródła.
    
    WYMAGANIA ODPOWIEDZI:
    ✅ Bezpośrednio odpowiedz na pytanie użytkownika
    ✅ Wykorzystaj konkretne informacje ze źródeł
    ✅ Dodaj praktyczne wskazówki krok po kroku
    ✅ Uwzględnij specyfikę produktów Aquaforest
    ✅ Zachowaj profesjonalny, pomocny ton
    ✅ Dodaj kontakt do ekspertów na końcu
    
    STRUKTURA:
    1. **Bezpośrednia odpowiedź** na pytanie
    2. **Szczegóły techniczne** z bazy wiedzy
    3. **Praktyczne wskazówki** krok po kroku
    4. **Kontakt ekspercki** dla dalszej pomocy
    
    ❌ NIE DODAWAJ informacji sprzecznych ze źródłami
    ❌ NIE WYMYŚLAJ konkretnych liczb/dawek bez potwierdzenia
    ❌ NIE UŻYWAJ ogólnikowych porad
    
    ODPOWIEDŹ EKSPERTA AQUAFOREST:
    """
    
    try:
        response = components.llm.invoke([SystemMessage(content=answer_prompt)])
        final_answer = response.content.strip()
        
        # Add expert contact if not present
        if "691 79 79" not in final_answer and "aquaforest.eu" not in final_answer:
            final_answer += f"""

📞 **Dodatkowa pomoc ekspertów Aquaforest:**
- Telefon: (+48) 14 691 79 79 (pon-pt, 8:00-16:00)
- Website: https://aquaforest.eu/pl/kontakt/"""
        
        print(f"✅ Generated answer ({len(final_answer)} characters)")
        
        return {
            **state,
            "final_answer": final_answer,
            "should_continue": False
        }
        
    except Exception as e:
        print(f"❌ Answer generation error: {e}")
        return {
            **state,
            "final_answer": f"Błąd generowania odpowiedzi: {e}. Skontaktuj się z ekspertami: (+48) 14 691 79 79",
            "should_continue": False,
            "escalate": True
        }