from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from github_interaction import get_repo_files
from chatgpt_interaction import generate_diff_with_chatgpt
import platform
import subprocess

router = APIRouter()

class CodegenRequest(BaseModel):
    repoUrl: str
    prompt: str

class DiffResponse(BaseModel):
    diff: str

def execute_command_based_on_prompt(prompt: str) -> str:
    system = platform.system()

    if "list files" in prompt:
        if system == "Windows":
            command = "dir"
        else:
            command = "ls"
    else:
        command = "ls"

    output = subprocess.check_output(command, shell=True).decode("utf-8")
    return output

@router.post("/generate-diff/", response_model=DiffResponse)
async def generate_diff(request: CodegenRequest):
    files = get_repo_files(request.repoUrl)
    output = execute_command_based_on_prompt(request.prompt)
    diff = generate_diff(files, output)
    corrected_diff = await generate_diff_with_chatgpt(diff)
    return DiffResponse(diff=corrected_diff)
