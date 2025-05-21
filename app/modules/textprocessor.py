from transformers import AutoTokenizer
import spacy
import re

class TextProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_md")
        self.tokenizer = AutoTokenizer.from_pretrained("roberta-large-mnli")

    def preprocess(self, text):
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()

        # Process with spaCy
        doc = self.nlp(text)

        # Split into sentences
        sentences = [sent.text.strip() for sent in doc.sents]

        # Tokenize for transformer
        tokens = self.tokenizer(text, return_tensors="pt",
                               padding=True, truncation=True)

        return {
            "raw_text": text,
            "sentences": sentences,
            "tokens": tokens,
            "doc": doc
        }