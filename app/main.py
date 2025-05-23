import gradio as gr
import torch
from modules.pipeline import PerformanceReviewAnalyzer
from modules.vizualisations import visualize_feedback_types, display_analysis_summary, visualize_objective_alignment
import pandas as pd

# Create analyzer instance
analyzer = PerformanceReviewAnalyzer()

def analyze_review(review_text):
    if not review_text:
        return "Please enter some review text to analyze."

    outputs = []
    # Run analysis
    
    results = analyzer.analyze(review_text, objectives=None)
    outputs = [pd.DataFrame(data) if data is not None else pd.DataFrame({"sentence": [], "label": [], "intensity": [], "prediction": [], "recommendation":[]}) for data in results["recommendations"].values()]

    return outputs

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
        gr.Textbox(lines=10, label="Performance Review Text", placeholder="Enter your review text...")
    ],
    outputs=[
        gr.DataFrame(label="Bias Analysis"),
        gr.DataFrame(label="Specificity Analysis"),
        gr.DataFrame(label="Feedback Type Analysis")
    ],
    title="Performance Review Analysis System",
    description="Analyze performance reviews for bias, specificity, and alignment with objectives.",
)

# Launch the interface
print("launching gradio app")
demo.launch(server_name="0.0.0.0",debug=True, share=True, server_port=7860)