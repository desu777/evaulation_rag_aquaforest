#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG STRESS TEST QUESTIONS for Aquaforest System - Enhanced with Dynamic Optimization
Comprehensive set of 116+ test questions across different categories and difficulty levels

Author: AI Assistant
Date: 2025-06-05
Purpose: Testing Enhanced Evaluation RAG v2 with Dynamic Query Optimization
"""

from agent import EnhancedEvaluationRAGAgentV2
import time
import json
from typing import Dict, List
from datetime import datetime

class AquaforestRAGStressTester:
    def __init__(self):
        self.agent = EnhancedEvaluationRAGAgentV2()
        self.results = []
        
    def run_comprehensive_stress_test(self):
        """Main stress test - reduced to ~30 questions across different categories"""
        
        print("🌊 AQUAFOREST RAG - COMPACT STRESS TEST v3")
        print("=" * 70)
        print(f"📅 Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Goal: Test ~30 diverse questions (reduced for file size)")
        print("📊 Evaluation: intent detection, confidence, business handling, dynamic optimization")
        print("🚀 NEW: Dynamic Query Optimization + Multi-Query Search")
        print("=" * 70)
        
        # Define all test categories
        test_categories = {
            "🔰 BEGINNER - Basic": self.beginner_questions(),
            "🏆 EXPERT - Advanced": self.expert_questions(),
            "🚨 PROBLEMS - Troubleshooting": self.problem_solving_questions(),
            "💊 DOSAGE - Dosing": self.dosage_questions(),
            "🔬 PRODUCTS - Product Info": self.product_info_questions(),
            "⚗️ CHEMISTRY - Water Chemistry": self.water_chemistry_questions(),
            "🐠 FISH & CORAL - Livestock": self.livestock_questions(),
            "🏢 BUSINESS - Business Queries": self.business_questions(),
            "🔒 TRADE SECRETS - Trade Secrets": self.trade_secret_questions(),
            "🌊 SEAWATER - Marine Specific": self.seawater_specific_questions(),
            "🌿 FRESHWATER - Freshwater Specific": self.freshwater_specific_questions(),
            "🧪 LAB - Laboratory Products": self.lab_questions(),
            "🏛️ OCEANGUARD - Premium Aquariums": self.oceanguard_questions(),
            "❓ AMBIGUOUS - Ambiguous Queries": self.ambiguous_questions(),
            "🚀 EDGE CASES - Edge Cases": self.edge_case_questions(),
            "🧠 DYNAMIC OPT - Dynamic Optimization Test": self.dynamic_optimization_test_questions()  # 🆕 NEW
        }
        
        total_questions = sum(len(questions) for questions in test_categories.values())
        print(f"📝 Total questions: {total_questions}")
        print("=" * 70)
        
        current_question = 1
        
        # Execute tests in each category
        for category_name, questions in test_categories.items():
            print(f"\n{category_name}")
            print("-" * 50)
            
            for question in questions:
                self.run_single_test(question, current_question, total_questions, category_name)
                current_question += 1
                time.sleep(0.5)  # Short pause between questions
        
        # Generate summary report
        self.generate_enhanced_summary_report()
    
    def run_single_test(self, question: str, current: int, total: int, category: str):
        """Execute single question test"""
        print(f"\n[{current}/{total}] 🔍 Testing...")
        print(f"❓ {question}")
        
        start_time = time.time()
        try:
            result = self.agent.ask(question)
            end_time = time.time()
            
            # 🆕 ENHANCED RESULT TRACKING with Dynamic Optimization metrics
            test_result = {
                "question_number": current,
                "category": category,
                "question": question,
                "full_answer": result['answer'],
                "answer_preview": result['answer'][:200] + "..." if len(result['answer']) > 200 else result['answer'],
                "intent": result['query_intent'],
                "business_type": result['business_type'],
                "confidence": result['model_confidence'],
                "attempts": result['attempts'],
                "escalated": result['escalated'],
                "trade_secret_handled": result['trade_secret_handled'],
                "response_time": round(end_time - start_time, 2),
                "evaluation_log": result.get('evaluation_log', []),
                
                # GPT Augmentation metrics (v2) - only essential fields
                "augmentation_used": result.get('augmentation_used', False),
                "augmentation_confidence": result.get('augmentation_confidence', 0.0),
                "best_partial_confidence": result.get('best_partial_confidence', 0.0),
                
                # 🆕 NEW: Dynamic Optimization metrics - only query transformations for analysis
                "optimization_type": self._extract_optimization_type(result),
                "query_transformations": self._extract_query_transformations(result),
                "semantic_enhancement": self._analyze_semantic_enhancement(question, result),
                "progressive_broadening": self._analyze_progressive_broadening(result),
                
                "success": True
            }
            
            # Display enhanced results
            self.print_enhanced_test_results(test_result)
            
        except Exception as e:
            # Handle errors
            test_result = {
                "question_number": current,
                "category": category,
                "question": question,
                "error": str(e),
                "success": False,
                "response_time": time.time() - start_time
            }
            print(f"❌ ERROR: {e}")
        
        self.results.append(test_result)
    
    def _extract_optimization_type(self, result: Dict) -> str:
        """Extract optimization type from attempt history"""
        attempt_history = result.get('attempt_history', [])
        for attempt in attempt_history:
            if attempt.get('optimization_type'):
                return attempt['optimization_type']
        return "unknown"
    
    def _extract_query_transformations(self, result: Dict) -> List[str]:
        """Extract query transformations from attempt history"""
        attempt_history = result.get('attempt_history', [])
        transformations = []
        for attempt in attempt_history:
            if 'optimized_query' in attempt:
                transformations.append(attempt['optimized_query'])
        return transformations
    

    
    def _analyze_semantic_enhancement(self, original_question: str, result: Dict) -> Dict:
        """Analyze semantic enhancement quality"""
        transformations = self._extract_query_transformations(result)
        if not transformations:
            return {"quality": "none", "score": 0}
        
        # Simple analysis - in production this could be more sophisticated
        original_words = set(original_question.lower().split())
        enhanced_words = set()
        for transformation in transformations:
            enhanced_words.update(transformation.lower().split())
        
        new_semantic_words = enhanced_words - original_words
        enhancement_ratio = len(new_semantic_words) / len(original_words) if original_words else 0
        
        if enhancement_ratio > 1.5:
            quality = "excellent"
            score = 10
        elif enhancement_ratio > 1.0:
            quality = "good"
            score = 7
        elif enhancement_ratio > 0.5:
            quality = "moderate"
            score = 5
        else:
            quality = "minimal"
            score = 3
        
        return {
            "quality": quality,
            "score": score,
            "enhancement_ratio": round(enhancement_ratio, 2),
            "new_semantic_words": len(new_semantic_words),
            "sample_enhancements": list(new_semantic_words)[:5]
        }
    
    def _analyze_progressive_broadening(self, result: Dict) -> Dict:
        """Analyze progressive query broadening strategy"""
        transformations = self._extract_query_transformations(result)
        if len(transformations) < 2:
            return {"effectiveness": "insufficient_data", "broadening_detected": False}
        
        # Analyze if queries became progressively broader
        word_counts = [len(t.split()) for t in transformations]
        is_progressive = all(word_counts[i] <= word_counts[i+1] for i in range(len(word_counts)-1))
        
        return {
            "effectiveness": "good" if is_progressive else "needs_improvement",
            "broadening_detected": is_progressive,
            "word_progression": word_counts,
            "strategy_consistency": is_progressive
        }
    
    def print_enhanced_test_results(self, result: Dict):
        """Display enhanced test results with dynamic optimization metrics"""
        # Confidence coloring
        if result['confidence'] >= 8.0:
            confidence_emoji = "🟢"
        elif result['confidence'] >= 6.0:
            confidence_emoji = "🟡"
        else:
            confidence_emoji = "🔴"
        
        # Augmentation status
        if result.get('augmentation_used', False):
            augmentation_status = f"🧠 AUGMENTATION: ✅ USED ({result.get('best_partial_confidence', 0)}/10 → {result.get('augmentation_confidence', 0)}/10)"
        elif result.get('best_partial_confidence', 0) > 0:
            augmentation_status = f"🧠 AUGMENTATION: ⚪ AVAILABLE ({result.get('best_partial_confidence', 0)}/10) but not used"
        else:
            augmentation_status = "🧠 AUGMENTATION: ❌ N/A"
        
        # 🆕 Dynamic Optimization status
        opt_type = result.get('optimization_type', 'unknown')
        semantic_enhancement = result.get('semantic_enhancement', {})
        opt_quality = semantic_enhancement.get('quality', 'unknown')
        
        dynamic_opt_status = f"🚀 DYNAMIC OPT: {opt_type} | Quality: {opt_quality}"
        
        print(f"🎯 Intent: {result['intent']} | Business: {result['business_type']}")
        print(f"{confidence_emoji} Confidence: {result['confidence']}/10 | Attempts: {result['attempts']} | Time: {result['response_time']}s")
        print(f"🔒 Trade Secret: {result['trade_secret_handled']} | Escalated: {result['escalated']}")
        print(f"{augmentation_status}")
        print(f"{dynamic_opt_status}")
        
        if result.get('query_transformations'):
            print(f"🔄 Query Evolution: {len(result['query_transformations'])} transformations")
            for i, transform in enumerate(result['query_transformations'][:2], 1):  # Show first 2
                print(f"   {i}. '{transform[:60]}{'...' if len(transform) > 60 else ''}'")
        
        print(f"💬 Preview: {result['answer_preview']}")
    
    def dynamic_optimization_test_questions(self) -> List[str]:
        """🆕 NEW: Questions specifically designed to test dynamic optimization"""
        return [
            "co poleca na start morskiego",  # Semantic expansion test
            "problem z czerwonymi bakteriami",  # Semantic understanding test
            "AF coś tam do koralowców",  # Ambiguous product reference
            "wysokie NO3 jak obniżyć",  # Technical synonym expansion
            "jakie sole najlepsze do rafy",  # Product comparison broadening
            "dawka tego preparatu z aminokwasami",  # Indirect product reference
            "glony na wszystkim jak pozbyć",  # Problem description expansion
            "bakterie do nowego zbiornika",  # Context-aware optimization
            "pH spadło nocą co robić",  # Technical problem expansion
            "koralowce nie rosną pomoc"  # Multi-aspect problem
        ]
    
    # Original question categories (keeping all existing methods)
    def beginner_questions(self) -> List[str]:
        """Questions for beginner aquarists - reduced to 3 questions"""
        return [
            "Jak założyć pierwsze akwarium morskie?",
            "Co to jest cykl azotowy?",
            "Jakiej soli użyć do akwarium morskiego?"
        ]
    
    def expert_questions(self) -> List[str]:
        """Questions for experienced aquarists - reduced to 2 questions"""
        return [
            "Optymalizacja parametrów wody dla koralowców SPS przy użyciu metody Ballinga",
            "Component B vs Micro E "
        ]
    
    def problem_solving_questions(self) -> List[str]:
        """Problem-solving questions - reduced to 3 questions"""
        return [
            "Cyjanobakterie pokryły całe dno akwarium - jak walczyć?",
            "Wysokie fosforany 0.5 ppm - szybkie obniżenie",
            "Spadek pH poniżej 7.8 w nocy - przyczyny i rozwiązania"
        ]
    
    def dosage_questions(self) -> List[str]:
        """Dosing questions - reduced to 2 questions"""
        return [
            "AF Power Elixir dawkowanie na 500L akwarium rafowe",
            "Component 1+2+3 ile ml dziennie na 200L?"
        ]
    
    def product_info_questions(self) -> List[str]:
        """Product information questions - reduced to 2 questions"""
        return [
            "Component Strong A - dokładny skład i zastosowanie",
            "Czym różni się Reef Salt od Hybrid Pro Salt?"
        ]
    
    def water_chemistry_questions(self) -> List[str]:
        """Water chemistry questions - reduced to 2 questions"""
        return [
            "Optimalne parametry wody dla koralowców miękkich",
            "Relacja kalsium do magnezu w akwarium rafowym"
        ]
    
    def livestock_questions(self) -> List[str]:
        """Fish and coral husbandry questions - reduced to 2 questions"""
        return [
            "Aklimatyzacja Anthias do nowego akwarium",
            "Koralowce LPS - wymagania świetlne"
        ]
    
    def business_questions(self) -> List[str]:
        """Business questions - test business handler - reduced to 2 questions"""
        return [
            "Chcielibyśmy zostać dystrybutorem Aquaforest w naszym regionie",
            "Warunki współpracy handlowej z Aquaforest"
        ]
    
    def trade_secret_questions(self) -> List[str]:
        """Trade secret questions - test filter - reduced to 2 questions"""
        return [
            "Jak powstaje AF Power Elixir - proces produkcji?",
            "Dokładna receptura Hybrid Pro Salt"
        ]
    
    def seawater_specific_questions(self) -> List[str]:
        """Marine aquarium specific questions - reduced to 2 questions"""
        return [
            "Rafa SPS - kompletna suplementacja dla 400L",
            "Metoda Ballinga vs Balling Light - porównanie"
        ]
    
    def freshwater_specific_questions(self) -> List[str]:
        """Freshwater aquarium questions - reduced to 1 question"""
        return [
            "Start akwarium roślinnego 200L z CO2"
        ]
    
    def lab_questions(self) -> List[str]:
        """Laboratory product questions - reduced to 1 question"""
        return [
            "AF Test ICP 1 vs ICP 2 - różnice w analizie"
        ]
    
    def oceanguard_questions(self) -> List[str]:
        """OceanGuard aquarium questions - reduced to 1 question"""
        return [
            "OceanGuard 980L - specyfikacja techniczna"
        ]
    
    def ambiguous_questions(self) -> List[str]:
        """Ambiguous questions - test difficult cases - reduced to 2 questions"""
        return [
            "Moja rybka chora co robić?",
            "Najlepszy produkt Aquaforest"
        ]
    
    def edge_case_questions(self) -> List[str]:
        """Edge cases - test robustness - reduced to 3 questions"""
        return [
            "askldjaksjd aslkdj aslkdj",  # Nonsense
            "How much Component A for 100L tank?",  # English
            "czy można używać produktów aquaforest w akwarium słodkowodnym morskim rafowym nano 10L 1000L jednocześnie"  # Confusing
        ]
    
    def generate_enhanced_summary_report(self):
        """Generate enhanced summary report with dynamic optimization metrics"""
        print("\n" + "=" * 70)
        print("📊 ENHANCED RAG v2 + DYNAMIC OPTIMIZATION STRESS TEST REPORT")
        print("=" * 70)
        
        successful_tests = [r for r in self.results if r.get('success', False)]
        failed_tests = [r for r in self.results if not r.get('success', False)]
        
        # Augmentation metrics
        augmented_tests = [r for r in successful_tests if r.get('augmentation_used', False)]
        partial_available = [r for r in successful_tests if r.get('best_partial_confidence', 0) > 0]
        
        # 🆕 Dynamic Optimization metrics
        dynamic_opt_tests = [r for r in successful_tests if r.get('optimization_type') == 'dynamic_llm_based']
        semantic_enhanced = [r for r in successful_tests if r.get('semantic_enhancement', {}).get('quality') in ['good', 'excellent']]
        
        print(f"✅ Successful tests: {len(successful_tests)}/{len(self.results)}")
        print(f"❌ Failed tests: {len(failed_tests)}")
        print(f"📈 Success rate: {len(successful_tests)/len(self.results)*100:.1f}%")
        print(f"🧠 GPT Augmentation used: {len(augmented_tests)}/{len(successful_tests)} ({len(augmented_tests)/len(successful_tests)*100:.1f}%)" if successful_tests else "")
        print(f"🚀 Dynamic Optimization used: {len(dynamic_opt_tests)}/{len(successful_tests)} ({len(dynamic_opt_tests)/len(successful_tests)*100:.1f}%)" if successful_tests else "")
        print(f"🎯 Semantic Enhancement quality: {len(semantic_enhanced)}/{len(successful_tests)} ({len(semantic_enhanced)/len(successful_tests)*100:.1f}%)" if successful_tests else "")
        
        if successful_tests:
            avg_confidence = sum(r['confidence'] for r in successful_tests) / len(successful_tests)
            avg_response_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
            avg_attempts = sum(r['attempts'] for r in successful_tests) / len(successful_tests)
            
            print(f"📊 Average confidence: {avg_confidence:.1f}/10")
            print(f"⏱️ Average response time: {avg_response_time:.2f}s")
            print(f"🔄 Average attempts: {avg_attempts:.1f}")
            
            # Augmentation detailed metrics
            if augmented_tests:
                avg_augmented_confidence = sum(r.get('augmentation_confidence', 0) for r in augmented_tests) / len(augmented_tests)
                avg_partial_confidence = sum(r.get('best_partial_confidence', 0) for r in partial_available) / len(partial_available) if partial_available else 0
                print(f"🧠 Average augmented confidence: {avg_augmented_confidence:.1f}/10")
                print(f"📊 Average partial confidence: {avg_partial_confidence:.1f}/10")
            
            # 🆕 Dynamic Optimization detailed metrics
            if semantic_enhanced:
                avg_enhancement_score = sum(r.get('semantic_enhancement', {}).get('score', 0) for r in semantic_enhanced) / len(semantic_enhanced)
                avg_enhancement_ratio = sum(r.get('semantic_enhancement', {}).get('enhancement_ratio', 0) for r in semantic_enhanced) / len(semantic_enhanced)
                print(f"🎯 Average semantic enhancement score: {avg_enhancement_score:.1f}/10")
                print(f"🔄 Average enhancement ratio: {avg_enhancement_ratio:.2f}")
            
            # Intent analysis
            intent_counts = {}
            for result in successful_tests:
                intent = result['intent']
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            print(f"\n🎯 Intent Distribution:")
            for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"   {intent}: {count}")
            
            # Confidence distribution
            high_confidence = len([r for r in successful_tests if r['confidence'] >= 8.0])
            medium_confidence = len([r for r in successful_tests if 6.0 <= r['confidence'] < 8.0])
            low_confidence = len([r for r in successful_tests if r['confidence'] < 6.0])
            
            print(f"\n📈 Confidence Distribution:")
            print(f"   🟢 High (8.0+): {high_confidence} ({high_confidence/len(successful_tests)*100:.1f}%)")
            print(f"   🟡 Medium (6.0-7.9): {medium_confidence} ({medium_confidence/len(successful_tests)*100:.1f}%)")
            print(f"   🔴 Low (<6.0): {low_confidence} ({low_confidence/len(successful_tests)*100:.1f}%)")
            
            # 🆕 Dynamic Optimization Analysis by Category
            print(f"\n🚀 Dynamic Optimization Performance by Category:")
            categories = {}
            for result in successful_tests:
                category = result.get('category', 'Unknown')
                if category not in categories:
                    categories[category] = {
                        'total': 0, 'dynamic_opt': 0, 'semantic_enhanced': 0,
                        'avg_enhancement_score': 0, 'enhancement_scores': []
                    }
                categories[category]['total'] += 1
                if result.get('optimization_type') == 'dynamic_llm_based':
                    categories[category]['dynamic_opt'] += 1
                semantic_qual = result.get('semantic_enhancement', {}).get('quality', 'none')
                if semantic_qual in ['good', 'excellent']:
                    categories[category]['semantic_enhanced'] += 1
                    categories[category]['enhancement_scores'].append(
                        result.get('semantic_enhancement', {}).get('score', 0)
                    )
            
            for category, stats in sorted(categories.items(), key=lambda x: x[1]['semantic_enhanced'], reverse=True):
                if stats['total'] > 0:
                    dynamic_rate = stats['dynamic_opt'] / stats['total'] * 100
                    semantic_rate = stats['semantic_enhanced'] / stats['total'] * 100
                    avg_score = sum(stats['enhancement_scores']) / len(stats['enhancement_scores']) if stats['enhancement_scores'] else 0
                    print(f"   {category}:")
                    print(f"     Dynamic: {stats['dynamic_opt']}/{stats['total']} ({dynamic_rate:.1f}%)")
                    print(f"     Semantic: {stats['semantic_enhanced']}/{stats['total']} ({semantic_rate:.1f}%, avg score: {avg_score:.1f})")
        
        # Save enhanced results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_rag_stress_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "test_summary": {
                    "total_questions": len(self.results),
                    "successful": len(successful_tests),
                    "failed": len(failed_tests),
                    "success_rate": len(successful_tests)/len(self.results)*100,
                    "dynamic_optimization_rate": len(dynamic_opt_tests)/len(successful_tests)*100 if successful_tests else 0,
                    "semantic_enhancement_rate": len(semantic_enhanced)/len(successful_tests)*100 if successful_tests else 0,
                    "timestamp": datetime.now().isoformat(),
                    "version": "Enhanced RAG v2 + Dynamic Optimization"
                },
                "detailed_results": self.results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Enhanced results saved to: {filename}")
        print("=" * 70)

def main():
    """Run comprehensive stress test with dynamic optimization"""
    tester = AquaforestRAGStressTester()
    tester.run_comprehensive_stress_test()

if __name__ == "__main__":
    main()