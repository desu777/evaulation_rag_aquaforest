# business_handlers.py - Business & Trade Secret Handlers
from state import EnhancedEvaluationRAGState

def handle_business_query(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Direct handling for business inquiries"""
    
    if state["business_type"] == "partnership":
        business_response = """Bardzo dziękujemy za zainteresowanie współpracą z Aquaforest! 🤝

**NAWIĄZANIE WSPÓŁPRACY**
Chętnie nawiążemy z Państwem współpracę biznesową.

📋 **Formularz kontaktowy**: https://aquaforest.eu/pl/kontakt/

📞 **Infolinia dla klientów biznesowych**: **(+48) 14 691 79 79**  
⏰ **Godziny pracy**: poniedziałek-piątek, 8:00-16:00

**Co oferujemy partnerom:**
🌊 Szeroką gamę produktów Aquaforest (sole, probiotyki, suplementy, akwaria OceanGuard)
🎓 Wsparcie techniczne i szkolenia  
📈 Materiały marketingowe i wsparcie sprzedażowe
💼 Konkurencyjne warunki współpracy

Jeśli masz pytania o dystrybucję naszych produktów, nasi specjaliści są gotowi zapewnić Ci pełne wsparcie i odpowiedzieć na wszystkie pytania biznesowe.

**Czekamy na Twój telefon!** 🌊"""
        
        return {
            **state, 
            "final_answer": business_response, 
            "should_continue": False,
            "model_confidence": 10.0  # Perfect business response
        }
    
    elif state["business_type"] == "technical_support":
        support_response = """Dziękujemy za kontakt z Aquaforest! 🛠️

**WSPARCIE TECHNICZNE**
Nasi eksperci są gotowi pomóc w rozwiązaniu problemów technicznych.

📞 **Pomoc techniczna**: **(+48) 14 691 79 79**  
⏰ **Godziny pracy**: poniedziałek-piątek, 8:00-16:00

📧 **Kontakt**: https://aquaforest.eu/pl/kontakt/

**Czym możemy pomóc:**
🔬 Doradztwo techniczne dotyczące produktów
📊 Interpretacja wyników testów ICP
🌊 Optymalizacja parametrów akwarium
🐠 Rozwiązywanie problemów z hodowlą

**Przygotuj do rozmowy:**
- Model i pojemność akwarium
- Aktualne parametry wody
- Stosowane produkty Aquaforest
- Opis problemu

Nasi specjaliści odpowiedzą na wszystkie pytania techniczne! 🌊"""
        
        return {
            **state, 
            "final_answer": support_response, 
            "should_continue": False,
            "model_confidence": 9.0  # Good support response
        }
    
    return state

def check_trade_secrets(state: EnhancedEvaluationRAGState) -> EnhancedEvaluationRAGState:
    """Handle production/trade secret queries"""
    
    if state.get("requires_trade_secret_filter"):
        trade_secret_response = """Dziękuję za pytanie o procesy produkcyjne Aquaforest! 🔒

**Informacje o produkcji to tajemnica handlowa firmy** - nie mogę ujawnić szczegółów dotyczących receptur, sposobów wytwarzania czy dokładnych składników.

**Co mogę powiedzieć:**
✅ Aquaforest produkuje w Polsce (Brzesko) od 1995 roku  
✅ Posiadamy własne laboratorium badawcze i hodowlę koralowców
✅ Produkty testowane w realnych warunkach hodowlanych
✅ Stosujemy surowce najwyższej czystości  
✅ Rygorystyczna kontrola jakości każdej partii
✅ Produkcja w małych partiach dla zapewnienia powtarzalności

**Wyróżniki naszej produkcji:**
🧪 **Metoda probiotyczna™** - zastosowanie korzystnych bakterii
🌊 **Hybrydowe sole** - naturalno-syntetyczne z witaminami
🔬 **Testowanie w hodowli** - każdy preparat sprawdzany na żywych organizmach

📞 **Kontakt techniczny**: (+48) 14 691 79 79 (pon-pt, 8:00-16:00)
🌐 **Więcej o firmie**: https://aquaforest.eu/pl/kontakt/"""
        
        return {
            **state, 
            "final_answer": trade_secret_response,
            "should_continue": False,
            "model_confidence": 9.0  # Good trade secret handling
        }
    
    return state