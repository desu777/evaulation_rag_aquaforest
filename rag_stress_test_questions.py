#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG STRESS TEST QUESTIONS dla systemu Aquaforest
Zestaw 60+ pytań testowych w różnych kategoriach i poziomach trudności

Autor: AI Assistant
Data: 2025-01-18
Cel: Testowanie systemu Enhanced Evaluation RAG pod różnymi kątami
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
        """Główny test stress - 60+ pytań w różnych kategoriach"""
        
        print("🌊 AQUAFOREST RAG - COMPREHENSIVE STRESS TEST")
        print("=" * 70)
        print(f"📅 Start: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🎯 Cel: Test 60+ różnorodnych pytań")
        print("📊 Ocena: intent detection, confidence, business handling, trade secrets")
        print("=" * 70)
        
        # Zdefiniuj wszystkie kategorie pytań
        test_categories = {
            "🔰 BEGINNER - Podstawowe": self.beginner_questions(),
            "🏆 EXPERT - Zaawansowane": self.expert_questions(),
            "🚨 PROBLEMS - Troubleshooting": self.problem_solving_questions(),
            "💊 DOSAGE - Dawkowanie": self.dosage_questions(),
            "🔬 PRODUCTS - Informacje o produktach": self.product_info_questions(),
            "⚗️ CHEMISTRY - Chemia wody": self.water_chemistry_questions(),
            "🐠 FISH & CORAL - Hodowla": self.livestock_questions(),
            "🏢 BUSINESS - Pytania biznesowe": self.business_questions(),
            "🔒 TRADE SECRETS - Tajemnice handlowe": self.trade_secret_questions(),
            "🌊 SEAWATER - Akwaria morskie": self.seawater_specific_questions(),
            "🌿 FRESHWATER - Akwaria słodkowodne": self.freshwater_specific_questions(),
            "🧪 LAB - Produkty laboratoryjne": self.lab_questions(),
            "🏛️ OCEANGUARD - Akwaria premium": self.oceanguard_questions(),
            "❓ AMBIGUOUS - Niejednoznaczne": self.ambiguous_questions(),
            "🚀 EDGE CASES - Przypadki graniczne": self.edge_case_questions()
        }
        
        total_questions = sum(len(questions) for questions in test_categories.values())
        print(f"📝 Łączna liczba pytań: {total_questions}")
        print("=" * 70)
        
        current_question = 1
        
        # Wykonaj testy w każdej kategorii
        for category_name, questions in test_categories.items():
            print(f"\n{category_name}")
            print("-" * 50)
            
            for question in questions:
                self.run_single_test(question, current_question, total_questions, category_name)
                current_question += 1
                time.sleep(0.5)  # Krótka przerwa między pytaniami
        
        # Podsumowanie wyników
        self.generate_summary_report()
    
    def run_single_test(self, question: str, current: int, total: int, category: str):
        """Wykonaj pojedynczy test pytania"""
        print(f"\n[{current}/{total}] 🔍 Testing...")
        print(f"❓ {question}")
        
        start_time = time.time()
        try:
            result = self.agent.ask(question)
            end_time = time.time()
            
            # Zapisz szczegółowe wyniki z pełną odpowiedzią i polami v2
            test_result = {
                "question_number": current,
                "category": category,
                "question": question,
                "full_answer": result['answer'],  # 🆕 Pełna odpowiedź zamiast preview
                "answer_preview": result['answer'][:200] + "..." if len(result['answer']) > 200 else result['answer'],
                "intent": result['query_intent'],
                "business_type": result['business_type'],
                "confidence": result['model_confidence'],
                "attempts": result['attempts'],
                "escalated": result['escalated'],
                "trade_secret_handled": result['trade_secret_handled'],
                "response_time": round(end_time - start_time, 2),
                "evaluation_log": result.get('evaluation_log', []),
                # 🆕 NOWE POLA V2 - GPT AUGMENTATION
                "augmentation_used": result.get('augmentation_used', False),
                "augmentation_confidence": result.get('augmentation_confidence', 0.0),
                "best_partial_confidence": result.get('best_partial_confidence', 0.0),
                "attempt_confidences": result.get('attempt_confidences', []),
                "augmentation_reasoning": result.get('augmentation_reasoning', ""),
                "attempt_history": result.get('attempt_history', []),
                "success": True
            }
            
            # Wyświetl wyniki
            self.print_test_results(test_result)
            
        except Exception as e:
            # Obsłuż błędy
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
    
    def print_test_results(self, result: Dict):
        """Wyświetl wyniki pojedynczego testu z informacjami v2"""
        # Kolorowanie na podstawie confidence
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
            
        print(f"🎯 Intent: {result['intent']} | Business: {result['business_type']}")
        print(f"{confidence_emoji} Confidence: {result['confidence']}/10 | Attempts: {result['attempts']} | Time: {result['response_time']}s")
        print(f"🔒 Trade Secret: {result['trade_secret_handled']} | Escalated: {result['escalated']}")
        print(f"{augmentation_status}")
        if result.get('attempt_confidences'):
            print(f"📊 Attempt Confidences: {result['attempt_confidences']}")
        print(f"💬 Preview: {result['answer_preview']}")
    
    def beginner_questions(self) -> List[str]:
        """Pytania dla początkujących akwarystów"""
        return [
            "Jak założyć pierwsze akwarium morskie?",
            "Co to jest cykl azotowy?",
            "Jakiej soli użyć do akwarium morskiego?",
            "Jak długo dojrzewa akwarium?",
            "Co to są bakterie nitryfikacyjne?",
            "Jak karmić ryby akwariowe?",
            "Jakie testy wody są najważniejsze?",
            "Co to są probiotyki w akwarium?",
            "Jak często robić podmiany wody?",
            "Jakie oświetlenie wybrać do akwarium?"
        ]
    
    def expert_questions(self) -> List[str]:
        """Pytania dla doświadczonych akwarystów"""
        return [
            "Optymalizacja parametrów wody dla koralowców SPS przy użyciu metody Ballinga",
            "Jak interpretować wyniki testu ICP dla rafowego akwarium mieszanego?",
            "Component Strong A vs standardowy Component A - różnice w aplikacji",
            "Wpływ porowatości Live Rock na efektywność denitryfikacji",
            "Hybrydowe sole naturalno-syntetyczne - zalety technologiczne",
            "Implementacja Metody Probiotycznej™ w systemie reef tank 1000L",
            "Biogeochemiczny cykl siarki w akwarium z suplementacją AF Lab",
            "Mikroelementy w kulturze zooxantelli - rola magnezu i strontu"
        ]
    
    def problem_solving_questions(self) -> List[str]:
        """Pytania dotyczące rozwiązywania problemów"""
        return [
            "Cyjanobakterie pokryły całe dno akwarium - jak walczyć?",
            "Ospa rybia u wszystkich ryb - natychmiastowe działanie",
            "Wysokie fosforany 0.5 ppm - szybkie obniżenie",
            "Glony nitkowate duszczą koralowce - ratunek",
            "Spadek pH poniżej 7.8 w nocy - przyczyny i rozwiązania",
            "Białe plamy na koralowcach LPS - diagnoza",
            "Rybki gasną przy powierzchni - problemy z tlenem",
            "Metoda probiotyczna nie działa - co robię źle?",
            "Niskie alkaliczność 6 dKH - jak podnieść bezpiecznie?",
            "Zamętnienie wody po dodaniu bakterii - czy to normalne?"
        ]
    
    def dosage_questions(self) -> List[str]:
        """Pytania o dawkowanie produktów"""
        return [
            "AF Power Elixir dawkowanie na 500L akwarium rafowe",
            "Component 1+2+3 ile ml dziennie na 200L?",
            "KH Pro dawka dla utrzymania 8.5 dKH",
            "Pro Bio S ile kapsułek na 100L obsady mieszanej?",
            "AF Vitality częstotliwość podawania dla LPS",
            "Life Bio Fil ilość na start 300L akwarium",
            "Hybrid Pro Salt proporcje na 50L wody",
            "AF Energy dawkowanie dla koralowców SPS",
            "Carbon dozowanie w reaktorze na 400L",
            "Kalium dawka przy niskich poziomach K+"
        ]
    
    def product_info_questions(self) -> List[str]:
        """Pytania o informacje produktowe"""
        return [
            "Component Strong A - dokładny skład i zastosowanie",
            "Czym różni się Reef Salt od Hybrid Pro Salt?",
            "AF K Boost - jaki rodzaj potasu zawiera?",
            "Pro Bio F - mechanizm działania probiotyków",
            "Zeomix - jak często wymieniać medium?",
            "AF Test Pro Pack - jakie parametry bada?",
            "Stone Fix - czas wiązania i wytrzymałość",
            "AF Plug Rocks - rozmiary i zastosowanie",
            "Liquid Vege składniki aktywne",
            "Magnesium Test Kit - dokładność pomiarów"
        ]
    
    def water_chemistry_questions(self) -> List[str]:
        """Pytania o chemię wody"""
        return [
            "Optimalne parametry wody dla koralowców miękkich",
            "Relacja kalsium do magnezu w akwarium rafowym",
            "Buforowanie pH w systemie zamkniętym",
            "Denitryfikacja vs filtracja biologiczna",
            "Osmoza odwrócona - jakie TDS po filtracji?",
            "Alkaliczność a stabilność pH w ciągu doby",
            "Mikroelementy - które są najważniejsze dla SPS?",
            "Zasolenie 1.025 czy 1.026 - różnice praktyczne",
            "Fosforany organiczne vs nieorganiczne",
            "Żelazo w akwarium rafowym - kiedy suplementować?"
        ]
    
    def livestock_questions(self) -> List[str]:
        """Pytania o hodowlę ryb i koralowców"""
        return [
            "Aklimatyzacja Anthias do nowego akwarium",
            "Koralowce LPS - wymagania świetlne",
            "Kwarantanna nowych ryb - procedura krok po kroku",
            "Rozmnażanie koralowców miękkich w akwarium",
            "Kompatybilność ryb w 200L rafie mieszanej",
            "Karmienie koralowców SPS - naturalne vs sztuczne",
            "Choroby skóry u ryb morskich - identyfikacja",
            "Stres u ryb - objawy i przeciwdziałanie",
            "Optymalna temperatura dla tropikalnej rafy",
            "Dojrzałość płciowa Amphiprion ocellaris"
        ]
    
    def business_questions(self) -> List[str]:
        """Pytania biznesowe - test business handler"""
        return [
            "Chcielibyśmy zostać dystrybutorem Aquaforest w naszym regionie",
            "Warunki współpracy handlowej z Aquaforest",
            "Jak nawiązać partnership z waszą firmą?",
            "Wholesale pricing dla sklepów akwarystycznych",
            "Reprezentacja marki Aquaforest - wymagania",
            "Dołączenie do sieci dealerów Aquaforest"
        ]
    
    def trade_secret_questions(self) -> List[str]:
        """Pytania o tajemnice handlowe - test filtra"""
        return [
            "Jak powstaje AF Power Elixir - proces produkcji?",
            "Dokładna receptura Hybrid Pro Salt",
            "Sposób wytwarzania bakterii probiotycznych Pro Bio S",
            "Technologia produkcji Component Strong A",
            "Jak Aquaforest wytwarza swoje produkty?",
            "Metoda produkcji soli Reef Salt Plus",
            "Proces technologiczny AF Rock"
        ]
    
    def seawater_specific_questions(self) -> List[str]:
        """Pytania specyficzne dla akwariów morskich"""
        return [
            "Rafa SPS - kompletna suplementacja dla 400L",
            "Metoda Ballinga vs Balling Light - porównanie",
            "Skimmer protein - dobór do akwarium 600L",
            "Live Rock maturation - czas i procedura",
            "Refugium makroalgi - wybór gatunków",
            "Calcium reactor vs dozowanie AF Components"
        ]
    
    def freshwater_specific_questions(self) -> List[str]:
        """Pytania o akwaria słodkowodne"""
        return [
            "Start akwarium roślinnego 200L z CO2",
            "AF Life Essence - dawkowanie w nowym zbiorniku",
            "Podłoże dla roślin akwariowych - wybór",
            "Nawożenie akwarium holenderskiego",
            "Glony zielone na szybach - metody usuwania"
        ]
    
    def lab_questions(self) -> List[str]:
        """Pytania o produkty laboratoryjne"""
        return [
            "AF Test ICP 1 vs ICP 2 - różnice w analizie",
            "Barium poziom docelowy w rafie SPS",
            "Strontium suplementacja - dawki laboratoryjne",
            "Bromium w akwarium - kiedy stosować?",
            "Chlorium poziomy optymalne"
        ]
    
    def oceanguard_questions(self) -> List[str]:
        """Pytania o akwaria OceanGuard"""
        return [
            "OceanGuard 980L - specyfikacja techniczna",
            "Porównanie OceanGuard 435L vs 605L",
            "Filtracj w systemach OceanGuard",
            "Koszt utrzymania OceanGuard 790L miesięcznie"
        ]
    
    def ambiguous_questions(self) -> List[str]:
        """Pytania niejednoznaczne - test trudnych przypadków"""
        return [
            "Moja rybka chora co robić?",
            "Najlepszy produkt Aquaforest",
            "Ile kosztuje akwarium?",
            "Czy można mieszać produkty?",
            "Problem z wodą pomocy",
            "Coś nie gra z moim tankiem"
        ]
    
    def edge_case_questions(self) -> List[str]:
        """Przypadki graniczne - test robustności"""
        return [
            "",  # Puste pytanie
            "askldjaksjd aslkdj aslkdj",  # Nonsens
            "Aquaforest" * 50,  # Bardzo długie
            "123456789",  # Tylko cyfry
            "How much Component A for 100L tank?",  # Angielski
            "Qu'est-ce que c'est Component 1?",  # Francuski
            "?!@#$%^&*()",  # Znaki specjalne
            "a",  # Jedno słowo
            "czy można używać produktów aquaforest w akwarium słodkowodnym morskim rafowym nano 10L 1000L jednocześnie",  # Konfuzyjne
        ]
    
    def generate_summary_report(self):
        """Wygeneruj raport podsumowujący z metrykami v2"""
        print("\n" + "=" * 70)
        print("📊 ENHANCED RAG v2 STRESS TEST REPORT")
        print("=" * 70)
        
        successful_tests = [r for r in self.results if r.get('success', False)]
        failed_tests = [r for r in self.results if not r.get('success', False)]
        
        # 🆕 AUGMENTATION METRICS
        augmented_tests = [r for r in successful_tests if r.get('augmentation_used', False)]
        partial_available = [r for r in successful_tests if r.get('best_partial_confidence', 0) > 0]
        
        print(f"✅ Successful tests: {len(successful_tests)}/{len(self.results)}")
        print(f"❌ Failed tests: {len(failed_tests)}")
        print(f"📈 Success rate: {len(successful_tests)/len(self.results)*100:.1f}%")
        print(f"🧠 GPT Augmentation used: {len(augmented_tests)}/{len(successful_tests)} ({len(augmented_tests)/len(successful_tests)*100:.1f}%)" if successful_tests else "")
        print(f"📊 Partial results available: {len(partial_available)}/{len(successful_tests)} ({len(partial_available)/len(successful_tests)*100:.1f}%)" if successful_tests else "")
        
        if successful_tests:
            avg_confidence = sum(r['confidence'] for r in successful_tests) / len(successful_tests)
            avg_response_time = sum(r['response_time'] for r in successful_tests) / len(successful_tests)
            avg_attempts = sum(r['attempts'] for r in successful_tests) / len(successful_tests)
            
            print(f"📊 Average confidence: {avg_confidence:.1f}/10")
            print(f"⏱️ Average response time: {avg_response_time:.2f}s")
            print(f"🔄 Average attempts: {avg_attempts:.1f}")
            
            # 🆕 AUGMENTATION DETAILED METRICS
            if augmented_tests:
                avg_augmented_confidence = sum(r.get('augmentation_confidence', 0) for r in augmented_tests) / len(augmented_tests)
                avg_partial_confidence = sum(r.get('best_partial_confidence', 0) for r in partial_available) / len(partial_available) if partial_available else 0
                print(f"🧠 Average augmented confidence: {avg_augmented_confidence:.1f}/10")
                print(f"📊 Average partial confidence: {avg_partial_confidence:.1f}/10")
            
            # Analiza intencji
            intent_counts = {}
            for result in successful_tests:
                intent = result['intent']
                intent_counts[intent] = intent_counts.get(intent, 0) + 1
            
            print(f"\n🎯 Intent Distribution:")
            for intent, count in sorted(intent_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"   {intent}: {count}")
            
            # Analiza confidence
            high_confidence = len([r for r in successful_tests if r['confidence'] >= 8.0])
            medium_confidence = len([r for r in successful_tests if 6.0 <= r['confidence'] < 8.0])
            low_confidence = len([r for r in successful_tests if r['confidence'] < 6.0])
            
            print(f"\n📈 Confidence Distribution:")
            print(f"   🟢 High (8.0+): {high_confidence} ({high_confidence/len(successful_tests)*100:.1f}%)")
            print(f"   🟡 Medium (6.0-7.9): {medium_confidence} ({medium_confidence/len(successful_tests)*100:.1f}%)")
            print(f"   🔴 Low (<6.0): {low_confidence} ({low_confidence/len(successful_tests)*100:.1f}%)")
            
            # 🆕 AUGMENTATION BREAKDOWN BY CATEGORY
            print(f"\n🧠 Augmentation Usage by Category:")
            categories = {}
            for result in successful_tests:
                category = result.get('category', 'Unknown')
                if category not in categories:
                    categories[category] = {'total': 0, 'augmented': 0, 'partial_available': 0}
                categories[category]['total'] += 1
                if result.get('augmentation_used', False):
                    categories[category]['augmented'] += 1
                if result.get('best_partial_confidence', 0) > 0:
                    categories[category]['partial_available'] += 1
            
            for category, stats in sorted(categories.items(), key=lambda x: x[1]['augmented'], reverse=True):
                if stats['total'] > 0:
                    aug_rate = stats['augmented'] / stats['total'] * 100
                    partial_rate = stats['partial_available'] / stats['total'] * 100
                    print(f"   {category}: {stats['augmented']}/{stats['total']} augmented ({aug_rate:.1f}%), {stats['partial_available']} partial ({partial_rate:.1f}%)")
        
        # Zapisz wyniki do pliku
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"rag_stress_test_results_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "test_summary": {
                    "total_questions": len(self.results),
                    "successful": len(successful_tests),
                    "failed": len(failed_tests),
                    "success_rate": len(successful_tests)/len(self.results)*100,
                    "timestamp": datetime.now().isoformat()
                },
                "detailed_results": self.results
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Detailed results saved to: {filename}")
        print("=" * 70)

def main():
    """Uruchom comprehensive stress test"""
    tester = AquaforestRAGStressTester()
    tester.run_comprehensive_stress_test()

if __name__ == "__main__":
    main() 