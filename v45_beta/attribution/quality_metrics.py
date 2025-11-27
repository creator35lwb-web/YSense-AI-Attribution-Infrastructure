"""
YSenseAI v4.5-Beta: Quality Metrics Calculator
Training optimization signals based on context engineering principles
"""

import re
from typing import Dict, List
from collections import Counter

class QualityMetricsCalculator:
    """
    Calculate 6 quality metrics for AI training optimization
    Based on Manus context engineering principles
    """
    
    def __init__(self):
        self.weights = {
            "context_efficiency": 0.15,
            "reasoning_depth": 0.25,
            "cultural_specificity": 0.20,
            "emotional_richness": 0.15,
            "attention_density": 0.15,
            "compression_quality": 0.10
        }
        
        # Cultural markers (expandable)
        self.cultural_markers = [
            "grandmother", "tradition", "ritual", "ceremony", "ancestor",
            "heritage", "indigenous", "local", "community", "elder",
            "sacred", "spirit", "blessing", "prayer", "temple",
            "mosque", "church", "shrine", "festival", "celebration"
        ]
        
        # Emotional descriptors
        self.emotional_words = [
            "feel", "felt", "emotion", "heart", "soul", "warmth",
            "cold", "tight", "open", "heavy", "light", "joy",
            "sadness", "anger", "fear", "love", "nostalgia",
            "reverence", "awe", "peace", "tension", "comfort"
        ]
    
    def calculate_all_metrics(self,
                             raw_story: str,
                             layer_responses: Dict[str, str],
                             distilled_essence: List[str]) -> Dict[str, float]:
        """
        Calculate all 6 quality metrics
        
        Returns:
            Dictionary of metric scores (0.0 to 1.0)
        """
        
        # Combine all text for analysis
        all_text = raw_story + " " + " ".join(layer_responses.values())
        
        scores = {
            "context_efficiency": self._calculate_context_efficiency(all_text),
            "reasoning_depth": self._calculate_reasoning_depth(layer_responses),
            "cultural_specificity": self._calculate_cultural_specificity(all_text),
            "emotional_richness": self._calculate_emotional_richness(all_text),
            "attention_density": self._calculate_attention_density(layer_responses),
            "compression_quality": self._calculate_compression_quality(
                all_text, distilled_essence
            )
        }
        
        # Calculate overall score (weighted average)
        overall = sum(scores[k] * self.weights[k] for k in scores.keys())
        scores["overall"] = round(overall, 3)
        
        # Round individual scores
        for key in scores:
            if key != "overall":
                scores[key] = round(scores[key], 3)
        
        return scores
    
    def _calculate_context_efficiency(self, text: str) -> float:
        """
        Metric 1: Context Efficiency
        Optimal token count for KV-cache efficiency
        Target: 300-800 tokens (approximated by words * 1.3)
        """
        words = len(text.split())
        approx_tokens = words * 1.3
        
        # Optimal range: 300-800 tokens
        if 300 <= approx_tokens <= 800:
            return 1.0
        elif approx_tokens < 300:
            # Too short
            return approx_tokens / 300
        else:
            # Too long (penalty increases)
            excess = approx_tokens - 800
            penalty = min(excess / 800, 0.5)  # Max 50% penalty
            return max(0.5, 1.0 - penalty)
    
    def _calculate_reasoning_depth(self, layer_responses: Dict[str, str]) -> float:
        """
        Metric 2: Reasoning Depth
        Number of explicit reasoning steps (5 layers minimum)
        """
        # Count non-empty layers
        filled_layers = sum(1 for v in layer_responses.values() if v and len(v.strip()) > 20)
        
        # Target: 5 layers
        return min(filled_layers / 5.0, 1.0)
    
    def _calculate_cultural_specificity(self, text: str) -> float:
        """
        Metric 3: Cultural Specificity
        Unique cultural markers vs generic content
        Target: >70% culturally-specific content
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        if not words:
            return 0.0
        
        # Count cultural markers
        cultural_count = sum(1 for marker in self.cultural_markers if marker in text_lower)
        
        # Count proper nouns (capitalized words, often cultural references)
        proper_nouns = sum(1 for word in text.split() if word and word[0].isupper())
        
        # Count unique words (diversity indicator)
        unique_ratio = len(set(words)) / len(words)
        
        # Combine signals
        cultural_density = cultural_count / max(len(words) / 50, 1)  # Per 50 words
        proper_noun_ratio = proper_nouns / len(words)
        
        score = (cultural_density * 0.4 + proper_noun_ratio * 0.3 + unique_ratio * 0.3)
        
        return min(score, 1.0)
    
    def _calculate_emotional_richness(self, text: str) -> float:
        """
        Metric 4: Emotional Richness
        Emotional descriptors per 100 words
        Target: >15 emotional markers per 100 words
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        if not words:
            return 0.0
        
        # Count emotional words
        emotional_count = sum(1 for word in self.emotional_words if word in text_lower)
        
        # Count sensory words (body, senses)
        sensory_patterns = [
            r'\b(see|saw|sight|look|watch|gaze)\b',
            r'\b(hear|sound|listen|noise|voice)\b',
            r'\b(smell|scent|aroma|fragrance)\b',
            r'\b(taste|flavor|bitter|sweet)\b',
            r'\b(touch|feel|texture|soft|rough)\b',
            r'\b(body|chest|heart|hand|eye|skin)\b'
        ]
        
        sensory_count = sum(len(re.findall(pattern, text_lower)) for pattern in sensory_patterns)
        
        # Calculate per 100 words
        total_markers = emotional_count + sensory_count
        markers_per_100 = (total_markers / len(words)) * 100
        
        # Target: 15 markers per 100 words
        score = min(markers_per_100 / 15, 1.0)
        
        return score
    
    def _calculate_attention_density(self, layer_responses: Dict[str, str]) -> float:
        """
        Metric 5: Attention Density
        Specific, verifiable details per layer
        Target: 3+ concrete details per layer
        """
        # Patterns that indicate specific details
        detail_patterns = [
            r'\b(exactly|precisely|specifically)\b',
            r'\b\d+\b',  # Numbers
            r'\b(the|this|that)\s+\w+',  # Specific references
            r'\b(color|shape|size|texture|pattern)\b',
            r'\b(north|south|east|west|left|right|top|bottom)\b',  # Spatial
            r'\b(morning|afternoon|evening|night|dawn|dusk)\b',  # Temporal
        ]
        
        total_details = 0
        filled_layers = 0
        
        for response in layer_responses.values():
            if response and len(response.strip()) > 20:
                filled_layers += 1
                layer_details = sum(len(re.findall(pattern, response.lower())) 
                                   for pattern in detail_patterns)
                total_details += layer_details
        
        if filled_layers == 0:
            return 0.0
        
        # Average details per layer
        avg_details_per_layer = total_details / filled_layers
        
        # Target: 3 details per layer
        score = min(avg_details_per_layer / 3, 1.0)
        
        return score
    
    def _calculate_compression_quality(self, 
                                      full_text: str,
                                      distilled_essence: List[str]) -> float:
        """
        Metric 6: Compression Quality
        Information preserved in 3-word distillation
        Target: >80% essence capture
        """
        if not distilled_essence or len(distilled_essence) < 3:
            return 0.0
        
        # Extract key concepts from full text
        words = full_text.lower().split()
        word_freq = Counter(words)
        
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these',
                     'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
                     'his', 'her', 'its', 'our', 'their'}
        
        key_words = {word: freq for word, freq in word_freq.items() 
                    if word not in stop_words and len(word) > 3}
        
        # Get top concepts
        top_concepts = sorted(key_words.items(), key=lambda x: x[1], reverse=True)[:10]
        top_concept_words = {word for word, _ in top_concepts}
        
        # Check how many essence words relate to key concepts
        essence_lower = [word.lower() for word in distilled_essence]
        
        # Direct matches
        direct_matches = sum(1 for word in essence_lower if word in top_concept_words)
        
        # Semantic proximity (simple check: shared letters)
        proximity_score = 0
        for essence_word in essence_lower:
            for concept_word in top_concept_words:
                # Calculate overlap
                overlap = len(set(essence_word) & set(concept_word))
                proximity_score += overlap / max(len(essence_word), len(concept_word))
        
        # Combine scores
        direct_score = direct_matches / 3  # 3 essence words
        proximity_score = min(proximity_score / 3, 1.0)
        
        final_score = (direct_score * 0.6 + proximity_score * 0.4)
        
        return min(final_score, 1.0)
    
    def get_quality_grade(self, overall_score: float) -> str:
        """
        Convert overall score to quality grade
        """
        if overall_score >= 0.90:
            return "A+ (Exceptional)"
        elif overall_score >= 0.80:
            return "A (Excellent)"
        elif overall_score >= 0.70:
            return "B (Good)"
        elif overall_score >= 0.60:
            return "C (Fair)"
        else:
            return "D (Needs Improvement)"
    
    def get_recommendations(self, scores: Dict[str, float]) -> List[str]:
        """
        Generate recommendations based on scores
        """
        recommendations = []
        
        if scores["context_efficiency"] < 0.70:
            if scores.get("_approx_tokens", 0) < 300:
                recommendations.append("💡 Add more detail to reach optimal context length (300-800 tokens)")
            else:
                recommendations.append("💡 Consider condensing to improve context efficiency")
        
        if scores["reasoning_depth"] < 0.70:
            recommendations.append("💡 Fill out all 5 perception layers for deeper reasoning")
        
        if scores["cultural_specificity"] < 0.70:
            recommendations.append("💡 Add more cultural context and specific references")
        
        if scores["emotional_richness"] < 0.70:
            recommendations.append("💡 Include more sensory and emotional descriptions")
        
        if scores["attention_density"] < 0.70:
            recommendations.append("💡 Add specific, verifiable details to each layer")
        
        if scores["compression_quality"] < 0.70:
            recommendations.append("💡 Ensure 3-word essence captures the core meaning")
        
        if not recommendations:
            recommendations.append("🎉 Excellent quality! This wisdom is training-ready.")
        
        return recommendations


