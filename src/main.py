import os
import glob
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import gradio as gr


load_dotenv(override=True)

api_key = os.getenv('OPENAI_API_KEY')

MODEL = "gpt-4.1-nano"

openai = OpenAI()

SYSTEM_PREFIX = """
You represent FC Barcelona, the Soccer Team.
You are an expert in answering questions about FC Barcelona; its employees.
You are provided with additional context that might be relevant to the user's question.
Give brief, accurate answers. If you don't know the answer, say so. use english.

Relevant context:
"""

knowledge = {}

def load_markdown_files(base_path="data/employees"):
    """
    Loads Markdown files from a specified directory into a dictionary.

    This function iterates through all files in the given directory. For each file
    with a `.md` extension, it reads the content and stores it in a dictionary with
    the filename (excluding the `.md` extension) as the key. The dictionary is
    returned, containing all the processed Markdown files.

    :param base_path: Path to the directory containing the Markdown files. Defaults to
        "data/employees".
    :type base_path: str
    :return: A dictionary where keys are filenames (without `.md` extensions) and
        values are the contents of the corresponding Markdown files.
    :rtype: dict
    """
    data = {}

    filenames = glob.glob("data/employees/*")

    for filename in filenames:
        name = Path(filename).stem.split('_')[-1]
        with open(filename, "r", encoding="utf-8") as f:
            data[name.lower()] = f.read()
    return data

def get_relevant_context(message):
    text = ''.join(ch for ch in message if ch.isalpha() or ch.isspace())
    words = text.lower().split()
    return [knowledge[word] for word in words if word in knowledge]

def additional_context(message):
    relevant_context = get_relevant_context(message)
    if not relevant_context:
        result = "There is no additional context relevant to the user's question."
    else:
        result = "The following additional context might be relevant in answering the user's question:\n\n"
        result += "\n\n".join(relevant_context)
    return result

def chat(message, history):
    system_message = SYSTEM_PREFIX + additional_context(message)
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

if __name__ == "__main__":
    knowledge = load_markdown_files()
    view = gr.ChatInterface(chat, type="messages").launch(inbrowser=True, debug=True)
    print("Loaded employees:", list(knowledge.keys()))