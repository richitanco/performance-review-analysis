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
            # ["culturally biased", "racial biased", "unbiased"]
            if bias["label"] == "culturally biased" or bias["label"] == "racial biased":
                if bias["intensity"] == "high":
                    row.append({
                        "sentence": bias["sentence"],
                        "label": bias["label"].capitalize(),
                        "intensity": bias["intensity"].capitalize(),
                        "score": round(bias["prediction"],3),
                        "recommendation": "This sentence is highly likely to contain bias. Please rephrase the sentence."
                    })
                elif bias["intensity"] == "medium":
                    row.append({
                        "sentence": bias["sentence"],
                        "label": bias["label"].capitalize(),
                        "intensity": bias["intensity"].capitalize(),
                        "score": round(bias["prediction"],3),
                        "recommendation": "This sentence may contain some bias. Please consider rephrasing it."
                    })
                else:
                    row.append({
                        "sentence": bias["sentence"],
                        "label": bias["label"].capitalize(),
                        "intensity": bias["intensity"].capitalize(),
                        "score": round(bias["prediction"],3),
                        "recommendation": "This sentence does not contain significant bias."
                    })
            else:
                row.append({
                    "sentence": bias["sentence"],
                    "label": bias["label"].capitalize(),
                    "intensity": bias["intensity"].capitalize(),
                    "score": round(bias["prediction"],3),
                    "recommendation": "There is a chance that is considered to be unbiased."
                })
            
        return row
    
    def generate_table_specificity(self) -> dict:
        if self.specificities is None:
            return None
        row = []
        # ["of being specific about a goal and having metrics to measure it","of a not specific sentence and lacking metrics","of having metrics, but with no specific goal",
        #   "of being specific about a goal, but lacking metrics"]
        for specificity in self.specificities:
            if specificity["label"] == "Vague":
                row.append({
                    "sentence": specificity["sentence"],
                    "label": specificity["label"].capitalize(),
                    "intensity": None,
                    "score": round(specificity["prediction"],3),
                    "recommendation": "This sentence is likely vague. Please provide more specific details, following SMART goals methodology."
                })

            else:
                row.append({
                    "sentence": specificity["sentence"],
                    "label": specificity["label"].capitalize(),
                    "intensity": None,
                    "score": round(specificity["prediction"],3),
                    "recommendation": "This sentence is likely specific."
                })
        
        return row
    def generate_table_feedback(self) -> dict:
        if self.feedbacks is None:
            return None
            # ["positive feedback", "constructive criticism",
            #      "actionable feedback", "vague feedback"]
        row = []
        for feedback in self.feedbacks:
            if feedback["label"] == "positive feedback":
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": round(feedback["prediction"],3),
                    "recommendation": f"There is a chance that this is considered to be positive."
                })
            elif feedback["label"] == "constructive criticism":
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": round(feedback["prediction"],3),
                    "recommendation": "This is a constructive criticism. Be mindfull of your feedback."
                })
            elif feedback["label"] == "actionable feedback":
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": round(feedback["prediction"],3),
                    "recommendation": "This is an actionable feedback. Please consider implementing the suggestions."
                })
            else:
                row.append({
                    "sentence": feedback["sentence"],
                    "label": feedback["label"].capitalize(),
                    "intensity": feedback["intensity"].capitalize(),
                    "score": round(feedback["prediction"],3),
                    "recommendation": "The feedback is vague. Please provide more specific details, like what/how to improve with SMART goals methodology."
                })

        return row