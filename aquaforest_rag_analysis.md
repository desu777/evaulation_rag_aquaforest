# 📊 ANALIZA SYSTEMU AQUAFOREST RAG

## 🏗️ ARCHITEKTURA SYSTEMU

### **1. Główne komponenty**

```
EnhancedEvaluationRAGAgent
    ├── workflow.py (LangGraph StateGraph)
    ├── workflow_nodes.py (Processing nodes)
    ├── intent_detection.py (Query classification)
    ├── business_handlers.py (Business/trade secret routing)
    ├── components.py (RAG core: search, evaluation)
    ├── state.py (State management)
    └── config.py (Configuration & prompts)
```

### **2. Architektura danych**

```
📁 aquarag/
    ├── knowledge/      (~53 pliki - główna baza wiedzy)
    ├── knowledge2/     (~151 plików - dodatkowa wiedza)
    └── produkty/
        ├── seawater/   (~100+ produktów morskich)
        ├── freshwater/ (produkty słodkowodne)
        ├── lab/        (produkty laboratoryjne)
        └── oceanguard/ (akwaria premium)
```

## 🧠 DZIAŁANIE SYSTEMU

### **Workflow Enhanced Evaluation RAG:**

1. **Initialize Evaluation** → ustaw state początkowy
2. **Analyze Query Intent** → wykryj typ pytania i intencję
3. **Business/Trade Secret Routing** → przekieruj specjalne zapytania
4. **Execute Search Attempt** → wyszukaj w Pinecone
5. **Enhanced Evaluate Content Quality** → oceń jakość LLM (1-10)
6. **Loop/Finish Decision** → kontynuuj wyszukiwanie lub zakończ
7. **Generate Evaluation Answer** → sformułuj odpowiedź

### **Intent Detection Patterns:**

- **Business**: "współpraca", "dystrybucja", "partnership"
- **Trade Secrets**: "jak powstaje", "receptura", "proces produkcji"
- **Dosage**: "dawkowanie", "ile ml", "proporcje"
- **Problems**: "problem", "jak pozbyć", "co robić"
- **Support**: "pomoc", "nie działa", "instrukcja"

### **Model-Based Evaluation (Kluczowa innowacja):**

System **NIE** używa Pinecone similarity scores do filtrowania!
Zamiast tego LLM (gpt-4o-mini) ocenia content quality na podstawie:

- **Relevance** (1-10): czy treść odpowiada na pytanie
- **Completeness** (1-10): czy informacje są wystarczające  
- **Actionability** (1-10): czy użytkownik wie co robić

**Progi pewności:**
- `EXCELLENT_CONFIDENCE = 9.0` (outstanding content)
- `GOOD_CONFIDENCE = 7.0` (sufficient to answer)
- `MAX_REASONING_ATTEMPTS = 3` (max próby przed eskalacją)

## 🔍 QUERY OPTIMIZATION

### **Progressive Query Enhancement:**

**Attempt 1**: Naturalne polskie słowa kluczowe
```
"dawkowanie AF Power Elixir" → "AF Power Elixir dawka stosowanie dozowanie"
```

**Attempt 2**: Rozszerzone synonimy
```
"dawkowanie" → "dawka, stosowanie, dozowanie, aplikacja, częstotliwość"
```

**Attempt 3**: Najszersze terminy kategorii
```
"morskie, słodkowodne, akwarystyka, preparaty, Aquaforest, AF"
```

## 📊 STRUKTURA DANYCH

### **Knowledge Base Format:**
```json
{
    "id": "unique-identifier",
    "content_type": "knowledge|product",
    "lang": "pl", 
    "title": "Tytuł artykułu",
    "query_text": "słowa kluczowe do wyszukiwania",
    "full_content": "pełna treść artykułu...",
    "domain": "seawater|freshwater|universal",
    "category": "education|problems|supplements",
    "intent": ["learning", "troubleshooting"],
    "difficulty": "beginner|intermediate|expert",
    "url": "źródłowy link",
    "tags": ["tag1", "tag2"],
    "related_items": ["powiązane-artykuły"],
    "updated_at": "2025-06-02"
}
```

## 🎯 TYPY ZAWARTOŚCI

### **Knowledge Categories:**
1. **Education** - artykuły edukacyjne (cykl azotowy, koralowce)
2. **Problems** - troubleshooting (ospa rybia, cyjanobakterie)
3. **Products** - informacje produktowe (dawkowanie, skład)
4. **Maintenance** - utrzymanie akwarium

### **Domain Distribution:**
- **Seawater**: ~60% zawartości (akwaria morskie, rafy)
- **Freshwater**: ~25% zawartości (akwaria słodkowodne)
- **Universal**: ~15% zawartości (ogólne zasady)

### **Difficulty Levels:**
- **Beginner**: podstawy akwarystyki
- **Intermediate**: standardowa hodowla
- **Expert**: zaawansowane techniki (SPS, metoda Ballinga)

