
import time
import shutil
import os
import streamlit as st
import zipfile

from agents import convert_flask_to_fastapi
from e2b_sandbox import get_sandbox_error, run_app
from llm import convert_to_fastapi

import streamlit.components.v1 as components

st.write("# Flask to the Future - Convert Flask apps to FastAPI")


# Streamlit app
st.title("Upload ZIP File of your Flask App")

# File uploader
uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")
# Create a placeholder for the code block
container = st.empty()


if uploaded_file:
# Get the file name without the extension
    zip_file_name = os.path.splitext(uploaded_file.name)[0]
    # Remove any existing directory with the same name
    shutil.rmtree(os.path.join("tmp", zip_file_name), ignore_errors=True)

    # Define the base temporary directory
    base_tmpdir = "tmp"

    # Define the target directory: "tmp/<zip_file_name>/flask"
    target_flask_dir = os.path.join(base_tmpdir, zip_file_name, "flask")
    target_fastapi_dir = os.path.join(base_tmpdir, zip_file_name, "fastapi")

    # Ensure the directory exists
    os.makedirs(target_flask_dir, exist_ok=True)

    # Open the ZIP file
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        # Iterate over each file in the zip
        for member in zip_ref.namelist():
            # Get only the file name (ignore any directory structure inside the zip)
            file_name = os.path.basename(member)
            
            # Skip directories
            if not file_name or ".py" not in file_name:
                # TODO: Handle directories
                continue
            
            # Define the full path to extract to
            file_path = os.path.join(target_flask_dir, file_name)
            
            # Extract each file to the target directory
            with open(file_path, "wb") as output_file:
                with zip_ref.open(member) as source_file:
                    content = source_file.read()
                    output_file.write(content)
                    
                    with container:
                      st.write(file_name)
                      st.code(content.decode('utf-8'))
                    time.sleep(2)

    app_url = run_app(convert_to_fastapi(target_flask_dir))

    if "url" in st.session_state:
        container.empty()
        with container:
            st.link_button("Open FastAPI App in E2B Sandbox", app_url)
