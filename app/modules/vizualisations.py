import matplotlib.pyplot as plt
import seaborn as sns

def visualize_feedback_types(results):
    """Visualize feedback type distribution"""
    feedback_types = results["analysis"]["feedback_type"]["labels"]
    scores = results["analysis"]["feedback_type"]["scores"]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(feedback_types, scores, color=sns.color_palette("viridis", len(feedback_types)))

    # Add a horizontal line at 0.5 for reference
    plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.3)

    plt.title('Feedback Type Distribution', fontsize=15)
    plt.ylabel('Confidence Score', fontsize=12)
    plt.ylim(0, 1)
    plt.xticks(rotation=30, ha='right')

    # Add value labels on top of bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                f'{height:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

def visualize_objective_alignment(results):
    """Visualize alignment with objectives"""
    if not results["analysis"].get("objective_alignment"):
        print("No objectives provided for alignment visualization.")
        return

    objectives = [item["objective"] if len(item["objective"]) < 30
                 else item["objective"][:27] + "..."
                 for item in results["analysis"]["objective_alignment"]]

    overlap_scores = [item["overlap_score"] for item in results["analysis"]["objective_alignment"]]
    mentioned = [item["mentioned"] for item in results["analysis"]["objective_alignment"]]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(objectives, overlap_scores, color=[
        'green' if m else 'red' for m in mentioned
    ])

    plt.title('Objective Alignment', fontsize=15)
    plt.xlabel('Overlap Score', fontsize=12)
    plt.xlim(0, 1)

    # Add value labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.02, bar.get_y() + bar.get_height()/2.,
                f'{width:.2f}', va='center')

    plt.tight_layout()
    plt.show()

def display_analysis_summary(results):
    """Display a text summary of the analysis"""
    print("=" * 60)
    print("PERFORMANCE REVIEW ANALYSIS SUMMARY")
    print("=" * 60)

    # Feedback type
    print("\nPREDOMINANT FEEDBACK TYPE:")
    feedback = results["analysis"]["feedback_type"]
    top_feedback = feedback["labels"][0]
    top_score = feedback["scores"][0]
    print(f"- {top_feedback.title()} ({top_score:.2f} confidence)")

    # Bias issues
    print("\nPOTENTIAL BIAS DETECTED:")
    if "lexicon_based" in results["analysis"]["bias_issues"]:
        bias_issues = results["analysis"]["bias_issues"]["lexicon_based"]
        if bias_issues:
            for issue in bias_issues:
                print(f"- {issue['bias_type'].title()} bias: \"{issue['sentence']}\"")
                print(f"  Concerning terms: {', '.join(issue['markers'])}")
        else:
            print("- No significant bias detected")

    # Specificity issues
    print("\nVAGUE LANGUAGE:")
    specificity_issues = results["analysis"]["specificity_issues"]["sentence_issues"]
    if specificity_issues:
        for issue in specificity_issues:
            print(f"- \"{issue['sentence']}\"")
    else:
        print("- No vague language detected")

    # Objective alignment
    if results["analysis"].get("objective_alignment"):
        print("\nOBJECTIVE ALIGNMENT:")
        for obj in results["analysis"]["objective_alignment"]:
            status = "✓ Mentioned" if obj["mentioned"] else "✗ Not addressed"
            print(f"- {obj['objective']}: {status}")

    # Recommendations
    print("\nKEY RECOMMENDATIONS:")
    if results["recommendations"]:
        for i, rec in enumerate(results["recommendations"], 1):
            print(f"{i}. Original: \"{rec['original']}\"")
            print(f"   Suggestion: {rec['suggestion']}")
    else:
        print("- No specific recommendations")

    print("\n" + "=" * 60)