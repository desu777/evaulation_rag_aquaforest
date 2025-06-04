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
        """MUCH simpler, natural query optimization"""
        
        if attempt == 1:
            # Keep it simple and natural
            optimization_prompt = f"""
            Skonwertuj pytanie na naturalne polskie słowa kluczowe dla wyszukiwania:
            
            PYTANIE: "{original_query}"
            
            ZASADY:
            - Użyj naturalnych polskich fraz
            - Zachowaj nazwy produktów (AF Power Elixir, Component Strong A)
            - Dodaj synonimy (dawkowanie = dawka, stosowanie)
            - MAX 10 słów
            
            NATURALNE SŁOWA KLUCZOWE:
            """
            
        elif attempt == 2:
            # Broader terms
            prev_feedback = previous_evaluations[-1] if previous_evaluations else "brak"
            optimization_prompt = f"""
            Rozszerz wyszukiwanie o pokrewne terminy:
            
            ORYGINALNE: "{original_query}"
            POPRZEDNIA PRÓBA DAŁA: {prev_feedback}
            
            Dodaj synonimy i powiązane terminy:
            - dawkowanie → dawka, stosowanie, dozowanie, aplikacja
            - akwarium → zbiornik, pojemność
            - produkty → preparaty, środki
            
            ROZSZERZONE SŁOWA KLUCZOWE:
            """
            
        else:  # attempt == 3
            # Very broad search
            optimization_prompt = f"""
            Ostatnia próba - najszersze wyszukiwanie:
            
            PYTANIE: "{original_query}"
            
            Użyj najogólniejszych terminów z kategorii produktu:
            - morskie, słodkowodne
            - akwarystyka, hodowla  
            - chemia, preparaty
            - Aquaforest, AF
            
            OGÓLNE TERMINY:
            """
        
        try:
            response = self.llm.invoke([SystemMessage(content=optimization_prompt)])
            optimized = response.content.strip().replace('"', '')
            
            # Clean up the response - extract only the keywords
            lines = optimized.split('\n')
            for line in lines:
                if line.strip() and not line.startswith('PYTANIE:') and not line.startswith('ZASADY:'):
                    if len(line.strip()) > 5:  # Skip very short lines
                        optimized = line.strip()
                        break
                        
            return optimized
            
        except Exception as e:
            print(f"❌ Query optimization error: {e}")
            return original_query
    
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