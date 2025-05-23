import numpy as np

class SpecificityAnalyzer:
    def __init__(self, zero_shot_analyzer):
        self.analyzer = zero_shot_analyzer

    def analyze_specificity(self, processed_text):
        results = []

        # Pattern-based detection
        for sentence in processed_text["sentences"]:
            # Check gender bias markers
            res = self.analyzer.analyze_specificity(sentence)
            loc = np.argmax(res["scores"])

            results.append({
                "sentence": sentence,
                "label": res["labels"][loc],
                "intensity": "high" if res["scores"][loc]> 0.8 else "low" if res["scores"][loc] < 0.3 else "medium",
                "prediction": res['scores'][loc]
            })

        return results