# dynamic_query_optimizer.py - Dynamic Query Optimizer for Aquaforest RAG
import re
from typing import List, Dict, Tuple, Optional
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

class DynamicQueryOptimizer:
    def __init__(self):
        self._llm: Optional[ChatOpenAI] = None  # Lazy initialization
        # Domain knowledge for better optimization
        self.aquaforest_domains = {
            "seawater": ["morskie", "rafowe", "koralowce", "SPS", "LPS", "sole"],
            "freshwater": ["słodkowodne", "rośliny", "akwarystyka", "nawozy"],
            "universal": ["akwarium", "filtracja", "bakterie", "parametry"],
            "products": ["AF", "Aquaforest", "Component", "Bio", "Life"]
        }
    
    @property
    def llm(self) -> ChatOpenAI:
        """Lazy initialization of LLM to avoid API key issues during import"""
        if self._llm is None:
            try:
                self._llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
            except Exception as e:
                print(f"⚠️ Warning: Could not initialize OpenAI LLM: {e}")
                print("🔧 Please set OPENAI_API_KEY environment variable")
                # Return a mock object that will fail gracefully
                raise RuntimeError(f"OpenAI LLM initialization failed: {e}")
        return self._llm
    
    def optimize_query_dynamically(self, 
                                 original_query: str, 
                                 attempt: int, 
                                 previous_attempts: List[Dict] = None,
                                 query_intent: str = "general") -> str:
        """
        🧠 DYNAMIC QUERY OPTIMIZATION BASED ON LLM
        
        Instead of hardcoded patterns, uses LLM for intelligent keyword generation
        based on semantic understanding and domain knowledge.
        """
        
        # Build context from previous attempts
        attempts_context = self._build_attempts_context(previous_attempts, attempt)
        
        # Get strategy for this attempt
        strategy = self._get_attempt_strategy(attempt)
        
        # Generate optimal query using LLM
        optimization_prompt = f"""
        {self._get_aquaforest_domain_prompt()}
        
        === DYNAMIC QUERY OPTIMIZATION TASK ===
        
        ORIGINAL USER QUERY: "{original_query}"
        QUERY INTENT: {query_intent}
        ATTEMPT: {attempt}/3
        STRATEGY: {strategy}
        
        {attempts_context}
        
        === OPTIMIZATION INSTRUCTIONS ===
        
        Your task is to generate optimal search keywords to find relevant content 
        in the Aquaforest knowledge base. The knowledge base contains documents with 
        metadata fields like "query_text" that contain semantic keywords.
        
        **ATTEMPT {attempt} STRATEGY: {strategy}**
        
        🎯 **SEMANTIC KEYWORD GENERATION RULES:**
        
        1. **ANALYZE USER INTENT**: What is the user really asking about?
        2. **GENERATE DOMAIN KEYWORDS**: Use semantic terms, NOT specific product names
        3. **PROGRESSIVE ABSTRACTION**: Each attempt should be broader than previous
        4. **AQUAFOREST CONTEXT**: Include appropriate domain terminology
        
        **TRANSFORMATION EXAMPLES:**
        - "jaką sól poleca" → "sól morska sole seawater Reef Salt Hybrid"
        - "dawkowanie AF Power Elixir" → "dawkowanie Power Elixir aminokwasy pokarm"
        - "cyjanobakterie problem" → "cyjanobakterie sinice niebiesko zielone glony problem"
        
        **DON'T:**
        ❌ Don't use exact product codes (AF-123-456)
        ❌ Don't generate unrelated keywords
        ❌ Don't repeat exactly same words from previous attempts
        ❌ Don't use too many keywords (max 6-8 words)
        
        **DO:**
        ✅ Use semantic domain terms
        ✅ Include synonyms and related concepts
        ✅ Match abstraction level to this attempt
        ✅ Consider Polish and English terminology
        
        GENERATE OPTIMAL KEYWORDS:
        """
        
        try:
            response = self.llm.invoke([SystemMessage(content=optimization_prompt)])
            optimal_query = response.content.strip()
            
            # Clean and validate response
            optimal_query = self._clean_optimal_query(optimal_query)
            
            print(f"🎯 Attempt {attempt} Dynamic Optimization:")
            print(f"   Original: '{original_query}'")
            print(f"   Strategy: {strategy}")
            print(f"   Optimal: '{optimal_query}'")
            
            return optimal_query
            
        except Exception as e:
            print(f"❌ Dynamic optimization failed: {e}")
            # Fallback to basic keyword extraction
            return self._fallback_optimization(original_query, attempt)
    
    def _get_aquaforest_domain_prompt(self) -> str:
        """Domain-specific context for better optimization"""
        return """
        === AQUAFOREST DOMAIN KNOWLEDGE ===
        
        **COMPANY**: Aquaforest - Polish manufacturer of aquarium products since 1995
        **PRODUCTS**: Seawater, Freshwater, Lab, OceanGuard systems
        
        **MAIN DOMAINS:**
        🌊 **SEAWATER**: corals, SPS, LPS, marine salts, Reef Salt, Hybrid Pro, Component, reef
        🌿 **FRESHWATER**: aquatic plants, fertilizers, substrate, CO2, aquascaping
        🔬 **LAB**: microelements, ICP tests, precision supplements
        🏛️ **OCEANGUARD**: premium aquariums, filtration, technology
        
        **POPULAR TERMS**: dosage, parameters, bacteria, nitrogen cycle, filtration, problems
        """
    
    def _get_attempt_strategy(self, attempt: int) -> str:
        """Get strategy description for current attempt"""
        strategies = {
            1: "FOCUSED SEARCH - Use specific keywords related to exact user question",
            2: "EXPANDED SEARCH - Add synonyms, related terms and broader domain concepts", 
            3: "BROAD SEARCH - Use high-level terms and general domain keywords"
        }
        return strategies.get(attempt, strategies[3])
    
    def _build_attempts_context(self, previous_attempts: List[Dict], current_attempt: int) -> str:
        """Build context from previous failed attempts"""
        if not previous_attempts or current_attempt == 1:
            return "**FIRST ATTEMPT**: No previous attempts to consider."
        
        context = "**PREVIOUS ATTEMPTS ANALYSIS:**\n"
        for i, attempt_data in enumerate(previous_attempts, 1):
            if i >= current_attempt:
                break
            confidence = attempt_data.get('confidence', 0)
            used_query = attempt_data.get('optimal_query', 'unknown')
            reasoning = attempt_data.get('reasoning', 'No reasoning')
            
            context += f"- Attempt {i}: '{used_query}' → Confidence: {confidence}/10\n"
            context += f"  Reasoning: {reasoning[:100]}...\n"
        
        context += f"\n**NEEDED IMPROVEMENT**: Previous attempts didn't find sufficient quality content. "
        context += f"Try different semantic approach for attempt {current_attempt}."
        
        return context
    
    def _clean_optimal_query(self, raw_query: str) -> str:
        """Clean and validate LLM-generated query"""
        # Remove common LLM artifacts
        cleaned = re.sub(r'^(keywords:?|search:?|query:?)\s*', '', raw_query, flags=re.IGNORECASE)
        cleaned = re.sub(r'"([^"]*)"', r'\1', cleaned)  # Remove quotes
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize whitespace
        cleaned = cleaned.strip()
        
        # Validate length (should be reasonable for search)
        words = cleaned.split()
        if len(words) > 10:
            cleaned = ' '.join(words[:10])  # Truncate if too long
        elif len(words) < 2:
            cleaned = f"aquarium Aquaforest {cleaned}"  # Add minimal terms
        
        return cleaned
    
    def _fallback_optimization(self, original_query: str, attempt: int) -> str:
        """Simple fallback if LLM optimization fails"""
        # Extract meaningful words from original query
        words = re.findall(r'\b\w{3,}\b', original_query.lower())
        
        # Add domain context based on attempt
        if attempt == 1:
            fallback = f"{' '.join(words)} aquarium"
        elif attempt == 2:
            fallback = f"{' '.join(words)} Aquaforest products"
        else:
            fallback = "aquaristics seawater freshwater Aquaforest"
        
        print(f"⚠️ Using fallback optimization: '{fallback}'")
        return fallback

    def generate_query_variants(self, original_query: str, num_variants: int = 3) -> List[str]:
        """
        🔀 GENERATE MULTIPLE QUERY VARIANTS
        
        Based on DMQR-RAG research - generate diverse queries for broader search
        """
        
        variants_prompt = f"""
        Generate {num_variants} diverse search query variants for this Aquaforest query:
        
        ORIGINAL: "{original_query}"
        
        Create variants using these techniques:
        1. **PARAPHRASING**: Rewrite while keeping meaning
        2. **SYNONYM SUBSTITUTION**: Use related terms
        3. **KEYWORD EXTRACTION**: Focus on core concepts
        
        EXAMPLE:
        Original: "problem z wysokimi azotanami"
        Variants:
        1. "azotany wysokie poziom obniżenie"
        2. "nadmiar azotanów jak pozbyć"
        3. "NO3 problem redukcja metody"
        
        Generate {num_variants} diverse variants (one per line):
        """
        
        try:
            response = self.llm.invoke([SystemMessage(content=variants_prompt)])
            variants = [line.strip() for line in response.content.split('\n') if line.strip()]
            
            # Clean each variant
            cleaned_variants = [self._clean_optimal_query(v) for v in variants[:num_variants]]
            
            print(f"🔀 Generated {len(cleaned_variants)} query variants")
            return cleaned_variants
            
        except Exception as e:
            print(f"❌ Multi-query generation failed: {e}")
            return [original_query]  # Return original as fallback

    def detect_intent_with_llm(self, query: str) -> str:
        """Use LLM to detect intent for ambiguous queries"""
        
        intent_prompt = f"""
        Analyze this Aquaforest query and determine user intent:
        
        QUERY: "{query}"
        
        Choose most appropriate intent:
        - **technical**: Technical questions about water parameters, chemistry, processes
        - **product**: Product information, comparisons, recommendations
        - **troubleshooting**: Problems requiring solutions
        - **setup**: New aquarium or equipment configuration
        - **maintenance**: Regular care and maintenance
        - **general**: General information or unclear intent
        
        Consider:
        - What is the user trying to achieve?
        - What type of information would be most helpful?
        - Is this a specific problem or general question?
        
        RESPOND WITH INTENT NAME ONLY:
        """
        
        try:
            response = self.llm.invoke([SystemMessage(content=intent_prompt)])
            detected_intent = response.content.strip().lower()
            
            # Validate response
            valid_intents = ["technical", "product", "troubleshooting", "setup", "maintenance", "general"]
            if detected_intent in valid_intents:
                return detected_intent
            else:
                return "general"
                
        except Exception as e:
            print(f"⚠️ LLM intent detection failed: {e}")
            return "general"