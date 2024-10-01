import gradio as gr

def handle_add(name, vendor, specification, set_default):
    # Implement logic to handle the addition of a new embedding model
    return f"Added embedding model '{name}' with vendor '{vendor}'. Set as default: {set_default}"


def handle_add():
    # Placeholder for handling the addition of a new entry
    return "Add functionality not implemented."

def handle_view():
    # Placeholder for handling the view action
    return "View functionality not implemented."



def create_app():
    with gr.Blocks() as app:
        with gr.Tabs():
            with gr.TabItem("Index Collections"):
                gr.Markdown("### Index Collections")
                with gr.Row():
                    with gr.TabItem("View"):
                # Corrected data format for the DataFrame
                        data = [
                            [1, "File", "FileIndex"],  # Data as a list of lists
                            [2, "GraphRAG", "GraphRAGIndex"]
                        ]
                        headers = ["id", "name", "index type"]

                        # Defining the DataFrame with corrected format
                        df = gr.Dataframe(value=data, headers=headers, interactive=False, height=200)
                    with gr.TabItem("Add"):
                        with gr.Row():
                            with gr.Column():
                                llm_name = gr.Textbox(label="LLM name", placeholder="Must be unique")
                                llm_vendor = gr.Dropdown(label="LLM vendors", choices=["ChatOpenAI", "AzureChatOpenAI", "LlamaCppChat"])
                                specification = gr.TextArea(label="Specification", placeholder="Specification in YAML format")
                                set_default = gr.Checkbox(label="Set default")
                                add_button = gr.Button("Add LLM")

                            with gr.Column():
                                gr.Markdown("### Spec description")
                                gr.Markdown("Select an LLM to view the spec description.")
            with gr.TabItem("LLMs"):
                gr.Markdown("### Large Language Models (LLMs)")
                with gr.Row():
                    with gr.TabItem("View"):
                # Corrected data format for the DataFrame
                        data = [
                            ["azure", "AzureChatOpenAI", "false"],  # Data as a list of lists
                            ["openai", "ChatOpenAI", "true"],
                            ["ollama","ChatOpenAI","false"]
                        ]
                        headers = ["name", "vendor", "default"]

                        # Defining the DataFrame with corrected format
                        df = gr.Dataframe(value=data, headers=headers, interactive=False, height=200)
                    with gr.TabItem("Add"):
                        with gr.Row():
                            with gr.Column():
                                llm_name = gr.Textbox(label="LLM name", placeholder="Must be unique")
                                llm_vendor = gr.Dropdown(label="LLM vendors", choices=["ChatOpenAI", "AzureChatOpenAI", "LlamaCppChat"])
                                specification = gr.TextArea(label="Specification", placeholder="Specification in YAML format")
                                set_default = gr.Checkbox(label="Set default")
                                add_button = gr.Button("Add LLM")
                            with gr.Column():
                                gr.Markdown("### Spec description")
                                gr.Markdown("Select an LLM to view the spec description.")
                        add_button.click(handle_add, inputs=[llm_name, llm_vendor, specification, set_default], outputs=gr.Markdown())
            
            with gr.TabItem("Embeddings"):
                gr.Markdown("### Embeddings")
                with gr.Row():
                    with gr.TabItem("View"):
                # Corrected data format for the DataFrame
                        data = [
                            ["azure", "AzureOpenAIEmbeddings", "false"],  # Data as a list of lists
                            ["openai", "penAIEmbeddings", "true"],
                            ["ollama","penAIEmbeddings","false"],
                            ["local-bge-en","FastEmbedEmbeddings","false"]
                        ]
                        
                        headers = ["name", "vendor", "default"]

                        # Defining the DataFrame with corrected format
                        df = gr.Dataframe(value=data, headers=headers, interactive=False, height=200)
                    with gr.TabItem("Add"):
                        with gr.Row():
                            with gr.Column():
                                name = gr.Textbox(label="Name", placeholder="Must be unique and non-empty")
                                vendors = gr.Dropdown(label="Vendors", choices=["AzureOpenAIEmbeddings","OpenAIEmbeddings","FastEmbedEmbeddings"])
                                specification = gr.TextArea(label="Specification", placeholder="Specification in YAML format")
                                set_default = gr.Checkbox(label="Set default")
                                add_button = gr.Button("Add")
                                add_button.click(handle_add, inputs=[name, vendors, specification, set_default], outputs=gr.Markdown())
                        
            

    return app

# Launch the app
if __name__ == "__main__":
    app = create_app()
    app.launch()
