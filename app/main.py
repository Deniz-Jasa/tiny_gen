from fastapi import FastAPI, APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from utils.github_interaction import (
    get_repo_files_as_string, 
    create_pull_request
)
from utils.code_assistant import modify_code

router = APIRouter()

class CodeRequest(BaseModel):
    repoUrl: str
    prompt: str
    create_pr: Optional[bool] = True

class DiffResponse(BaseModel):
    diff: str
    pr_url: Optional[str] = None
    
@router.get("/")
async def base_url():
    return {"message": "Welcome to Code Generator!"}

@router.post("/run")
async def run_code_assistant(request: CodeRequest):
    try:
        if not request.repoUrl:
            raise HTTPException(status_code=400, detail="Repository URL is required")

        print(f"Starting process for repo: {request.repoUrl}")
        
        # Get current code
        code_content = get_repo_files_as_string(request.repoUrl)
        print("Successfully got repo content")
        
        # Get AI suggestions
        modified_content = modify_code(request.prompt, code_content)
        print("Got AI modifications")
        
        # Create PR if requested
        pr_url = None
        if request.create_pr:
            print("Attempting to create PR...")
            try:
                pr_url = create_pull_request(
                    repo_url=request.repoUrl,
                    modified_content=modified_content['modified_files'],
                    pr_description=modified_content['pr_description']
                )
                print(f"Successfully created PR: {pr_url}")
            except Exception as e:
                print(f"PR creation failed with error: {str(e)}")
                raise HTTPException(status_code=500, detail=f"PR creation failed: {str(e)}")
        
        return {
            "modified_files": modified_content['modified_files'],
            "pr_description": modified_content['pr_description'],
            "pr_url": pr_url
        }
            
    except Exception as e:
        print(f"Error in run_code_assistant: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
app = FastAPI()
app.include_router(router)