import streamlit as st
from agents import run_agent
import time
import shutil


st.write("# e2b-hackathon-2024")

import streamlit as st
import zipfile
import tempfile
import os

st.session_state.status = "not ready"


button = st.button("Run simulation")

if button:
  st.session_state.status = "running"
  time.sleep(2)


if "status" in st.session_state:
  st.write(st.session_state.status)


# Streamlit app
st.title("Upload and Extract ZIP File")

# File uploader
uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

if uploaded_file:
# Get the file name without the extension
    zip_file_name = os.path.splitext(uploaded_file.name)[0]
    # Remove any existing directory with the same name
    shutil.rmtree(os.path.join("tmp", zip_file_name), ignore_errors=True)

    # Define the base temporary directory
    base_tmpdir = "tmp"

    # Define the target directory: "tmp/<zip_file_name>/flask"
    target_dir = os.path.join(base_tmpdir, zip_file_name, "flask")

    # Ensure the directory exists
    os.makedirs(target_dir, exist_ok=True)

    # Open the ZIP file
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        # Iterate over each file in the zip
        for member in zip_ref.namelist():
            # Get only the file name (ignore any directory structure inside the zip)
            file_name = os.path.basename(member)
            
            # Skip directories
            if not file_name:
                continue
            
            # Define the full path to extract to
            file_path = os.path.join(target_dir, file_name)
            
            # Extract each file to the target directory
            with open(file_path, "wb") as output_file:
                with zip_ref.open(member) as source_file:
                    output_file.write(source_file.read())
    
    st.write(f"Extracted files to: {target_dir}")


