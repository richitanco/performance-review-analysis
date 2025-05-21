class BiasDetector:   
    def __init__(self, zero_shot_analyzer):
        self.analyzer = zero_shot_analyzer
        # Create basic lexicons in-memory instead of loading from files
        self.gender_terms = self._create_gender_lexicon()
        self.cultural_terms = self._create_cultural_lexicon()

    def _create_gender_lexicon(self):
        # Simple in-memory gender lexicon
        return {
            "masculine_coded": ["aggressive", "ambitious", "analytical", "assertive", "confident", "dominant", "forceful", "independent", "logical"],
            "feminine_coded": ["collaborative", "compassionate", "emotional", "empathetic", "nurturing", "sensitive", "supportive", "warm"],
            "gendered_terms": ["he", "she", "him", "her", "his", "hers", "himself", "herself"]
        }

    def _create_cultural_lexicon(self):
        # Simple in-memory cultural bias lexicon
        return {
            "cultural_stereotypes": ["articulate", "well-spoken", "exotic", "diverse fit", "cultural fit"]
        }

    def _check_lexicon(self, sentence, lexicon_dict):
        sentence = sentence.lower()
        found_terms = []

        # Check each category in the lexicon
        for category, terms in lexicon_dict.items():
            for term in terms:
                if f" {term} " in f" {sentence} " or sentence.startswith(f"{term} ") or sentence.endswith(f" {term}"):
                    found_terms.append(term)

        return found_terms

    def _combine_results(self, zs_results, lexicon_results):
        # Combine zero-shot and lexicon-based results
        # For this simplified version, we'll just return both
        return {
            "zero_shot": zs_results,
            "lexicon_based": lexicon_results
        }

    def detect_bias(self, processed_text):
        results = []

        # Zero-shot classification
        zs_results = self.analyzer.detect_bias(processed_text["raw_text"])

        # Lexicon-based detection
        for sentence in processed_text["sentences"]:
            # Check gender bias markers
            gender_markers = self._check_lexicon(sentence, self.gender_terms)
            if gender_markers:
                results.append({
                    "sentence": sentence,
                    "bias_type": "gender",
                    "markers": gender_markers,
                    "confidence": 0.8 if len(gender_markers) > 1 else 0.6
                })

            # Check cultural bias markers
            cultural_markers = self._check_lexicon(sentence, self.cultural_terms)
            if cultural_markers:
                results.append({
                    "sentence": sentence,
                    "bias_type": "cultural",
                    "markers": cultural_markers,
                    "confidence": 0.8 if len(cultural_markers) > 1 else 0.6
                })

        # Combine results from zero-shot and lexicon approaches
        combined_results = self._combine_results(zs_results, results)
        return combined_results