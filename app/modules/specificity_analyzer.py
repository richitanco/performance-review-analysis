import numpy as np
import re

class SpecificityAnalyzer:
    def __init__(self, zero_shot_analyzer):
        self.analyzer = zero_shot_analyzer

    def is_specific(self, sentence):
        score = 0
        # Check for clues that indicate specificity (numbers, dates, project names)
        if re.search(r'\d+%|\d+ percent|\d+\b', sentence): score += 2
        if re.search(r'on \w+ \d{1,2}(st|nd|rd|th)|during Q[1-4]|in \w+ 20\d{2}', sentence): score += 2
        if re.search(r'project [A-Z][a-z]+', sentence, re.IGNORECASE): score += 1
        # Look for "for example" and see if it is followed by specific info
        if "for example" in sentence.lower():
            example_text = sentence.lower().split("for example")[-1]
            if re.search(r'\d+|project|successfully|delivered|implemented', example_text):
                score += 1
            else:
                score -= 1
        # Penalize for vague patterns/phrases
        vague_phrases = [
            "good job", "great work", "excellent performance", "well done",
            "needs improvement", "work harder", "communication skills",
            "meets expectations", "in the future", "attention to detail"
        ]
        for vp in vague_phrases:
            if vp in sentence.lower():
                score -= 2
        # Return label based on score
        return {'labels':"Specific" if score >= 1 else "Vague",'scores': float(score)}

    def analyze_specificity(self, processed_text):
        results = []

        # Pattern-based detection
        for sentence in processed_text["sentences"]:
            # Check gender bias markers
            # res = self.analyzer.analyze_specificity(sentence)
            # loc = np.argmax(res["scores"])
            
            res = self.is_specific(sentence)

            results.append({
                "sentence": sentence,
                "label": res["labels"],
                "intensity": None,
                "prediction": res['scores']
            })

        return results