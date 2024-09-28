import gradio as gr
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def create_sample_graph():
    G = nx.random_geometric_graph(30, 0.2)
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=False, node_color='lightblue', 
            node_size=50, edge_color='gray', alpha=0.6)
    
    labels = {0: "VECTORRAG", 15: "HYBRIDRAG", 29: "GRAPHRAG"}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
    plt.title("Knowledge Graph Visualization")
    return plt

def search_files(query, collection):
    return f"Searching for '{query}' in {collection}"

def update_chat(message, history):
    if not history:
        history = []
    history.append((message, f"Response to: {message}"))
    return history, history

# Update the information panel based on the chat input
def update_info_panel(message):
    graph = create_sample_graph()
    
    # Update the DataFrame based on the message (chat input)
    df = pd.DataFrame({
        "entity": [message],
        "description": [f"{message} is related to advanced information retrieval in HybridRAG."]
    })
    return graph, df

# Click handler to update chat with the section clicked
def navigate_to_section(section, history):
    message = f"Navigating to {section} section"
    history.append((message, f"You are now in the {section} section"))
    return history, history
custom_css = """
.no-background {
    border: none !important;
    background: none !important;
    box-shadow: none !important;
}
.custom-button-row {
    display: flex;
    justify-content: flex-start;
    gap: 10px;
}
"""
with gr.Blocks(theme=gr.themes.Default(primary_hue=gr.themes.colors.blue), css=custom_css) as demo:
    # Adding header with buttons
    with gr.Tabs():
        with gr.TabItem("Chat"):
            gr.Markdown("### {message}: Advanced Information Retrieval")
            
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Row():
                        gr.Textbox("HybridRAG: Advanced Information Retrieval", label="Current Conversation")
                    with gr.Row():
                        gr.Button("🆕", size="sm",min_width=2,scale=1,
                        elem_classes=["no-background", "body-text-color"])  # New icon
                        gr.Button("🗑️", size="sm",min_width=2,scale=1,
                        elem_classes=["no-background", "body-text-color"])  # Delete icon
                        gr.Button("✏️", size="sm",min_width=2,scale=1,
                        elem_classes=["no-background", "body-text-color"])  # Edit icon
                        gr.Button("📤", size="sm",min_width=2,scale=1,
                        elem_classes=["no-background", "body-text-color"])  # Share icon
                    
                    with gr.Row():
                        with gr.Accordion("File Collection", open=True):
                            file_search_all = gr.Button("Search All", size="sm")  # Checkbox for "Search All"
                            file_search_in = gr.Button("Search In File(s)", size="sm")  # Checkbox for "Search In File(s)")

                    with gr.Row():
                        with gr.Accordion("GraphRAG Collection", open=True):
                            graph_search_all = gr.Button("Search All", size="sm")
                            graph_search_in = gr.Button("Search In File(s)", size="sm", variant="primary")
                    
                    gr.Markdown("### Quick Upload")
                    file_upload = gr.File()
                
                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(label="Chat History", height=600)
                    chat_input = gr.Textbox(label="Chat Input", placeholder="What is HybridRAG?")
                    
                    with gr.Row():
                        send_btn = gr.Button(value="Send",size="sm" ,variant="primary",scale=1,min_width=10,
                        elem_classes=["cap-button-height"])
                        regen_btn = gr.Button(value="Cancel",scale=1,min_width=10,size="sm",
                        elem_classes=["cap-button-height"])
                    
                    gr.Markdown("### Chat settings")
                
                with gr.Column(scale=1):
                    with gr.Accordion("Information Panel", open=True):
                        graph_output = gr.Plot(label="Knowledge Graph")
                        entity_table = gr.DataFrame(label="Table from Entities", headers=["entity", "description"])

                # Event handler for the send button, updating both chat and the info panel
                    send_btn.click(update_chat, [chat_input, chatbot], [chatbot, chatbot]).then(
                        update_info_panel, chat_input, [graph_output, entity_table])

                # Event handlers for file search buttons
                graph_search_all.click(lambda: search_files("", "All GraphRAG"), outputs=chatbot)
                graph_search_in.click(lambda: search_files("", "Selected GraphRAG Files"), outputs=chatbot)
                file_search_all.click(lambda: search_files("", "All Files"), outputs=chatbot)
                file_search_in.click(lambda: search_files("", "Selected Files"), outputs=chatbot) 
                # Event handlers for header buttons
        with gr.TabItem("Files"):
            
            gr.File(label="Upload files here")

        with gr.TabItem("Resources"):
            gr.Markdown("## Resources Page")
            gr.Markdown("This is the Resources page content.")

        with gr.TabItem("Settings"):
            gr.Markdown("## Settings Page")
            gr.Checkbox(label="Enable notifications")
            gr.Slider(minimum=0, maximum=100, label="Volume")

        with gr.TabItem("Help"):
            gr.Markdown("## Help Page")   
# Launch the app
demo.launch()