## 🛡️ SPECIALIZED HANDLERS

### **Business Handler:**
```python
def handle_business_query(state):
    if "partnership" → contact info + phone number
    if "technical_support" → tech support details
    return final_answer (no RAG search needed)
```

### **Trade Secret Filter:**
```python
def check_trade_secrets(state):
    if production_patterns → generic company info
    no detailed recipes/processes revealed
    return final_answer (protects IP)
```

## ⚙️ KONFIGURACJA SYSTEMU

### **Vector Store:** Pinecone
- **Index**: "aquaforest"
- **Namespace**: "pl" (polish content)
- **Embeddings**: OpenAI text-embedding-3-small
- **Top-K**: 8 results per search

### **LLM:** OpenAI gpt-4o-mini
- **Temperature**: 0.1 (low randomness)
- **Role**: Aquaforest expert system
- **Task**: Content quality evaluation + answer generation

## 🔧 ADVANCED FEATURES

### **1. Confidence Threshold Override**
Różne progi pewności dla różnych typów pytań:
- Business: 9.0 (high threshold)
- Dosage: 6.0 (lower threshold, uses fallback)
- Problems: 6.5 (medium threshold)

### **2. Fallback Mechanisms**
Jeśli model evaluation < threshold:
- Próba 2: rozszerzone słowa kluczowe
- Próba 3: najogólniejsze terminy
- Eskalacja: "skontaktuj się z ekspertem"

### **3. Response Time Optimization**
- Pattern-based intent detection (szybsze niż LLM)
- Direct routing dla business/trade secrets
- Cached embeddings w Pinecone

## 📈 METRYKI OCENY

### **Success Metrics:**
- **Confidence Score**: średnia ocena jakości treści
- **Response Time**: czas odpowiedzi
- **Success Rate**: % pytań z odpowiedzią
- **Intent Accuracy**: poprawność klasyfikacji intencji
- **Escalation Rate**: % pytań przekazanych do ekspertów

### **Quality Indicators:**
- 🟢 **High (8.0+)**: Excellent content quality
- 🟡 **Medium (6.0-7.9)**: Acceptable content
- 🔴 **Low (<6.0)**: Poor/irrelevant content

## 🎪 STRESS TEST CATEGORIES

1. **🔰 BEGINNER** - podstawowe pytania (10 pytań)
2. **🏆 EXPERT** - zaawansowane zagadnienia (8 pytań)  
3. **🚨 PROBLEMS** - troubleshooting (10 pytań)
4. **💊 DOSAGE** - dawkowanie produktów (10 pytań)
5. **🔬 PRODUCTS** - informacje produktowe (10 pytań)
6. **⚗️ CHEMISTRY** - chemia wody (10 pytań)
7. **🐠 LIVESTOCK** - hodowla (10 pytań)
8. **🏢 BUSINESS** - pytania biznesowe (6 pytań)
9. **🔒 TRADE SECRETS** - tajemnice handlowe (7 pytań)
10. **🌊 SEAWATER** - specyfika morska (6 pytań)
11. **🌿 FRESHWATER** - specyfika słodkowodna (5 pytań)
12. **🧪 LAB** - produkty laboratoryjne (5 pytań)
13. **🏛️ OCEANGUARD** - akwaria premium (4 pytań)
14. **❓ AMBIGUOUS** - niejednoznaczne (6 pytań)
15. **🚀 EDGE CASES** - przypadki graniczne (9 pytań)

**ŁĄCZNIE: 116 pytań stres testowych**

## 🏆 PRZEWAGI SYSTEMU

### **1. Inteligentna Ocena Jakości**
- Model LLM zamiast prostych similarity scores
- Kontekstowe zrozumienie relevance
- Adaptacyjne progi pewności

### **2. Specjalistyczne Routing**
- Automatyczne wykrywanie intencji biznesowych
- Ochrona tajemnic handlowych
- Dedykowane handlery dla edge cases

### **3. Progressive Enhancement**
- 3-stopniowa optymalizacja zapytań
- Inteligentne fallback mechanisms
- Graceful degradation przy trudnych pytaniach

### **4. Komprehensywna Baza**
- 200+ dokumentów wiedzy
- 100+ produktów w 4 kategoriach
- Wielopoziomowa struktura trudności

## 🎯 EXPECTED PERFORMANCE

### **High Confidence Categories (8.0+):**
- Product information queries
- Specific dosage questions  
- Business/trade secret handling
- Well-documented problems

### **Medium Confidence Categories (6.0-7.9):**
- Complex chemistry questions
- Livestock breeding specifics
- Advanced troubleshooting
- Ambiguous product comparisons

### **Challenging Areas (<6.0):**
- Very specific edge cases
- Undocumented product combinations
- Extremely technical biochemistry
- Non-Polish language queries

---

**System zaprojektowany jako Production-Ready Enhanced RAG z zaawansowaną oceną jakości treści i inteligentnym routingiem zapytań specjalistycznych.** 