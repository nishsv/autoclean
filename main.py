import shutil
import os
import autopep8
import ast
from openai import OpenAI
import re

from dotenv import load_dotenv

load_dotenv('.env')
gpt_api_key = os.getenv('gpt_api_key')# Initialize OpenAI client

import shutil
import os

def clone_repo(src, dst):
    """
    Clone the repository from src to dst, leaving the .git directory intact.
    """
    if os.path.exists(dst):
        shutil.rmtree(dst)

    # Copy everything except the .git directory
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns('.git'))
    print(f"Repository cloned from {src} to {dst}")


def read_codebase(repo_path):
    """
    Recursively reads all Python files in the repository.
    """
    python_files = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def cleanup(file):
    """
    Generate a docstring for the function using OpenAI's GPT model.
    """

    with open(file, 'r', encoding='utf-8') as f:
        code = f.read()
    
    prompt = f"""

    Instructions:
    1. Clean the code without affecting the logic behind it
    2. Add comments in the start of every function, parameters shortly
    3. Follow PEP8 standards strictly

    Input code:
    {code}
    """

    client = OpenAI(api_key=gpt_api_key)
    response = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': "".join('You are an expert in following PEP8 standards')},
            {'role': 'user', 'content': "".join(prompt)}
        ],
        model='gpt-4',
        temperature=0.01,
        max_tokens=4096,
        top_p=1
    )
    resp = response.choices[0].message.content

    # start = resp.find('python')
    # end = resp[::-1].find('```')
    # content = resp[start:end]

    with open(file, 'w') as f:
        f.write(resp)



# Main flow
src_repo_path = "C:/Users/nishanth.sivalingam/Desktop/ChatBot"
dst_repo_path = "C:/Users/nishanth.sivalingam/Desktop/ChatBot_Cleaned"
clone_repo(src_repo_path, dst_repo_path)

repo_path = dst_repo_path
files = read_codebase(repo_path)
print(f"Found {len(files)} Python files.")

for file in files:
    print('Processing : ', file)
    cleanup(file)