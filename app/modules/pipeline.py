from .textprocessor import TextProcessor
from .zero_shot_classification import ZeroShotAnalyzer
from .bias_detection import BiasDetector
from .specificity_analyzer import SpecificityAnalyzer
from .recommendation_engine import RecommendationEngine
import re

class PerformanceReviewAnalyzer:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.zero_shot = ZeroShotAnalyzer()
        self.bias_detector = BiasDetector(self.zero_shot)
        self.specificity_analyzer = SpecificityAnalyzer(self.zero_shot)
        self.recommender = RecommendationEngine()

    def _check_objective_alignment(self, processed_text, objectives):
        # Simple objective alignment check
        # For each objective, check if it's mentioned in the review
        alignment = []

        for objective in objectives:
            if not objective.strip():  # Skip empty objectives
                continue

            # Check if objective keywords appear in the text
            objective_words = set(word.lower() for word in re.findall(r'\w+', objective)
                                if len(word) > 3)  # Only consider words longer than 3 chars

            text_words = set(word.lower() for word in re.findall(r'\w+', processed_text["raw_text"])
                           if len(word) > 3)

            # Calculate overlap
            common_words = objective_words.intersection(text_words)

            alignment.append({
                "objective": objective,
                "mentioned": len(common_words) > 0,
                "overlap_score": len(common_words) / len(objective_words) if objective_words else 0
            })

        return alignment

    def analyze(self, review_text, objectives=None):
        if not review_text.strip():
            return {
                "error": "No review text provided"
            }

        # Process text
        processed = self.text_processor.preprocess(review_text)

        # Run analysis engines
        bias_results = self.bias_detector.detect_bias(processed)
        specificity_results = self.specificity_analyzer.analyze_specificity(processed)
        feedback_type = self.zero_shot.classify_feedback_type(review_text)

        # Check alignment with objectives if provided
        objective_alignment = None
        if objectives:
            objective_list = objectives.split('\n') if isinstance(objectives, str) else objectives
            objective_alignment = self._check_objective_alignment(processed, objective_list)

        # Combine all analysis results
        analysis_results = {
            "bias_issues": bias_results,
            "specificity_issues": specificity_results,
            "feedback_type": feedback_type,
            "objective_alignment": objective_alignment
        }

        # Generate recommendations
        recommendations = self.recommender.generate_recommendations(analysis_results)

        return {
            "analysis": analysis_results,
            "recommendations": recommendations
        }

