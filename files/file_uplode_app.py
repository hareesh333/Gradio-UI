import gradio as gr
import pandas as pd
import os
from datetime import datetime

# Initialize an empty DataFrame to store file data dynamically
file_df = pd.DataFrame(columns=["name", "size", "tokens", "loader", "date_created"])

def upload_file(files):
    global file_df
    if files is not None:
        # Gather metadata for each uploaded file
        new_files_data = []
        for file in files:
            file_name = file.name
            file_size = f"{os.path.getsize(file.name) // 1024}KB"  # File size in KB
            tokens = f"{len(file.read()) // 1000}K"  # Tokens estimate (just a rough example)
            loader = "AutoLoader"  # Placeholder, adjust based on logic to detect file loader
            date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Append new file data to the DataFrame
            new_files_data.append({
                "name": file_name, 
                "size": file_size, 
                "tokens": tokens, 
                "loader": loader, 
                "date_created": date_created
            })

        # Update the DataFrame with new files
        new_files_df = pd.DataFrame(new_files_data)
        file_df = pd.concat([file_df, new_files_df], ignore_index=True)
        return file_df  # Return updated file list for display

    return file_df  # Return empty or existing file list

def filter_files(name_filter):
    if name_filter:
        filtered_df = file_df[file_df['name'].str.contains(name_filter, case=False, na=False)]
    else:
        filtered_df = file_df
    return filtered_df

def download_all_files():
    return "Download all files clicked!"

def create_file_upload_tab():
    with gr.Column(scale=1):
        with gr.TabItem("File Collection"):
            gr.Markdown("### File Upload")
            
            # Allow multiple file uploads
            upload_area = gr.Files(label="Drop Files Here\n- or -\nClick to Upload", 
                                   file_types=[".png", ".jpeg", ".jpg", ".tiff", ".tif", ".pdf", ".xls", ".xlsx", ".doc", ".docx", ".pptx", ".csv", ".html", ".mhtml", ".txt", ".zip"])
            
            gr.Markdown("""
                - Supported file types: .png, .jpeg, .jpg, .tiff, .tif, .pdf, .xls, .xlsx, .doc, .docx, .pptx, .csv, .html, .mhtml, .txt, .zip
                - Maximum file size: 1000 MB (manually enforced in the backend)
            """)

            with gr.Accordion("Advanced indexing options", open=False):
                force_reindex = gr.Checkbox(label="Force reindex file")

            upload_button = gr.Button("Upload and Index")

    with gr.Column(scale=2):
        gr.Markdown("### File List")

        # Filter box for searching file list
        name_filter = gr.Textbox(placeholder="Filter by name:", label="Filter by name (1) Case-insensitive. (2) Search with empty string to show all files.")
        filtered_file_list = gr.DataFrame(value=file_df, headers=["name", "size", "tokens", "loader", "date_created"], interactive=False, max_rows=10)
        
        # Update file list when a file is uploaded
        upload_button.click(upload_file, inputs=upload_area, outputs=filtered_file_list)
        
        # Filter file list based on search
        name_filter.change(filter_files, inputs=name_filter, outputs=filtered_file_list)

        download_button = gr.Button("Download all files")
        download_button.click(download_all_files, outputs=gr.Textbox())

# Call this function in the main app to create the File Upload UI
    return (upload_area, filtered_file_list, name_filter)
    

