from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from utils.github_interaction import get_repo_files_as_string
from utils.chatgpt_interaction import tiny_gen
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

        # Generate fixed code using GPT-3
        fixed_code, changed_files = tiny_gen(request.prompt, original_code)

        # Calculate the difference between original and fixed code
        changed_files_str = '\n'.join(changed_files)
        diff = calculate_code_diff(original_code, fixed_code, changed_files_str)

        return DiffResponse(diff=diff)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app = FastAPI()
app.include_router(router)
