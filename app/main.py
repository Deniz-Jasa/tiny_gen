from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from utils.github_interaction import get_repo_files_as_string
from utils.chatgpt_interaction import ask_chatgpt
from utils.calculate_diff import calculate_code_diff

router = APIRouter()

class TinyGenRequest(BaseModel):
    repoUrl: str
    prompt: str

class DiffResponse(BaseModel):
    diff: str

@router.post("/run", response_model=DiffResponse)
async def run_tiny_gen(request: TinyGenRequest):
    try:
        # Fetch code from the GitHub repository
        original_code = get_repo_files_as_string(request.repoUrl)

        # Initial suggestion
        fixed_code = ask_chatgpt(request.prompt, original_code)
        
        # Ask for reflection
        reflection_prompt = "Are you sure about the changes? Would you like to correct anything?"
        reflection_response = ask_chatgpt(reflection_prompt, fixed_code)
        
        # If GPT wants to correct, generate a new suggestion
        if "no" in reflection_response.lower(): # Assuming GPT responds with "no" to indicate a correction
            fixed_code = ask_chatgpt(request.prompt, original_code)  # Generate a new suggestion
        
        # Calculate the difference between original and fixed code
        diff = calculate_code_diff(original_code, fixed_code)

        return DiffResponse(diff=diff)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()
app.include_router(router)
