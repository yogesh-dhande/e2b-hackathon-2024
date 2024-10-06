import json
import os
import xml.etree.ElementTree as ET

from langchain.agents import AgentExecutor
from langchain.agents import create_tool_calling_agent
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from glob import glob

llm = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-405b-instruct")

@tool
def do_nothing():
  """
  Do nothing
  """
  return "Do nothing"


tools = [do_nothing]

system_prompt = """
You are a experience Flask and FastAPI developer.
Your task is to convert your Flask app to FastAPI.
Respond with target filepaths and content in JSON format.
The output should a valid JSON array with each object in the array 
containing two keys: "filepath" and "content".
The filepath should be relative to the current working directory.
The content should be the contents of the file.
"""
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            system_prompt,
        ),
        ("human", "{input}"),
        # Placeholders fill up a **list** of messages
        ("placeholder", "{agent_scratchpad}"),
    ]
)


agent = create_tool_calling_agent(llm, tools, prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

def run_agent(prompt):
    response = agent_executor.invoke({"input": prompt})
    return response["output"]


def is_file_allowed(file_path):
    # check if it's a file
    if not os.path.isfile(file_path):
        return False
    if "__pycache__" in file_path or file_path.endswith(".db"): 
        return False

    return True

def get_tree_as_json(root_dir):
    # os.chdir(root_dir)
    filepaths = glob(f"*", recursive=True)
    filtered_files = [filepath for filepath in filepaths if is_file_allowed(filepath)]

    context = ''
    for filepath in filtered_files:
        context += "\nfilepath: " + filepath + "\n```" + open(filepath).read()+"\n```\n"
    return context


def get_tree_as_xml(root_dir):
    filepaths = glob(f"{root_dir}/**/*", recursive=True)
    filtered_files = [filepath for filepath in filepaths if is_file_allowed(filepath)]
    
    # Create the root element
    root = ET.Element("files")
    
    for filepath in filtered_files:
        file_element = ET.SubElement(root, "file")
        filepath_element = ET.SubElement(file_element, "filepath")
        filepath_element.text = filepath
        
        content_element = ET.SubElement(file_element, "content")
        content_element.text = open(filepath).read()
    
    # Convert the XML tree to a string
    return ET.tostring(root, encoding='unicode')
    

def convert_flask_to_fastapi(root_dir):
    # TODO: implement LLM agent to convert code to fastapi
    return "examples/fastapi/lost_and_found"



