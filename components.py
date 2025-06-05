# components.py - Core RAG Components
import re
from typing import List, Dict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage
from config import get_pinecone_index, ENHANCED_AQUAFOREST_EXPERT_PROMPT

class EvaluationRAGComponents:
    def __init__(self):
        self.index = get_pinecone_index()
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    def search_knowledge(self, query: str, top_k: int = 8) -> List[Dict]:
        """Simple search without score filtering - let model decide quality"""
        try:
            if not self.index:
                return []
            
            query_embedding = self.embeddings.embed_query(query)
            
            results = self.index.query(
                vector=query_embedding,
                namespace='pl',
                top_k=top_k,
                include_metadata=True
            )
            
            # Return ALL results - no score filtering!
            formatted_results = []
            for match in results.get('matches', []):
                metadata = match.get('metadata', {})
                formatted_results.append({
                    'pinecone_score': match.get('score', 0),  # Keep for reference only
                    'title': metadata.get('title', 'Brak tytułu'),
                    'full_content': metadata.get('full_content', ''),
                    'content_type': metadata.get('content_type', ''),
                    'url': metadata.get('url', ''),
                    'domain': metadata.get('domain', ''),
                    'category': metadata.get('category', ''),
                    'tags': metadata.get('tags', [])
                })
            
            return formatted_results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []
    
    def optimize_query_for_attempt(self, original_query: str, attempt: int, previous_evaluations: List[str] = None) -> str:
        """Intelligent query optimization based on topic context and embeddings structure"""
        
        # TOPIC DETECTION - analyze query intent
        query_lower = original_query.lower()
        
        # Detect main topic categories
        is_salt_query = any(term in query_lower for term in ['sól', 'soli', 'salt', 'zasolenie', 'hybrid', 'reef salt'])
        is_dosage_query = any(term in query_lower for term in ['dawkowanie', 'dawka', 'ile', 'ml', 'dozowanie', 'stosowanie'])
        is_component_query = any(term in query_lower for term in ['component', 'komponent', 'a', 'b', 'c', '1', '2', '3'])
        is_coral_query = any(term in query_lower for term in ['koralowce', 'sps', 'lps', 'coral', 'polip'])
        is_problem_query = any(term in query_lower for term in ['problem', 'jak pozbyć', 'cyjan', 'glon', 'wysokie', 'niskie'])
        is_fish_query = any(term in query_lower for term in ['rybka', 'ryby', 'fish', 'anthias', 'kwarantanna'])
        is_water_query = any(term in query_lower for term in ['woda', 'parametry', 'ph', 'alkalicz', 'wapń', 'magnez'])
        is_startup_query = any(term in query_lower for term in ['założyć', 'start', 'pierwsze', 'nowe', 'cykl'])
        
        if attempt == 1:
            # FOCUSED SEARCH - topic-specific keywords
            if is_salt_query:
                keywords = "sól morska seawater Reef Salt Hybrid Pro Salt 33ppt"
            elif is_dosage_query and is_component_query:
                keywords = "Component dawkowanie ml stosowanie akwarium"
            elif is_dosage_query:
                keywords = "dawkowanie dawka ml aplikacja stosowanie"
            elif is_coral_query:
                keywords = "koralowce SPS LPS miękkie twardy coral polyp"
            elif is_problem_query:
                keywords = "problem cyjanobakterie glony azotany fosforany"
            elif is_fish_query:
                keywords = "ryby fish aklimatyzacja kwarantanna choroba"
            elif is_water_query:
                keywords = "parametry wody pH alkaliczność wapń magnez"
            elif is_startup_query:
                keywords = "start akwarium założyć cykl azotowy nowe"
            else:
                # Extract main keywords from query
                keywords = " ".join([word for word in query_lower.split() if len(word) > 3])
                keywords = f"{keywords} akwarium Aquaforest"
                
        elif attempt == 2:
            # BROADER SEARCH - add synonyms and related terms
            if is_salt_query:
                keywords = "sól morska salt seawater Hybrid Pro bakterie probiotyczne aminokwasy witamina"
            elif is_dosage_query:
                keywords = "dawkowanie dawka stosowanie dozowanie aplikacja ml instrukcja"
            elif is_coral_query:
                keywords = "koralowce coral SPS LPS miękkie twardy wzrost polipowanie"
            elif is_problem_query:
                keywords = "problem rozwiązanie cyjan glony azotany fosforany klarowanie"
            elif is_fish_query:
                keywords = "ryby fish aklimatyzacja choroba kwarantanna leczenie"
            elif is_water_query:
                keywords = "parametry woda chemia pH KH wapń magnez test"
            elif is_startup_query:
                keywords = "start założenie akwarium cykl bakterie dojrzewanie"
            else:
                keywords = f"akwarystyka morska słodkowodna Aquaforest AF hodowla"
                
        else:  # attempt == 3
            # WIDEST SEARCH - domain-level keywords
            if any([is_salt_query, is_coral_query, is_component_query]):
                keywords = "akwarystyka morska seawater coral reef marine"
            elif is_startup_query or is_water_query:
                keywords = "akwarium start parametry woda bakterie Aquaforest"
            elif is_fish_query:
                keywords = "ryby akwarium hodowla marine fish care"
            else:
                keywords = "akwarystyka Aquaforest AF produkty akwarium"
        
        print(f"🎯 Topic detection: salt={is_salt_query}, dosage={is_dosage_query}, coral={is_coral_query}")
        
        return keywords.strip()
    
    def evaluate_content_quality(self, query: str, results: List[Dict]) -> tuple[float, str]:
        """Model-based evaluation of content quality - NO Pinecone scores used!"""
        
        if not results:
            return 0.0, "No search results to evaluate"
        
        # Prepare context from results (WITHOUT showing Pinecone scores to model)
        context = ""
        for i, result in enumerate(results[:4]):  # Top 4 results
            context += f"\n--- RESULT {i+1} ---\n"
            context += f"Title: {result['title']}\n"
            context += f"Type: {result.get('content_type', 'unknown')}\n"
            context += f"Content: {result['full_content'][:400]}...\n"
        
        evaluation_prompt = f"""
        {ENHANCED_AQUAFOREST_EXPERT_PROMPT}
        
        === EVALUATION TASK ===
        
        USER QUESTION: "{query}"
        
        SEARCH RESULTS TO EVALUATE:
        {context}
        
        === EVALUATION CRITERIA ===
        
        Rate how well these results answer the user's question (1-10):
        
        🎯 **RELEVANCE** (czy treść odpowiada na pytanie):
        - 1-3: Nie odpowiada / zupełnie inne tematy
        - 4-6: Częściowo związane ale nie na temat
        - 7-8: Odpowiada na pytanie, dobre informacje
        - 9-10: Perfekcyjnie odpowiada, kompletne info
        
        📊 **COMPLETENESS** (czy wystarczające informacje):
        - 1-3: Brak konkretów, ogólniki
        - 4-6: Niektóre informacje ale niepełne
        - 7-8: Wystarczające do pomocy użytkownikowi
        - 9-10: Kompletne, wszystko co potrzebne
        
        🔧 **ACTIONABILITY** (czy użytkownik wie co robić):
        - 1-3: Brak praktycznych porad
        - 4-6: Ogólne wskazówki
        - 7-8: Konkretne kroki do wykonania
        - 9-10: Precyzyjne instrukcje krok po krok
        
        RESPOND IN FORMAT:
        CONFIDENCE: [number 1-10]
        REASONING: [brief explanation why this rating]
        """
        
        try:
            response = self.llm.invoke([SystemMessage(content=evaluation_prompt)])
            evaluation_text = response.content
            
            # Extract confidence score
            confidence_match = re.search(r'CONFIDENCE:\s*([1-9]|10)', evaluation_text)
            reasoning_match = re.search(r'REASONING:\s*(.+)', evaluation_text, re.DOTALL)
            
            confidence = float(confidence_match.group(1)) if confidence_match else 5.0
            reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"
            
            return confidence, reasoning
            
        except Exception as e:
            print(f"❌ Content evaluation error: {e}")
            return 3.0, f"Evaluation failed: {e}"