# Test the quality metrics calculator
def test_quality_metrics():
    """Test quality metrics calculation"""
    
    print("📊 Testing YSenseAI Quality Metrics Calculator")
    print("=" * 60)
    
    calculator = QualityMetricsCalculator()
    
    # Test data
    test_data = {
        "raw_story": "A grandmother teaches patience through cooking rendang, a traditional Malaysian dish that takes 8 hours.",
        "layer_responses": {
            "narrative": "The unspoken story is about generational knowledge transfer. Elders pass down not just recipes, but philosophy.",
            "somatic": "The body feels warmth from the fire, reverence in the chest, and nostalgia in the heart.",
            "attention": "The way the coconut paste darkens from cream to deep brown, like memories deepening with time.",
            "synesthetic": "The vibe is: Patient. Earthy. Sacred.",
            "temporal": "A low, steady hum - like time itself cooking, transforming raw into refined."
        },
        "distilled_essence": ["Patience", "Tradition", "Alchemy"]
    }
    
    # Calculate metrics
    print("\n🔢 Calculating quality metrics...")
    scores = calculator.calculate_all_metrics(**test_data)
    
    print("\n📈 Quality Scores:")
    for metric, score in scores.items():
        if metric != "overall":
            print(f"  {metric.replace('_', ' ').title()}: {score:.3f}")
    
    print(f"\n🎯 Overall Score: {scores['overall']:.3f}")
    print(f"🏆 Grade: {calculator.get_quality_grade(scores['overall'])}")
    
    # Get recommendations
    print("\n💡 Recommendations:")
    recommendations = calculator.get_recommendations(scores)
    for rec in recommendations:
        print(f"  {rec}")
    
    print("\n🎉 Quality Metrics Test Complete!")


if __name__ == "__main__":
    test_quality_metrics()
