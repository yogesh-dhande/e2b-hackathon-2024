import os
import shutil
from fireworks.client import Fireworks

# Initialize Fireworks client
api_key = os.getenv("fw_3ZbroVgV8mZHos5hXttaMzCF")
client = Fireworks(api_key=api_key)

def get_file_content(file_path):
    try:
        print(f"Reading file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""

def clean_code(raw_code):
    """Extracts and returns only the code part from the raw response."""
    lines = raw_code.strip().splitlines()
    code = []
    inside_code_block = False

    for line in lines:
        if line.startswith("```python"):
            inside_code_block = True
            continue  # Skip the line that starts the code block

        if line.startswith("```") and inside_code_block:
            break  # Stop when the closing delimiter is found

        if inside_code_block:
            code.append(line)  # Add the line as is to maintain indentation
    
    return "\n".join(code)

def convert_flask_file_to_fastapi_raw(file_path):
    try:
        print(f"Converting Flask file to FastAPI: {file_path}")
        flask_code = get_file_content(file_path)
        
        print(f"Sending request to Fireworks API...")
        response = client.chat.completions.create(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            messages=[{
                "role": "user",
                "content": f"Convert the following Flask code to FastAPI:\n{flask_code}"
            }],
        )

        # Get the raw response content
        raw_response = response.choices[0].message.content
        print("Raw Response:", raw_response)  # Log the raw response

        # Clean the response to extract only the code
        code = clean_code(raw_response)
        return code

    except Exception as e:
        print(f"Error calling Fireworks API for {file_path}: {e}")
        return ""

def convert_to_fastapi(source_folder):
    # Create a single new folder for all converted files
    new_folder_name = source_folder.replace('/flask', '/fastapi')
    os.makedirs(new_folder_name, exist_ok=True)
    print(f"Created new folder: {new_folder_name}")

    # Copy templates and static files to the new folder
    templates_src = os.path.join(source_folder, 'templates')
    static_src = os.path.join(source_folder, 'static')
    
    # Copy templates if they exist
    if os.path.exists(templates_src):
        shutil.copytree(templates_src, os.path.join(new_folder_name, 'templates'), dirs_exist_ok=True)
        print(f"Copied templates from {templates_src} to {new_folder_name}/templates")
    
    # Copy static files if they exist
    if os.path.exists(static_src):
        shutil.copytree(static_src, os.path.join(new_folder_name, 'static'), dirs_exist_ok=True)
        print(f"Copied static files from {static_src} to {new_folder_name}/static")

    for root, dirs, files in os.walk(source_folder):
        if 'static' in dirs:
            dirs.remove('static')

        for file_name in files:
            # Check if the file has a .py extension
            if file_name.endswith('.py'):
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")
                converted_code = convert_flask_file_to_fastapi_raw(file_path)

                if converted_code:  # Check if conversion was successful
                    # Write the converted code to the new folder with the original filename
                    output_file_path = os.path.join(new_folder_name, file_name)  # Same filename, no change
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        output_file.write(converted_code)
                    print(f"Converted File: {output_file_path}")
                else:
                    print(f"Conversion failed for {file_name}")

    return new_folder_name

# # Constants for the source folder path
# SOURCE_FOLDER = "tmp/hello/flask"  # Specify your source folder here

# # Create the new folder structure and convert files
# create_flask_folder_structure(SOURCE_FOLDER)
