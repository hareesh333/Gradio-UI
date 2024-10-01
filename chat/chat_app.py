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

def update_info_panel(message):
    graph = create_sample_graph()
    df = pd.DataFrame({
        "entity": [message],
        "description": [f"{message} is related to advanced information retrieval in HybridRAG."]
    })
    return graph, df
custom_css = """
/* Reset default body margins and padding */
body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Style for the main container to remove padding and margins */
.gradio-container {
    padding: 10px 10px !important; /* Reduced padding: top/bottom 10px, left/right 10px */
    margin: 0 !important; /* Remove default margins */
    max-width: 100% !important; /* Ensure it spans full width */
    box-sizing: border-box !important; /* Include padding in width calculations */
}

/* Hide Gradio footer if present */
.gr-footer {
    display: none !important;
}

/* Responsive Design for Small Screens */
@media (max-width: 600px) {
    .gr-row {
        flex-direction: column !important; /* Stack elements vertically on small screens */
    }

    .gr-column {
        width: 100% !important; /* Full width for columns on mobile */
    }

    /*.gr-button {
        padding: 8px 8px !important;  /* Increase padding for easier tapping */
        font-size: 14px !important;     /* Slightly larger font size */
    }*/

    .gr-chatbot {
        height: auto !important; /* Adjust height for mobile */
        max-height: 400px !important; /* Limit height for better visibility */
    }
}

@media (min-width: 50px) {
    .gr-button {
        min-width: 50px !important; /* Wider buttons on desktop */
    }

    .gr-chatbot {
        height: 600px !important; /* Maintain height on larger screens */
    }
}
.gr-button {
        border: none;
        color: white;
        padding: 10px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
    }
/* Existing button styles */
/*.gr-button {
    padding: 4px 8px !important;  
    font-size: 12px !important;   
}*/

.gr-button-primary {
    color:#42A5F5;
    
}

.no-background {
    border: none !important;
    background: none !important;
    box-shadow: 20px !important;
}

.custom-button-row {
    display: flex !important;
    justify-content: flex-start !important;
    gap: 10px !important;
    
}

/* Define custom classes for additional styling */

/* Custom class for body text color */
.body-text-color {
    color: #333333 !important; /* Example: Dark gray text */
}

/* Custom class for button height */
.cap-button-height {
    height: 40px !important; /* Example: Fixed height */
}

/* Optional: Style for the header textbox */
.custom-header-textbox {
    font-weight: bold !important;
    font-size: 16px !important;
}
/* Style for the custom footer */
.custom-footer {
    text-align: center !important;
    padding: 10px !important;
    font-size: 12px !important;
    color: #ffffff !important;
    background: linear-gradient(90deg, #0D47A1 40%, #42A5F5 60%);!important; /* Optional: Light background for the footer */
    position: fixed !important;
    bottom: 0 !important;
    width: 100% !important;
}    
/* Optional: Remove padding/margin from specific components if needed */
.custom-remove-padding {
    padding: 0 !important;
    margin: 0 !important;
}
"""
def chat_app_interface():
    with gr.Blocks(theme=gr.themes.Default(primary_hue=gr.themes.colors.blue),css=custom_css) as demo:
    # Adding header with buttons
        with gr.Tabs():
            with gr.TabItem("Chat"):
                gr.Markdown("### Conversation")
                
                with gr.Row():
                    with gr.Column(scale=1):
                        with gr.Row():
                            # Added custom class for header textbox
                            gr.Textbox(
                                "HybridRAG: Advanced Information Retrieval",
                                elem_classes=["custom-header-textbox"],
                                interactive=False,
                                label=None
                            )
                        with gr.Row(elem_classes=["custom-button-row"]):
                            gr.Button(
                                "🆕", size="sm", min_width=2, scale=1,
                                elem_classes=["no-background", "body-text-color"]
                            )  # New icon
                            gr.Button(
                                "🗑️", size="sm", min_width=2, scale=1,
                                elem_classes=["no-background", "body-text-color"]
                            )  # Delete icon
                            gr.Button(
                                "✏️", size="sm", min_width=2, scale=1,
                                elem_classes=["no-background", "body-text-color"]
                            )  # Edit icon
                            gr.Button(
                                "📤", size="sm", min_width=2, scale=1,
                                elem_classes=["no-background", "body-text-color"]
                            )  # Share icon
                        
                        with gr.Row():
                            with gr.Accordion("File Collection", open=True):
                                file_search_all = gr.Button("Search All", size="sm",variant="primary")  # Search All
                                file_search_in = gr.Button("Search In File(s)", size="sm")  # Search In File(s)
        
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
                            send_btn = gr.Button(
                                value="Send",
                                size="sm",
                                variant="primary",
                                scale=1,
                                min_width=10,
                                elem_classes=["cap-button-height"]
                            )
                            regen_btn = gr.Button(
                                value="Cancel",
                                scale=1,
                                min_width=10,
                                size="sm",
                                elem_classes=["cap-button-height"]
                            )
                        
                        gr.Markdown("### Chat settings")
                    
                    with gr.Column(scale=1):
                        with gr.Accordion("Information Panel", open=True):
                            graph_output = gr.Plot(label="Knowledge Graph")
                            entity_table = gr.DataFrame(
                                label="Table from Entities",
                                headers=["entity", "description"]
                            )
        
                    # Event handler for the send button, updating both chat and the info panel
                    send_btn.click(
                        update_chat,
                        inputs=[chat_input, chatbot],
                        outputs=[chatbot, chatbot]
                    ).then(
                        update_info_panel,
                        inputs=chat_input,
                        outputs=[graph_output, entity_table]
                    )
        
                    # Event handlers for file search buttons
                    graph_search_all.click(
                        lambda: search_files("", "All GraphRAG"),
                        outputs=chatbot
                    )
                    graph_search_in.click(
                        lambda: search_files("", "Selected GraphRAG Files"),
                        outputs=chatbot
                    )
                    file_search_all.click(
                        lambda: search_files("", "All Files"),
                        outputs=chatbot
                    )
                    file_search_in.click(
                        lambda: search_files("", "Selected Files"),
                        outputs=chatbot
                    )

    demo.launch()

# This function can be imported and used in the main app file where the Blocks instance is created.
if __name__ == "__main__":
    app = chat_app_interface()
    app.launch()