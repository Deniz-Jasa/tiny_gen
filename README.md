# Deniz Jasarbasic's TinyGen

TinyGen is a simplified version of Codegen, a code generation service designed to transform code from a public GitHub repository based on specific prompts, such as converting the code to a different language (e.g., TypeScript). The service outputs the difference (diff) between the original and transformed code. Had a blast and hope you enjoy my implementation :)


## Overview

To build this service, my implementation uses FastAPI, Supabase DB for storage, and AWS EC2 to host the API along with a collection of small Python utility functions to fetch code, transform code, store code, and return a diff.


## Notion Page

For more detailed information about the implementation of this FastAPI service. The page breaks down how I approached this technical challenge, the process, and docs for future maintenance of this app. You can visit my Notion page: [Deniz Jasarbasic's TinyGen](https://quilled-sky-f24.notion.site/Deniz-Jasarbasic-s-TinyGen-812426b2eadb48c884f5ebd584446d50?pvs=4)


## Usage

### Basics

The base URL for the TinyGen API is `base_api_url` = [http://3.22.241.58](http://3.22.241.58)

| Methods | Endpoints | Description                                         |
|---------|-----------|-----------------------------------------------------|
| GET     | `/`       | Returns a welcome message.                          |
| POST    | `/run`    | Executes tinygen with required parameters repoUrl and prompt in the request body. Return a unified diff of suggested changes. |
| GET     | `/docs`   | Provides interactive API documentation via Swagger UI. |


### Request Body

```json
{
    "repoUrl": "a public GitHub URL",
    "prompt": "A prompt, ex: Convert the source code to Java."
}
```

### Response

```json
{
  "diff": ...
}
```

- The `diff` attribute contains a unified diff (as a string) between the orginal code and modified suggested code by ChatGPT.
  
## Status Codes

TinyGen returns the following status codes in its API:

| Status Code | Description            |
|-------------|------------------------|
| 200         | OK                     |
| 400         | BAD REQUEST            |
| 422         | UNPROCESSABLE ENTITY   |
| 500         | INTERNAL SERVER ERROR  |

## Run in Postman

Click the button below to import the Postman collection and environment file. Play around with the `Welcome` and `Run` steps. The example in the collection below uses a simple multi-file python repository and asks a simple prompt to convert the code to Java. Feel free to play around with this example or use your own:

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/15932234-bd2d4ba5-5fbc-42d8-bcd9-c0b0f236f852?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D15932234-bd2d4ba5-5fbc-42d8-bcd9-c0b0f236f852%26entityType%3Dcollection%26workspaceId%3Dffed2e4e-5834-47b3-af33-a3c5f6ab80d5)

## Interactive Swagger Docs Tool

Explore the API endpoints using the interactive Swagger documentation tool at [http://3.22.241.58/docs](http://3.22.241.58/docs)


## Local Setup

### Step 1: Dependencies

Tinygen uses Python 3. All necessary libraries are listed in the **`requirements.txt`** file. Install them by running **`pip install -r requirements.txt`**.

- Python ≥ 3.9.7
- Libraries: difflib, os, OpenAI, python-dotenv, PyGithub, supabase, uvicorn, pydantic, fastapi

### Step 2: Environment Variables

You can create a .env file locally to store the key information below, or pass it via secrets when deployed.

```python
# ChatGPT API Access
OPENAI_API_KEY=""

# GitHub API Access
GITHUB_TOKEN=""

# Supabase Configuration
SUPABASE_URL=""
SUPABASE_KEY=""
```

### Step 3: Running Tinygen

Go to the `app/` directory and run:
```python
python3 -m uvicorn main:app --reload
```

<br>