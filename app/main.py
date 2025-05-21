import gradio as gr
import torch
from modules.pipeline import PerformanceReviewAnalyzer
from modules.vizualisations import visualize_feedback_types, display_analysis_summary, visualize_objective_alignment

# Create analyzer instance
analyzer = PerformanceReviewAnalyzer()

def analyze_review(objectives, review_text):
    if not review_text:
        return "Please enter some review text to analyze."

    # Run analysis
    results = analyzer.analyze(review_text, objectives)

    # Generate visualizations
    visualize_feedback_types(results)
    if results["analysis"].get("objective_alignment"):
        visualize_objective_alignment(results)

    # Display text summary
    display_analysis_summary(results)

    # Format results for Gradio markdown output
    output = "## Analysis Results\n\n"

    output += "### Detected Issues\n\n"

    # Bias issues
    output += "#### Potential Bias\n"
    if "lexicon_based" in results["analysis"]["bias_issues"]:
        bias_issues = results["analysis"]["bias_issues"]["lexicon_based"]
        if bias_issues:
            for issue in bias_issues:
                output += f"- **{issue['bias_type'].title()} bias:** \"{issue['sentence']}\"\n"
                output += f"  - Concerning terms: {', '.join(issue['markers'])}\n"
        else:
            output += "- No significant bias detected\n"

    # Specificity issues
    output += "\n#### Vague Language\n"
    specificity_issues = results["analysis"]["specificity_issues"]["sentence_issues"]
    if specificity_issues:
        for issue in specificity_issues:
            output += f"- \"{issue['sentence']}\"\n"
    else:
        output += "- No vague language detected\n"

    # Objective alignment
    if results["analysis"].get("objective_alignment"):
        output += "\n#### Objective Alignment\n"
        for obj in results["analysis"]["objective_alignment"]:
            status = "✓ Mentioned" if obj["mentioned"] else "✗ Not addressed"
            output += f"- {obj['objective']}: {status}\n"

    # Recommendations
    output += "\n### Recommendations\n\n"
    if results["recommendations"]:
        for i, rec in enumerate(results["recommendations"], 1):
            output += f"**Recommendation {i}:**\n"
            output += f"- **Original:** \"{rec['original']}\"\n"
            output += f"- **Suggestion:** {rec['suggestion']}\n\n"
    else:
        output += "- No specific recommendations\n"

    return output

# Check if GPU is available
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    device = torch.device("cpu")
    print("Using CPU")

# Create Gradio interface
demo = gr.Interface(
    fn=analyze_review,
    inputs=[
        gr.Textbox(lines=5, label="Performance Objectives (one per line)", placeholder="Enter objectives..."),
        gr.Textbox(lines=10, label="Performance Review Text", placeholder="Enter your review text...")
    ],
    outputs=gr.Markdown(),
    title="Performance Review Analysis System",
    description="Analyze performance reviews for bias, specificity, and alignment with objectives.",
    examples=[
        ["Increase sales by 10% in Q3\nComplete project X by November 15th",
         "John has done a good job this year. He completed the database migration project and worked on the new API. He needs to improve his communication and be more proactive."],
        ["Improve team collaboration\nDeliver quarterly reports on time",
         "Sarah is an aggressive manager who pushes her team hard. She has good ideas but sometimes she is too emotional in meetings. Her team has delivered good results."]
    ]
)

# Launch the interface
print("launching gradio app")
demo.launch(server_name="0.0.0.0",debug=True, server_port=7860)
print("App Launched, check http://localhost:7860")