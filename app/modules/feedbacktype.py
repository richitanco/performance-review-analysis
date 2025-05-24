from .zero_shot_classification import ZeroShotAnalyzer

class FeedbackTypeAnalyzer:
    def __init__(self, zero_shot_analyzer):
        self.analyzer = zero_shot_analyzer

    def feedback_type(self, processed_text):
        results = []

        # Pattern-based detection
        for sentence in processed_text["sentences"]:
            # Analyze each sentence for feedback type
            res = self.analyzer.classify_feedback_type(sentence)
            loc = res["scores"].index(max(res["scores"]))

            results.append({
                "sentence": sentence,
                "label": res["labels"][loc],
                "intensity": "high" if res["scores"][loc] > 0.8 else "low" if res["scores"][loc] < 0.3 else "medium",
                "prediction": res['scores'][loc]
            })
        
        return results