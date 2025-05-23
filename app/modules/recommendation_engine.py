import random


class RecommendationEngine:
    def __init__(self,results:dict):
        self.biases = results.get('biases')
        self.specificities = results.get('specificities')
        self.feedbacks = results.get('feedbacks')
        self.objectives = results.get('objectives')

    def generate_table_bias(self) -> dict:
        if self.biases is None:
            return None
        
        row = []
        for bias in self.biases:
            if bias["intensity"] == "high":
                row.append({
                    "sentence": bias["sentence"],
                    "label": bias["label"].capitalize(),
                    "intensity": bias["intensity"].capitalize(),
                    "score": bias["prediction"],
                    "recommendation": "This sentence is highly likely to contain bias. Please rephrase the sentence."
                })
            elif bias["intensity"] == "medium":
                row.append({
                    "sentence": bias["sentence"],
                    "label": bias["label"].capitalize(),
                    "intensity": bias["intensity"].capitalize(),
                    "score": bias["prediction"],
                    "recommendation": "This sentence may contain some bias. Please consider rephrasing it."
                })
            else:
                row.append({
                    "sentence": bias["sentence"],
                    "label": bias["label"].capitalize(),
                    "intensity": bias["intensity"].capitalize(),
                    "score": bias["prediction"],
                    "recommendation": "This sentence does not contain significant bias."
                })
            
        return row

    def generate_table_specificity(self) -> dict:
        if self.specificities is None:
            return None
        row = []

        for specificity in self.specificities:
            if specificity["intensity"] == "high":
                row.append({
                    "sentence": specificity["sentence"],
                    "label": specificity["label"].capitalize(),
                    "intensity": specificity["intensity"].capitalize(),
                    "score": specificity["prediction"],
                    "recommendation": "This sentence is highly vague. Please provide more specific details."
                })
            elif specificity["intensity"] == "medium":
                row.append({
                    "sentence": specificity["sentence"],
                    "label": specificity["label"].capitalize(),
                    "intensity": specificity["intensity"].capitalize(),
                    "score": specificity["prediction"],
                    "recommendation": "This sentence may be somewhat vague. Consider adding more details."
                })
            else:
                row.append({
                    "sentence": specificity["sentence"],
                    "label": specificity["label"].capitalize(),
                    "intensity": specificity["intensity"].capitalize(),
                    "score": specificity["prediction"],
                    "recommendation": "This sentence is clear and specific."
                })
        
        return row
    def generate_table_feedback(self) -> dict:
        if self.feedbacks is None:
            return None

        row = []
        for feedback in self.feedbacks:
            if feedback["label"] == "positive feedback":
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": feedback["prediction"],
                    "recommendation": "This is a positive feedback. No action needed."
                })
            elif feedback["label"] == "constructive criticism":
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": feedback["prediction"],
                    "recommendation": "This is a constructive criticism. Consider rephrasing the sentence."
                })
            elif feedback["label"] == "actionable feedback":
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": feedback["prediction"],
                    "recommendation": "This is an actionable feedback. Please consider implementing the suggestions."
                })
            else:
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": feedback["prediction"],
                    "recommendation": "The feedback is vague. Please provide more specific details, like what to improve."
                })

        return row