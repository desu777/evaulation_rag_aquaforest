#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick test script for RAG improvements
Tests key improvements without full stress test
"""

from agent import EnhancedEvaluationRAGAgent

def test_improvements():
    """Test kluczowych usprawnień"""
    print("🧪 TESTING RAG IMPROVEMENTS")
    print("=" * 50)
    
    agent = EnhancedEvaluationRAGAgent()
    
    # Test cases focusing on improved areas
    test_cases = [
        {
            "query": "AF Power Elixir dawkowanie na 500L",
            "expected_improvements": ["Better dosage fallback", "Lower threshold", "Simple query optimization"]
        },
        {
            "query": "Component A zastosowanie",
            "expected_improvements": ["Query preprocessing", "Product name correction"]
        },
        {
            "query": "Problem z cyjanobakteriami jak pozbyć",
            "expected_improvements": ["Lower threshold for problems", "Better keyword extraction"]
        },
        {
            "query": "Jak nawiązać współpracę z Aquaforest?",
            "expected_improvements": ["Business handler", "High threshold but direct routing"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- TEST {i}: {test_case['query']} ---")
        print(f"Expected improvements: {', '.join(test_case['expected_improvements'])}")
        
        try:
            result = agent.ask(test_case['query'])
            
            print(f"✅ Intent: {result['query_intent']}")
            print(f"📊 Confidence: {result['model_confidence']}/10")
            print(f"🔄 Attempts: {result['attempts']}")
            print(f"⚠️ Escalated: {result['escalated']}")
            print(f"🔒 Trade Secret: {result['trade_secret_handled']}")
            
            # Quick quality check
            answer_length = len(result['answer'])
            has_practical_info = any(word in result['answer'].lower() for word in ['ml', 'dawka', 'telefon', 'kontakt', 'krok'])
            
            print(f"📝 Answer length: {answer_length} chars")
            print(f"🎯 Has practical info: {has_practical_info}")
            
            if result['escalated']:
                print("⚠️  ESCALATED - might need further improvement")
            elif result['model_confidence'] >= 7.0:
                print("🎉 HIGH CONFIDENCE - improvement working!")
            elif result['model_confidence'] >= 6.0:
                print("👍 MEDIUM CONFIDENCE - acceptable")
            else:
                print("👎 LOW CONFIDENCE - needs work")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
        
        print("-" * 30)
    
    print("\n🎯 IMPROVEMENT TEST COMPLETED")
    print("Check above for confidence levels and escalation rates")

if __name__ == "__main__":
    test_improvements() 