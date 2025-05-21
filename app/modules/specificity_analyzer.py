import re

class SpecificityAnalyzer:
    def __init__(self, zero_shot_analyzer):
        self.analyzer = zero_shot_analyzer
        # Patterns for vague language
        self.vague_patterns = [
            r"good job",
            r"needs improvement",
            r"work harder",
            r"be more proactive",
            r"communication skills",
            r"team player",
            r"meets expectations"
        ]

    def analyze_specificity(self, processed_text):
        results = []

        # Zero-shot analysis
        zs_results = self.analyzer.analyze_specificity(processed_text["raw_text"])

        # Pattern-based detection
        for i, sentence in enumerate(processed_text["sentences"]):
            for pattern in self.vague_patterns:
                if re.search(pattern, sentence, re.IGNORECASE):
                    results.append({
                        "sentence_id": i,
                        "sentence": sentence,
                        "issue": "vague language",
                        "pattern": pattern
                    })

        # Check for measurable outcomes
        has_metrics = any(re.search(r'\d+%|\d+ percent|increased by', s)
                         for s in processed_text["sentences"])

        return {
            "sentence_issues": results,
            "has_measurable_outcomes": has_metrics,
            "zero_shot_results": zs_results
        }