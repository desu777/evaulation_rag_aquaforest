# evaluation_rag.py v3 - Enhanced Evaluation RAG with Dynamic Optimization Test
from agent import EnhancedEvaluationRAGAgentV2

def test_enhanced_evaluation_rag_v3():
    """Test Enhanced Evaluation RAG v3 with Dynamic Query Optimization"""
    print("🧠 ENHANCED EVALUATION RAG v3 TEST")
    print("📊 Model-based quality + GPT Augmentation + Dynamic Optimization")
    print("🚀 Features: Business routing, Trade secrets, Dosage fallbacks, GPT Augmentation, Dynamic Query Optimization")
    print("=" * 70)
    
    agent = EnhancedEvaluationRAGAgentV2()
    
    # Test queries targeting different optimization and augmentation scenarios
    test_queries = [
        # 🚀 Dynamic Optimization test cases
        "co poleca na start morskiego akwarium",  # Should show semantic expansion
        "problem z czerwonymi bakteriami na dnie",  # Should show domain understanding
        "AF coś tam do karmienia koralowców",  # Should handle ambiguous product references
        "wysokie NO3 jak szybko obniżyć",  # Should expand technical terms
        
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
        
        # Dynamic optimization + potential augmentation candidates
        "glony na wszystkim jak pozbyć natychmiast",
        "koralowce nie rosną od miesiąca pomoc",
        "pH spadło w nocy do 7.5 co robić",
        
        # Expected to work normally
        "Pro Bio S dawkowanie na 100L",
        
        # Complex optimization test
        "bakterie do nowego zbiornika 200L morski",
        
        # Edge case - should escalate
        "askjdlaksjd random text"
    ]
    
    results = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}/{len(test_queries)}] Testing...")
        result = agent.ask(query)
        results.append(result)
        
        # Print detailed test summary
        print(f"✅ Query: {query}")
        print(f"🎯 Intent: {result['query_intent']}, Business: {result['business_type']}")
        print(f"📊 Attempts: {result['attempts']}, Final Confidence: {result['model_confidence']}/10")
        
        # 🚀 Dynamic Optimization Analysis
        opt_perf = result.get('optimization_performance', {})
        semantic_enh = result.get('semantic_enhancement', {})
        
        print(f"🚀 DYNAMIC OPTIMIZATION:")
        print(f"   Status: {opt_perf.get('status', 'unknown')}")
        print(f"   Quality: {semantic_enh.get('quality', 'unknown')} (ratio: {semantic_enh.get('enhancement_ratio', 0)})")
        if semantic_enh.get('sample_enhancements'):
            print(f"   Enhancements: {', '.join(semantic_enh['sample_enhancements'][:3])}")
        
        # GPT Augmentation Analysis
        if result['augmentation_used']:
            print(f"🧠 AUGMENTATION: ✅ SUCCESS (partial: {result['best_partial_confidence']}/10 → final: {result['augmentation_confidence']}/10)")
        elif result['best_partial_confidence'] > 0:
            print(f"🧠 AUGMENTATION: ❌ SKIPPED (had partial: {result['best_partial_confidence']}/10)")
        else:
            print(f"🧠 AUGMENTATION: ⚪ N/A (no partial results)")
        
        # Query Evolution
        query_evolution = result.get('query_evolution', [])
        if query_evolution:
            print(f"🔄 QUERY EVOLUTION:")
            for j, evolution in enumerate(query_evolution):
                opt_type = evolution.get('optimization_type', 'unknown')
                confidence = evolution.get('confidence', 0)
                query_preview = evolution.get('query', '')[:40] + '...' if len(evolution.get('query', '')) > 40 else evolution.get('query', '')
                print(f"   {j+1}. [{opt_type[:8]}] '{query_preview}' → {confidence}/10")
            
        print(f"🔒 Trade Secret: {result['trade_secret_handled']}")
        print(f"⚠️ Escalated: {result['escalated']}")
        print(f"💬 Answer Preview: {result['answer'][:150]}...")
        print("-" * 50)
    
    # Generate enhanced summary statistics
    print_enhanced_summary_statistics(results)
    
    return results

