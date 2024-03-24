from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from utils.github_interaction import get_repo_files_as_string
from utils.chatgpt_interaction import ask_chatgpt
from utils.calculate_diff import calculate_code_diff
from utils.supabase_integration import store

router = APIRouter()

class TinyGenRequest(BaseModel):
    repoUrl: str
    prompt: str

class DiffResponse(BaseModel):
    diff: str
    
@router.get("/")
async def base_url():
    return {"message": "Welcome to Deniz Jasarbasic's Implementation of the TinyGen API!"}

@router.post("/run", response_model=DiffResponse)
async def run_tiny_gen(request: TinyGenRequest):
    try:
        original_code = get_repo_files_as_string(request.repoUrl)
        fixed_code = ask_chatgpt(request.prompt, original_code)
        
        reflection_text = (
            f"Review changes against requirements: '{request.prompt}'. "
            "Reply with [CONFIDENT] for no further improvements needed, or "
            "[REVISION NEEDED] for more adjustments."
        )
        
        code_for_reflection = f"Modified Code:\n{fixed_code} \n Original Code:\n{original_code}\n\n"
        
        reflection_response = ask_chatgpt(reflection_text, code_for_reflection)
        
        if "[REVISION NEEDED]" in reflection_response:
            fixed_code = reflection_response.replace("[REVISION NEEDED]", "").strip() # remove the revision flag
        
        diff = calculate_code_diff(original_code, fixed_code)

        # Store data in Supabase
        store_data = {
            "repo_url": request.repoUrl,
            "prompt": request.prompt,
            "original_code": original_code,
            "fixed_code": fixed_code,
            "diff": diff,
            "timestamp": datetime.now().isoformat()
        }
        store(store_data)
        
        return DiffResponse(diff=diff)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
app = FastAPI()
app.include_router(router)