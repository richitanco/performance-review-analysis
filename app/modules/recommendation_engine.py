import random


class RecommendationEngine:
    def __init__(self):
        # Load suggestion templates
        self.templates = {
            "vague_feedback": [
                "Consider replacing '{original}' with specific examples: '{suggestion}'",
                "Make this more actionable by adding metrics: '{suggestion}'"
            ],
            "bias": [
                "This phrase could show bias: '{original}'. Consider: '{suggestion}'",
                "For more inclusive language, try: '{suggestion}' instead of '{original}'"
            ]
        }

        # Load specific alternatives for common issues
        self.alternatives = {
            "good job": [
                "completed {project} ahead of schedule, resulting in {outcome}",
                "exceeded the target of {metric} by {amount}"
            ],
            "needs improvement": [
                "could increase {metric} by focusing on {specific_area}",
                "would benefit from developing skills in {skill_area}"
            ],
            "work harder": [
                "could dedicate more time to {specific_task}",
                "might prioritize {important_aspect} to improve outcomes"
            ],
            "be more proactive": [
                "could anticipate {specific_need} before being asked",
                "might identify opportunities to improve {process} independently"
            ],
            "aggressive": [
                "presents ideas with conviction",
                "advocates strongly for their position",
                "communicates directly and clearly"
            ],
            "emotional": [
                "shows passion for the work",
                "demonstrates strong engagement",
                "cares deeply about team outcomes"
            ]
        }

    def _generate_bias_alternative(self, bias_issue):
        # Generate alternative for biased language
        for marker in bias_issue["markers"]:
            if marker.lower() in self.alternatives:
                return random.choice(self.alternatives[marker.lower()])

        # Default fallback suggestion
        if bias_issue["bias_type"] == "gender":
            return "using more gender-neutral language"
        else:
            return "focusing on specific behaviors rather than personal attributes"

    def _generate_specificity_alternative(self, specificity_issue):
        # Generate alternative for vague language
        pattern = specificity_issue["pattern"].lower()

        if pattern in self.alternatives:
            suggestion_template = random.choice(self.alternatives[pattern])

            # For a real system, we would fill in the placeholders with relevant content
            # For this prototype, we'll use generic examples
            if "{project}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{project}", "the database migration")
            if "{outcome}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{outcome}", "a 15% performance improvement")
            if "{metric}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{metric}", "customer satisfaction")
            if "{amount}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{amount}", "10%")
            if "{specific_area}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{specific_area}", "email response time")
            if "{skill_area}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{skill_area}", "technical documentation")
            if "{specific_task}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{specific_task}", "planning stages")
            if "{important_aspect}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{important_aspect}", "quality assurance")
            if "{specific_need}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{specific_need}", "client requirements")
            if "{process}" in suggestion_template:
                suggestion_template = suggestion_template.replace("{process}", "team workflows")

            return suggestion_template

        # Default fallback
        return "providing specific examples with measurable outcomes"

    def generate_recommendations(self, analysis_results):
        recommendations = []

        # Process bias issues
        if "lexicon_based" in analysis_results.get("bias_issues", {}):
            for bias in analysis_results["bias_issues"]["lexicon_based"]:
                template = random.choice(self.templates["bias"])
                suggestion = self._generate_bias_alternative(bias)
                recommendations.append({
                    "type": "bias",
                    "original": bias["sentence"],
                    "suggestion": template.format(
                        original=bias["markers"][0] if bias["markers"] else "this phrase",
                        suggestion=suggestion
                    )
                })

        # Process specificity issues
        if "sentence_issues" in analysis_results.get("specificity_issues", {}):
            for issue in analysis_results["specificity_issues"]["sentence_issues"]:
                template = random.choice(self.templates["vague_feedback"])
                suggestion = self._generate_specificity_alternative(issue)
                recommendations.append({
                    "type": "specificity",
                    "original": issue["sentence"],
                    "suggestion": template.format(
                        original=issue["pattern"],
                        suggestion=suggestion
                    )
                })

        return recommendations