def print_enhanced_summary_statistics(results):
    """Print comprehensive summary statistics with dynamic optimization metrics"""
    print("\n" + "=" * 70)
    print("📈 ENHANCED RAG v3 + DYNAMIC OPTIMIZATION SUMMARY")
    print("=" * 70)
    
    total = len(results)
    successful = len([r for r in results if not r['escalated']])
    augmented = len([r for r in results if r['augmentation_used']])
    had_partial = len([r for r in results if r['best_partial_confidence'] > 0])
    
    # 🚀 Dynamic Optimization Metrics
    dynamic_optimized = len([r for r in results if r.get('optimization_performance', {}).get('status') == 'full_dynamic'])
    semantic_enhanced = len([r for r in results if r.get('semantic_enhancement', {}).get('quality') in ['good', 'excellent']])
    
    print(f"📊 BASIC METRICS:")
    print(f"   Total queries: {total}")
    print(f"   Successful: {successful}/{total} ({successful/total*100:.1f}%)")
    print(f"   Escalated: {total-successful}/{total} ({(total-successful)/total*100:.1f}%)")
    
    print(f"\n🚀 DYNAMIC OPTIMIZATION METRICS:")
    print(f"   Full dynamic optimization: {dynamic_optimized}/{total} ({dynamic_optimized/total*100:.1f}%)")
    print(f"   Semantic enhancement success: {semantic_enhanced}/{total} ({semantic_enhanced/total*100:.1f}%)")
    
    # Calculate average enhancement metrics
    enhancement_ratios = []
    optimization_performances = []
    
    for r in results:
        semantic_enh = r.get('semantic_enhancement', {})
        if 'enhancement_ratio' in semantic_enh:
            enhancement_ratios.append(semantic_enh['enhancement_ratio'])
        
        opt_perf = r.get('optimization_performance', {})
        if opt_perf.get('status') == 'full_dynamic':
            optimization_performances.append(1.0)
        elif opt_perf.get('status') == 'partial_dynamic':
            optimization_performances.append(0.5)
        else:
            optimization_performances.append(0.0)
    
    if enhancement_ratios:
        avg_enhancement = sum(enhancement_ratios) / len(enhancement_ratios)
        print(f"   Average enhancement ratio: {avg_enhancement:.2f}")
    
    if optimization_performances:
        avg_opt_performance = sum(optimization_performances) / len(optimization_performances)
        print(f"   Average optimization performance: {avg_opt_performance:.2f}")
    
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
    
    # 🚀 Dynamic Optimization Quality Analysis
    print(f"\n🚀 DYNAMIC OPTIMIZATION QUALITY BREAKDOWN:")
    quality_counts = {}
    for r in results:
        quality = r.get('semantic_enhancement', {}).get('quality', 'unknown')
        quality_counts[quality] = quality_counts.get(quality, 0) + 1
    
    for quality, count in sorted(quality_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {quality}: {count}")
    
    # Query Evolution Analysis
    print(f"\n🔄 QUERY EVOLUTION ANALYSIS:")
    total_transformations = 0
    unique_transformations = 0
    
    for r in results:
        query_evolution = r.get('query_evolution', [])
        if query_evolution:
            total_transformations += len(query_evolution)
            unique_queries = set(e.get('query', '') for e in query_evolution)
            unique_transformations += len(unique_queries)
    
    print(f"   Total query transformations: {total_transformations}")
    print(f"   Unique transformations: {unique_transformations}")
    print(f"   Average transformations per query: {total_transformations/total:.1f}")

def run_dynamic_optimization_showcase():
    """Showcase dynamic optimization capabilities"""
    print("\n🚀 DYNAMIC OPTIMIZATION SHOWCASE")
    print("=" * 50)
    
    agent = EnhancedEvaluationRAGAgentV2()
    
    # Queries specifically designed to showcase dynamic optimization
    showcase_queries = [
        "jakieś bakterie do startu",  # Vague -> should expand semantically
        "problem z tymi czerwonymi rzeczami",  # Ambiguous -> should identify cyano
        "AF jakiś tam preparat do koralowców",  # Product ambiguity -> should expand product terms
        "wysokie te azoty jak obniżyć",  # Informal -> should formalize to technical terms
        "glony wszędzie ratunku",  # Emotional -> should expand to technical solutions
    ]
    
    print("Testing semantic expansion and domain understanding:")
    
    for i, query in enumerate(showcase_queries, 1):
        print(f"\n🔍 Test {i}: {query}")
        result = agent.ask(query)
        
        # Show query evolution
        query_evolution = result.get('query_evolution', [])
        if query_evolution:
            print("📈 Query Evolution:")
            for j, evolution in enumerate(query_evolution):
                print(f"   Attempt {j+1}: '{evolution.get('query', '')}'")
                print(f"   Confidence: {evolution.get('confidence', 0)}/10")
        
        # Show semantic enhancement
        semantic_enh = result.get('semantic_enhancement', {})
        if semantic_enh.get('sample_enhancements'):
            print(f"🎯 Semantic Enhancements: {', '.join(semantic_enh['sample_enhancements'])}")
        
        print(f"🏆 Final Result: {result['model_confidence']}/10 confidence")

def quick_dynamic_optimization_test():
    """Quick test focusing on dynamic optimization scenarios"""
    print("\n🧠 QUICK DYNAMIC OPTIMIZATION TEST")
    print("=" * 40)
    
    agent = EnhancedEvaluationRAGAgentV2()
    
    # Queries likely to benefit from dynamic optimization
    optimization_candidates = [
        "coś do obniżenia azotanów",
        "jakieś glony na skałach",
        "bakterie na start zbiornika",
        "sól do morskiego akwarium",
        "problem z pH w nocy"
    ]
    
    for query in optimization_candidates:
        print(f"\n🔍 Testing: {query}")
        result = agent.ask(query)
        
        opt_perf = result.get('optimization_performance', {})
        semantic_enh = result.get('semantic_enhancement', {})
        
        if opt_perf.get('status') == 'full_dynamic':
            print(f"   ✅ DYNAMIC OPTIMIZATION SUCCESS!")
            print(f"   Quality: {semantic_enh.get('quality', 'unknown')}")
            print(f"   Enhancement ratio: {semantic_enh.get('enhancement_ratio', 0)}")
        else:
            print(f"   ⚠️ Optimization status: {opt_perf.get('status', 'unknown')}")

def run_interactive_mode_v3():
    """Interactive mode for testing v3 with dynamic optimization"""
    print("\n🤖 ENHANCED EVALUATION RAG v3 - Interactive Mode")
    print("🧠 Now with Dynamic Query Optimization!")
    print("🚀 Features: GPT Augmentation + Semantic Enhancement + Progressive Broadening")
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
        
        # Show optimization results
        opt_perf = result.get('optimization_performance', {})
        semantic_enh = result.get('semantic_enhancement', {})
        
        print(f"🚀 Dynamic Optimization: {opt_perf.get('status', 'unknown')} | Quality: {semantic_enh.get('quality', 'unknown')}")
        
        if result['augmentation_used']:
            print(f"🧠 GPT Augmentation: ✅ USED ({result['best_partial_confidence']}/10 → {result['augmentation_confidence']}/10)")
        elif result['best_partial_confidence'] > 0:
            print(f"🧠 GPT Augmentation: ❌ Available but not used ({result['best_partial_confidence']}/10)")
        
        # Show query evolution
        query_evolution = result.get('query_evolution', [])
        if len(query_evolution) > 1:
            print(f"🔄 Query Evolution ({len(query_evolution)} attempts):")
            for i, evolution in enumerate(query_evolution):
                opt_type = evolution.get('optimization_type', 'unknown')[:8]
                confidence = evolution.get('confidence', 0)
                query_preview = evolution.get('query', '')[:50] + '...' if len(evolution.get('query', '')) > 50 else evolution.get('query', '')
                print(f"   {i+1}. [{opt_type}] '{query_preview}' → {confidence}/10")
        
        print(f"\n💬 **Answer:**")
        print(result['answer'])

if __name__ == "__main__":
    # Run automated tests
    test_enhanced_evaluation_rag_v3()
    
    # Uncomment to run specific showcases
    # run_dynamic_optimization_showcase()
    # quick_dynamic_optimization_test()
    
    # Uncomment for interactive mode
    # run_interactive_mode_v3()