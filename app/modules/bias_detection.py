import numpy as np
class BiasDetector:   
    def __init__(self, zero_shot_analyzer):
        self.analyzer = zero_shot_analyzer

    def detect_bias(self, processed_text):
        results = []

        for sentence in processed_text["sentences"]:
            # Look into each of the sentence and check if its biased
            res = self.analyzer.detect_bias(sentence)
            loc = np.argmax(res["scores"])

            results.append({
                "sentence": sentence, # Return the original sentence
                "label": res["labels"][loc], # The clasification
                "intensity": "high" if res["scores"][loc]> 0.8 else "low" if res["scores"][loc] < 0.3 else "medium", # The intensity of the bias
                "prediction": res['scores'][loc] # The score of the classification or prediciton
            })

        return results