# evaluation_rag.py v2 - Enhanced Evaluation RAG with GPT Augmentation Test
from agent import EnhancedEvaluationRAGAgentV2

def test_enhanced_evaluation_rag_v2():
    """Test Enhanced Evaluation RAG v2 with GPT Augmentation"""
    print("🧠 ENHANCED EVALUATION RAG v2 TEST")
    print("📊 Model-based content quality assessment + GPT Augmentation + Intent detection")
    print("🚀 Features: Business routing, Trade secrets, Dosage fallbacks, GPT Augmentation")
    print("=" * 70)
    
    agent = EnhancedEvaluationRAGAgentV2()
    
    # Test queries targeting different augmentation scenarios
    test_queries = [
        # Expected to work normally (high confidence)
        "AF Power Elixir dawkowanie na 300L akwarium",
        
        # Expected to use augmentation (partial knowledge)
        "Jak rozwiązać problem z wysokimi azotanami w akwarium rafowym?",
        
        # Expected to trigger business handler
        "Chcielibyśmy nawiązać współpracę dystrybucyjną",
        
        # Expected to trigger trade secret protection  
        "Jak jest produkowany AF Power Elixir?",
        
        # Expected to use dosage fallback
        "Ile ML Component Strong A na 150L?",
        
        # Potential augmentation candidate
        "Cyjanobakterie w akwarium - jak się pozbyć?",
        
        # Potential augmentation candidate  
        "Białe plamy na koralowcach - co robić?",
        
        # Expected to work normally
        "Pro Bio S dawkowanie na 100L",
        
        # Potential augmentation candidate
        "Problemy z pH w akwarium morskim",
        
        # Edge case - should escalate
        "askjdlaksjd random text"
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}] Testing...")
        result = agent.ask(query)
        results.append(result)
        
        # Print test summary
        print(f"✅ Query: {query}")
        print(f"🎯 Intent: {result['query_intent']}, Business: {result['business_type']}")
        print(f"📊 Attempts: {result['attempts']}, Final Confidence: {result['model_confidence']}/10")
        
        if result['augmentation_used']:
            print(f"🧠 AUGMENTATION: ✅ SUCCESS (partial: {result['best_partial_confidence']}/10 → final: {result['augmentation_confidence']}/10)")
        elif result['best_partial_confidence'] > 0:
            print(f"🧠 AUGMENTATION: ❌ SKIPPED (had partial: {result['best_partial_confidence']}/10)")
        else:
            print(f"🧠 AUGMENTATION: ⚪ N/A (no partial results)")
            
        print(f"🔒 Trade Secret: {result['trade_secret_handled']}")
        print(f"⚠️ Escalated: {result['escalated']}")
        print(f"💬 Answer Preview: {result['answer'][:150]}...")
        print("-" * 50)
    
    # Generate summary statistics
    print_summary_statistics(results)
    
    return results

def print_summary_statistics(results):
    """Print comprehensive summary statistics"""
    print("\n" + "=" * 70)
    print("📈 ENHANCED RAG v2 SUMMARY STATISTICS")
    print("=" * 70)
    
    total = len(results)
    successful = len([r for r in results if not r['escalated']])
    augmented = len([r for r in results if r['augmentation_used']])
    had_partial = len([r for r in results if r['best_partial_confidence'] > 0])
    
    print(f"📊 BASIC METRICS:")
    print(f"   Total queries: {total}")
    print(f"   Successful: {successful}/{total} ({successful/total*100:.1f}%)")
    print(f"   Escalated: {total-successful}/{total} ({(total-successful)/total*100:.1f}%)")
    
    print(f"\n🧠 AUGMENTATION METRICS:")
    print(f"   Queries with partial results: {had_partial}/{total} ({had_partial/total*100:.1f}%)")
    print(f"   Augmentation used: {augmented}/{total} ({augmented/total*100:.1f}%)")
    print(f"   Augmentation success rate: {augmented}/{had_partial} ({augmented/had_partial*100:.1f}%)" if had_partial > 0 else "   Augmentation success rate: N/A")
    
    # Confidence distribution
    all_confidences = []
    augmented_confidences = []
    
    for r in results:
        if not r['escalated']:
            all_confidences.append(r['model_confidence'])
        if r['augmentation_used']:
            augmented_confidences.append(r['augmentation_confidence'])
    
    if all_confidences:
        avg_confidence = sum(all_confidences) / len(all_confidences)
        print(f"\n📊 CONFIDENCE METRICS:")
        print(f"   Average confidence: {avg_confidence:.1f}/10")
        
        if augmented_confidences:
            avg_aug_confidence = sum(augmented_confidences) / len(augmented_confidences)
            print(f"   Average augmented confidence: {avg_aug_confidence:.1f}/10")
    
    # Intent distribution
    intents = {}
    for r in results:
        intent = r['query_intent']
        intents[intent] = intents.get(intent, 0) + 1
    
    print(f"\n🎯 INTENT DISTRIBUTION:")
    for intent, count in sorted(intents.items(), key=lambda x: x[1], reverse=True):
        print(f"   {intent}: {count}")
    
    # Augmentation details
    print(f"\n🧠 AUGMENTATION DETAILS:")
    for i, r in enumerate(results, 1):
        if r['best_partial_confidence'] > 0:
            status = "✅ USED" if r['augmentation_used'] else "❌ SKIPPED"
            print(f"   Q{i}: {status} (partial: {r['best_partial_confidence']}/10)")

def run_interactive_mode_v2():
    """Interactive mode for testing v2"""
    print("\n🤖 ENHANCED EVALUATION RAG v2 - Interactive Mode")
    print("🧠 Now with GPT Augmentation!")
    print("Type 'exit' to quit")
    print("=" * 50)
    
    agent = EnhancedEvaluationRAGAgentV2()
    
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
        
        if result['augmentation_used']:
            print(f"🧠 GPT Augmentation: ✅ USED ({result['best_partial_confidence']}/10 → {result['augmentation_confidence']}/10)")
        elif result['best_partial_confidence'] > 0:
            print(f"🧠 GPT Augmentation: ❌ Available but not used ({result['best_partial_confidence']}/10)")
        
        print(f"\n💬 **Answer:**")
        print(result['answer'])

def quick_augmentation_test():
    """Quick test focusing on augmentation scenarios"""
    print("\n🧠 QUICK AUGMENTATION TEST")
    print("=" * 40)
    
    agent = EnhancedEvaluationRAGAgentV2()
    
    # Queries likely to have partial knowledge (5.0-6.9 range)
    augmentation_candidates = [
        "Jak obniżyć wysokie fosforany w akwarium?",
        "Problem z glonami nitkowatymi",
        "Białe plamy na koralowcach SPS",
        "Niska alkaliczność w akwarium",
        "Cyjanobakterie czerwony dywan"
    ]
    
    for query in augmentation_candidates:
        print(f"\n🔍 Testing: {query}")
        result = agent.ask(query)
        
        if result['augmentation_used']:
            print(f"   ✅ AUGMENTATION SUCCESS! ({result['best_partial_confidence']}/10 → {result['augmentation_confidence']}/10)")
        elif result['best_partial_confidence'] > 0:
            print(f"   ⚠️ Had partial ({result['best_partial_confidence']}/10) but not used")
        else:
            print(f"   ❌ No partial results found")

if __name__ == "__main__":
    # Run automated tests
    test_enhanced_evaluation_rag_v2()
    
    # Uncomment for interactive mode
    # run_interactive_mode_v2()
    
    # Uncomment for quick augmentation test
    # quick_augmentation_test()