import gradio as gr
import asyncio
import pandas as pd
import plotly.express as px
from sklearn.decomposition import PCA
import numpy as np
import os

from trie_engine import SkillTrie, DEFAULT_SKILLS
from vector_service import VectorService
from pdf_parser import extract_text_from_pdf
from resume_processor import evaluate_resume, TopKCandidatesHeap

# Initialize Services
trie = SkillTrie(DEFAULT_SKILLS)
vector_service = VectorService()

async def process_resumes_async(job_description, resume_files, top_k):
    if not job_description or not resume_files:
        return pd.DataFrame(), None, "Please provide a job description and at least one resume."
        
    vector_service.reset()
    heap = TopKCandidatesHeap(k=int(top_k))
    
    tasks = []
    parsed_docs = []
    
    # 1. Parse PDFs and extract skills synchronously
    for file in resume_files:
        candidate_name = os.path.basename(file.name).replace(".pdf", "")
        text = extract_text_from_pdf(file.name)
        if not text:
            continue
            
        skills = list(trie.extract_skills(text))
        
        doc_data = {
            "candidate_name": candidate_name,
            "text": text,
            "skills": skills
        }
        parsed_docs.append(doc_data)
        
    if not parsed_docs:
        return pd.DataFrame(), None, "No valid text could be extracted from the uploaded PDFs."
        
    # 2. Add to Vector Service
    vector_service.add_documents(parsed_docs)
    
    # 3. Create Async Tasks for LLM Evaluation
    for doc in parsed_docs:
        task = evaluate_resume(
            job_description=job_description,
            resume_text=doc["text"],
            candidate_name=doc["candidate_name"],
            extracted_skills=doc["skills"]
        )
        tasks.append(task)
        
    # Run evaluations concurrently
    eval_results = await asyncio.gather(*tasks)
    
    # 4. Add to Heap
    for result in eval_results:
        heap.add_candidate(result)
        
    top_candidates = heap.get_top_candidates()
    
    # 5. Format Leaderboard
    df = pd.DataFrame(top_candidates)
    cols = ["Candidate_Name", "Technical_Score", "Skills_Found", "Soft_Skills_Analysis", "Red_Flags"]
    df = df[[c for c in cols if c in df.columns]]
    
    # 6. Generate PCA Plot
    embeddings, docs = vector_service.get_all_embeddings()
    fig = None
    if len(embeddings) >= 2:
        query_emb = vector_service.model.encode([job_description], convert_to_numpy=True)
        all_embs = np.vstack([embeddings, query_emb])
        
        # PCA to 2 dimensions
        n_comp = min(2, len(all_embs))
        if n_comp == 2:
            pca = PCA(n_components=2)
            components = pca.fit_transform(all_embs)
            
            names = [doc.get("candidate_name", f"Doc {i}") for i, doc in enumerate(docs)] + ["Job Description"]
            types = ["Candidate"] * len(docs) + ["Job Profile"]
            
            plot_df = pd.DataFrame({
                "PCA_1": components[:, 0],
                "PCA_2": components[:, 1],
                "Name": names,
                "Type": types
            })
            
            fig = px.scatter(plot_df, x="PCA_1", y="PCA_2", color="Type", hover_data=["Name"], 
                             title="Candidate Semantic Cluster Map (PCA)",
                             color_discrete_map={"Candidate": "#00d2ff", "Job Profile": "#ff0055"},
                             symbol="Type")
            fig.update_traces(marker=dict(size=14, line=dict(width=1, color='DarkSlateGrey')))
            fig.update_layout(
                template="plotly_dark", 
                plot_bgcolor="rgba(0,0,0,0)", 
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
                legend=dict(title=None)
            )

    return df, fig, f"Successfully processed {len(parsed_docs)} resumes."

def process_wrapper(job_description, resume_files, top_k):
    return asyncio.run(process_resumes_async(job_description, resume_files, top_k))

# --- Gradio UI Setup ---
# Creating a custom, futuristic, professional theme
custom_css = """
.gradio-container {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364) !important;
}
h1 {
    text-shadow: 0 0 10px rgba(0, 210, 255, 0.8);
}
"""

theme = gr.themes.Soft(
    primary_hue="cyan",
    secondary_hue="blue",
).set(
    body_text_color="white",
    block_background_fill="rgba(20, 30, 40, 0.6)",
    block_border_width="1px",
    block_border_color="rgba(0, 210, 255, 0.3)",
    input_background_fill="rgba(0, 0, 0, 0.3)",
    button_primary_background_fill="linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%)",
    button_primary_text_color="white",
)

with gr.Blocks(theme=theme, css=custom_css, title="NexusScreen") as demo:
    gr.Markdown(
        """
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #00d2ff; font-weight: 800; font-size: 3em; letter-spacing: 2px; margin-bottom: 5px;">🚀 NexusScreen</h1>
            <h3 style="color: #a0c4ff; font-weight: 300;">High-Performance AI Resume Intelligence System</h3>
            <p style="color: #8899a6; font-size: 0.9em;">
                Powered by <b>FAISS Vectors</b> for semantic search, <b>Trie DSA</b> for $O(L)$ keyword extraction, and <b>LLM Intelligence</b>.
            </p>
        </div>
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Input Configuration")
            job_desc_input = gr.Textbox(
                label="Job Description", 
                lines=8, 
                placeholder="Paste the target job description here..."
            )
            top_k_slider = gr.Slider(minimum=1, maximum=50, value=5, step=1, label="Top K Candidates (Heap Size)")
            file_input = gr.File(label="Upload Resumes (.pdf)", file_types=[".pdf"], file_count="multiple")
            submit_btn = gr.Button("Analyze Candidates ✨", variant="primary", size="lg")
            status_text = gr.Textbox(label="System Status", interactive=False)
            
        with gr.Column(scale=2):
            gr.Markdown("### 🏆 Intelligence Output")
            with gr.Tabs():
                with gr.TabItem("📊 Cluster Map"):
                    pca_plot_output = gr.Plot(label="Semantic Landscape")
                with gr.TabItem("📋 Top K Leaderboard"):
                    leaderboard_output = gr.Dataframe(label="Ranked Candidates", interactive=False, wrap=True)

    submit_btn.click(
        fn=process_wrapper,
        inputs=[job_desc_input, file_input, top_k_slider],
        outputs=[leaderboard_output, pca_plot_output, status_text]
    )

if __name__ == "__main__":
    demo.launch(inbrowser=True)
