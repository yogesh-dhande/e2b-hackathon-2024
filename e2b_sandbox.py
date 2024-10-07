import os
import time
from e2b_code_interpreter import CodeInterpreter
from e2b import Sandbox

import streamlit as st



def run_app(local_project_folder):
    # Initialize sandbox
    sandbox = CodeInterpreter()

    # Define the directories and necessary files for the app
    home_dir = "/home/user"
    app_dir = f"{home_dir}/app"

    # Create the app folder and the necessary subfolders
    sandbox.filesystem.make_dir(app_dir)
    sandbox.filesystem.make_dir(f"{app_dir}/templates")
    sandbox.filesystem.make_dir(f"{app_dir}/static")
    st.session_state.stderr = "No errors yet"
    st.session_state.stdout = "No output yet"

    def handle_stdout(output):
        print(output.line) # st.session_state.output.line

    def handle_stderr(output):
        print(output.line)
        

    # Copy the files from the local project folder to the e2b sandbox
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
        "pip install --upgrade pip && pip install fastapi sqlalchemy uvicorn jinja2 python-multipart", 
        on_stdout=handle_stdout,
        on_stderr=handle_stderr
    ).wait()

    # Start the FastAPI server in the sandbox
    open_port = 8080
    domain = sandbox.get_hostname(open_port)
    url = f"https://{domain}"
    print(f"FastAPI app will run at {url}")
    st.session_state.url = url
    st.session_state.sandbox_id = sandbox.id
    sandbox.process.start(
        f"cd {app_dir} && sudo uvicorn app:app --host 0.0.0.0 --port {open_port}",
        on_stdout=handle_stdout,
        on_stderr=handle_stderr
    )
    sandbox.keep_alive(60 * 2)
    sandbox.close()
    return url


def get_sandbox_error(sandbox_id):
    try:
        sandbox = Sandbox.reconnect(sandbox_id) 
        error = sandbox.filesystem.read("/home/user/app/error.txt")
        return error
    except Exception as e:
        pass
    


if __name__ == "__main__":
    run_app("tmp/hello/fastapi")
