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
    
    def search_knowledge(self, query: str, top_k: int = 8, attempt: int = 1) -> List[Dict]:
        """Search with dynamic top_k - more results in later attempts"""
        try:
            if not self.index:
                return []
            
            # Zwiększ liczbę wyników w kolejnych próbach
            dynamic_top_k = {
                1: 8,   # Standardowo
                2: 12,  # Więcej opcji
                3: 16   # Maksymalnie szeroko
            }
            
            final_top_k = dynamic_top_k.get(attempt, top_k)
            print(f"🔍 Searching with top_k={final_top_k} (attempt {attempt})")
            
            query_embedding = self.embeddings.embed_query(query)
            
            results = self.index.query(
                vector=query_embedding,
                namespace='pl',
                top_k=final_top_k,
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
        """SIMPLE rule-based query optimization - NO LLM calls!"""
        
        # Wyciągamy kluczowe słowa
        query_lower = original_query.lower()
        
        # Lista produktów AF do zachowania
        af_products = [
            "af power elixir", "component strong", "component 1+2+3", "component a", "component b", "component c",
            "pro bio s", "pro bio f", "hybrid pro salt", "reef salt", "kh pro", "kh plus",
            "life bio fil", "af vitality", "af energy", "zeomix", "carbon", "magnesium",
            "calcium", "stone fix", "af rock", "liquid vege", "af test", "barium", "strontium"
        ]
        
        # Zachowaj nazwy produktów
        keywords = []
        for product in af_products:
            if product in query_lower:
                keywords.append(product.replace(" ", "_"))  # Zastąp spacje podkreśleniami
        
        if attempt == 1:
            # Podstawowe słowa kluczowe + najbardziej trafne synonimy
            synonyms = {
                "dawkowanie": ["dawka", "stosowanie", "dozowanie"],
                "problem": ["pozbyć", "zwalczyć", "usunąć"],
                "koralowce": ["koralowiec", "sps", "lps"],
                "ryby": ["rybka", "ryba", "fish"],
                "akwarium": ["zbiornik", "tank"],
                "woda": ["water", "parametry"],
                "filtracja": ["filtr", "filter"],
                "oświetlenie": ["światło", "led"]
            }
            
            # Dodaj podstawowe słowa z zapytania
            words = query_lower.split()
            for word in words:
                if len(word) > 3 and word not in ["jest", "jest", "które", "można", "moje"]:
                    keywords.append(word)
            
            # Dodaj najbardziej trafne synonimy (max 2)
            for base, syns in synonyms.items():
                if base in query_lower:
                    keywords.extend(syns[:2])
                    
        elif attempt == 2:
            # Szersze kategorie + wszystkie podstawowe słowa
            words = query_lower.split()
            keywords.extend([w for w in words if len(w) > 2])
            
            # Kategorie domenowe
            if any(word in query_lower for word in ["morsk", "reef", "salt", "coral"]):
                keywords.extend(["seawater", "marine", "reef", "coral"])
            elif any(word in query_lower for word in ["słodkowod", "fresh", "roślinn"]):
                keywords.extend(["freshwater", "planted", "aquascaping"])
                
            # Dodaj ogólne terminy Aquaforest
            keywords.extend(["aquaforest", "af"])
            
        else:  # attempt 3
            # Najbardziej ogólne - szerokie pokrycie
            keywords = ["aquaforest", "af", "preparaty", "produkty", "akwarystyka", "akwarium"]
            
            # Dodaj kategorie na podstawie poprzednich prób
            if previous_evaluations:
                last_eval = previous_evaluations[-1].lower()
                if "brak" in last_eval or "insufficient" in last_eval:
                    keywords.extend(["marine", "freshwater", "supplements", "care", "maintenance"])
        
        # Usuń duplikaty zachowując kolejność
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen and len(kw) > 1:
                seen.add(kw)
                unique_keywords.append(kw)
        
        # Maksymalnie 8 najważniejszych słów
        final_query = " ".join(unique_keywords[:8])
        
        # Fallback jeśli query jest zbyt krótkie
        if len(final_query) < 10:
            final_query = original_query
            
        return final_query
    
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