from transformers import pipeline
import torch


class ZeroShotAnalyzer:
    def __init__(self):
        # Use GPU if available
        self.classifier = pipeline("zero-shot-classification",
                                  model="facebook/bart-large-mnli",
                                  device=0 if torch.cuda.is_available() else -1)

    def classify_feedback_type(self, text):
        # Define feedback type labels
        labels = ["positive feedback", "constructive criticism",
                 "actionable feedback", "vague feedback"]
        # Run zero-shot classification
        result = self.classifier(text, labels, multi_label=True, hypothesis_template="This is an example of a {}.")
        return result

    def detect_bias(self, text):
        # Define bias category labels
        labels = ["culturally biased", "racial biased", "unbiased"]

        # Run zero-shot classification
        result = self.classifier(text, labels, multi_label=True, hypothesis_template="This statement, is {}.")
        return result

    def analyze_specificity(self, text):
        # Define specificity labels
        labels = ["goal oriented","not goal oriented"]

        # Run zero-shot classification
        result = self.classifier(text, labels, multi_label=True, hypothesis_template="This statment is {}.")
        return result