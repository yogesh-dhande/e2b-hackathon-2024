import os
import time
from e2b_code_interpreter import CodeInterpreter

# Initialize sandbox
sandbox = CodeInterpreter()

# Define the directories and necessary files for the app
home_dir = "/home/user"
app_dir = f"{home_dir}/app"

# Create the app folder and the necessary subfolders
sandbox.filesystem.make_dir(app_dir)
sandbox.filesystem.make_dir(f"{app_dir}/templates")
sandbox.filesystem.make_dir(f"{app_dir}/static")


def run_app(local_project_folder):
    for root, dirs, files in os.walk(local_project_folder):
        for file in files:
            if "__pycache__" in root or "__pycache__" in file or file.endswith(".db"): 
                continue
            local_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_path, local_project_folder)
            remote_path = os.path.join(app_dir, relative_path)
            print(local_path, remote_path)

            # Upload file to the sandbox in the specified directory
            with open(local_path, "r") as f:
                # Write the FastAPI app code to the sandbox
                content = f.read()
                sandbox.filesystem.write(remote_path, content)

    # Install necessary packages in the e2b sandbox environment
    sandbox.process.start(
        "ls -lah /home/user/app", 
        on_stdout=lambda output: print("Installing dependencies: ", output.line),
        on_stderr=lambda output: print("Error installing dependencies: ", output.line)
    ).wait()


    # Install necessary packages in the e2b sandbox environment
    sandbox.process.start(
        "pip install --upgrade pip && pip install fastapi sqlalchemy uvicorn jinja2 python-multipart", 
        on_stdout=lambda output: print("Installing dependencies: ", output.line),
        on_stderr=lambda output: print("Error installing dependencies: ", output.line)
    ).wait()

    # Start the FastAPI server in the sandbox
    open_port = 8080
    domain = sandbox.get_hostname(open_port)
    url = f"https://{domain}"
    print(f"FastAPI app will run at {url}")

    sandbox.process.start(
        f"cd {app_dir} && sudo uvicorn main:app --host 0.0.0.0 --port {open_port} --reload",
        on_stdout=lambda output: print("STDOUT: ", output.line),  # Capture stdout logs
        on_stderr=lambda output: print("STDERR: ", output.line),  # Capture stderr logs
    )
    sandbox.keep_alive(60 * 5)
    sandbox.close()
    return url
