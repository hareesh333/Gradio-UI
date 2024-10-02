import gradio as gr

def save_settings(file_loader, llm_vendor, doc_chunks, retrieval_mode, prioritize_table, use_mmr, use_reranking, use_llm_scoring):
    return f"Settings saved! Details: File Loader: {file_loader}, LLM Vendor: {llm_vendor}, Doc Chunks: {doc_chunks}, Retrieval Mode: {retrieval_mode}, Table: {prioritize_table}, MMR: {use_mmr}, Re-ranking: {use_reranking}, LLM Scoring: {use_llm_scoring}"

def create_app():
    with gr.Blocks() as app:
        with gr.Tabs():
            with gr.TabItem("Retrieval Settings"):
                with gr.TabItem("File Collection"):
                    with gr.Column():
                        file_loader = gr.Dropdown(label="File loader", choices=["Azure AI Document Intelligence (figure+table extraction)", "Adobe API (figure+table extraction)","Default (open-source)"])
                        llm_vendor = gr.Dropdown(label="LLM for relevant scoring", choices=["openai (default)","openai", "azure","ollama"])
                        doc_chunks = gr.Number(label="Number of document chunks to retrieve", value=10, step=1)
                        retrieval_mode = gr.Dropdown(label="Retrieval mode", choices=["hybrid", "text","vector"])
                        prioritize_table = gr.Checkbox(label="Prioritize table", value=False)
                        use_mmr = gr.Checkbox(label="Use MMR", value=False)
                        use_reranking = gr.Checkbox(label="Use reranking", value=True)
                        use_llm_scoring = gr.Checkbox(label="Use LLM relevant scoring", value=True)

                with gr.TabItem("GraphRAG Collection"):
                    with gr.Column():
                        graphrag_loader = gr.Dropdown(label="File loader", choices=["Default (open-source)", "Adobe API (figure+table extraction)","Azure AI Document Intelligence (figure+table extraction)"])
                        search_type = gr.Dropdown(label="Search type", choices=["local", "global"])

            with gr.TabItem("Reasoning Settings"):
                with gr.Column():
                    language = gr.Dropdown(label="Language", choices=["English", "Spanish", "French"])
                    max_context_length = gr.Number(label="Max context length (LLM)", value=32000, step=1000)
                    reasoning_options = gr.Radio(label="Reasoning options", choices=["simple", "complex", "ReAct", "ReWOO"], value="simple")
                    language_model = gr.Dropdown(label="Language model", choices=["openai (default)", "azure","openai","ollama"])
                    highlight_citation = gr.Checkbox(label="Highlight Citation", value=True)
                    system_prompt = gr.Textbox(label="System Prompt", value="This is a question answering system", lines=2)
                    qa_prompt = gr.Textbox(label="QA Prompt (contains {context}, {question}, {lang})", value="Enter your query", lines=3)
                    num_interactions = gr.Number(label="Number of interactions to include", value=5, step=1)
                    max_message_length = gr.Number(label="Maximum message length for context rewriting", value=150, step=1)

            save_button = gr.Button("Save Changes")
            save_button.click(
                save_settings,
                inputs=[file_loader, llm_vendor, doc_chunks, retrieval_mode, prioritize_table, use_mmr, use_reranking, use_llm_scoring, graphrag_loader, search_type, language, max_context_length, reasoning_options, language_model, highlight_citation, system_prompt, qa_prompt, num_interactions, max_message_length],
                outputs=gr.Markdown()
            )

    return app

if __name__ == "__main__":
    app = create_app()
    app.launch(share=True)
