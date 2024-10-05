import os
from e2b_code_interpreter import CodeInterpreter

# Set your e2b API Key
os.environ["E2B_API_KEY"] = ""

# Initialize sandbox
sandbox = CodeInterpreter()

# Define the directories and necessary files for the app
home_dir = "/home/user"
app_dir = f"{home_dir}/app"

# Create the app folder and the necessary subfolders
sandbox.filesystem.make_dir(app_dir)
sandbox.filesystem.make_dir(f"{app_dir}/templates")
sandbox.filesystem.make_dir(f"{app_dir}/static")

# Write a basic FastAPI app that serves an HTML page
fastapi_code = """
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "message": "Welcome to the Lost and Found App!"})
"""

# Write the FastAPI app code to the sandbox
sandbox.filesystem.write(f"{app_dir}/main.py", fastapi_code)

# Write a basic HTML template (index.html)
index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lost and Found</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>{{ message }}</h1>
    <p>Report and find lost items here.</p>
</body>
</html>
"""

# Write the index.html template to the sandbox
sandbox.filesystem.write(f"{app_dir}/templates/index.html", index_html)

# Write a basic CSS file (style.css)
style_css = """
body {
    font-family: Arial, sans-serif;
    margin: 0 auto;
    padding: 20px;
    max-width: 800px;
    background-color: #f9f9f9;
}

h1 {
    color: #333;
}
"""

# Write the CSS file
sandbox.filesystem.write(f"{app_dir}/static/style.css", style_css)

# Install necessary packages in the e2b sandbox environment
sandbox.process.start(
    "pip install fastapi uvicorn jinja2 python-multipart", 
    on_stdout=lambda output: print("Installing dependencies: ", output.line),
    on_stderr=lambda output: print("Error installing dependencies: ", output.line)
)

# Start the FastAPI server in the sandbox
open_port = 8080
url = sandbox.get_hostname(open_port)
print(f"FastAPI app will run at https://{url}")

sandbox.process.start(
    f"cd {app_dir} && uvicorn main:app --host 0.0.0.0 --port {open_port} --reload",
    on_stdout=lambda output: print("STDOUT: ", output.line),  # Capture stdout logs
    on_stderr=lambda output: print("STDERR: ", output.line),  # Capture stderr logs
)
