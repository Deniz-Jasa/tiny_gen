from fastapi import FastAPI
from endpoints import generate_diff_endpoint

tiny_gen_app = FastAPI()

# Add of the endpoint routes to the 
tiny_gen_app.include_router(generate_diff_endpoint.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(tiny_gen_app, host="0.0.0.0", port=8000)
