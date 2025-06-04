# evaluation_rag.py - Enhanced Evaluation RAG Main File
from agent import EnhancedEvaluationRAGAgent

def test_enhanced_evaluation_rag():
    """Test Enhanced Evaluation RAG with examples"""
    print("🧠 ENHANCED EVALUATION RAG TEST")
    print("📊 Model-based content quality assessment + Intent detection")
    print("🚀 Features: Business routing, Trade secrets, Dosage fallbacks")
    print("=" * 70)
    
    agent = EnhancedEvaluationRAGAgent()
    
    test_queries = [
        # Dosage query - should use fallback instead of escalation
        "AF Power Elixir dawkowanie na 300L akwarium",
        
        # Problem solving - should work well
        "Cyjanobakterie czerwony dywan jak pozbyć się",
        
        # Product info - should work well
        "Component Strong A skład i zastosowanie",
        
        # Comparison - should work quickly
        "Hybrid Pro Salt vs Reef Salt różnice",
        
        # Trade secret - should be handled directly
        "Jak jest produkowany AF Power Elixir?",
        
        # Problem solving
        "Wysokie azotany NO3 jak obniżyć akwarium rafowe",
        
        # Business query - should route to business handler
        "Chcielibyśmy z Państwem nawiązać współpracę dystrybucyjną",
        
        # Support query
        "Potrzebuję pomocy z parametrami akwarium"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}] Testing...")
        result = agent.ask(query)
        
        print(f"✅ Query: {query}")
        print(f"🎯 Intent: {result['query_intent']}, Business: {result['business_type']}")
        print(f"📊 Attempts: {result['attempts']}, Confidence: {result['model_confidence']}/10")
        print(f"🔒 Trade Secret: {result['trade_secret_handled']}")
        print(f"⚠️ Escalated: {result['escalated']}")
        print(f"💬 Answer Preview: {result['answer'][:150]}...")
        print("-" * 50)

def run_interactive_mode():
    """Interactive mode for testing"""
    print("\n🤖 ENHANCED EVALUATION RAG - Interactive Mode")
    print("Type 'exit' to quit")
    print("=" * 50)
    
    agent = EnhancedEvaluationRAGAgent()
    
    while True:
        user_input = input("\n❓ Your question: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q']:
            print("👋 Goodbye!")
            break
            
        if not user_input:
            continue
            
        result = agent.ask(user_input)
        
        print(f"\n🎯 Intent: {result['query_intent']} | Business: {result['business_type']}")
        print(f"📊 Confidence: {result['model_confidence']}/10 | Attempts: {result['attempts']}")
        print(f"\n💬 **Answer:**")
        print(result['answer'])

if __name__ == "__main__":
    # Run automated tests
    test_enhanced_evaluation_rag()
    
    # Uncomment for interactive mode
    # run_interactive_mode()