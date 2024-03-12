# Deniz Jasarbasic's TinyGen

TinyGen is a simplified version of Codegen, a code generation service designed to transform code from a public GitHub repository based on specific prompts, such as converting the code to a different language (e.g., TypeScript). The service outputs the difference (diff) between the original and transformed code. Had a blast and hope you enjoy my implementation :)


## Overview

To build this service, my implementation uses FastAPI, Supabase DB for storage, and AWS EC2 to host the API along with a collection of small Python utility functions to fetch code, transform code, store code, and return a diff.


## Notion Page

For more detailed information about the implementation of this FastAPI service. The page breaks down how I approached this technical challenge, the process, and docs for future maintenance of this app. You can visit my Notion page: [Deniz Jasarbasic's TinyGen](https://quilled-sky-f24.notion.site/Deniz-Jasarbasic-s-TinyGen-812426b2eadb48c884f5ebd584446d50?pvs=4)


## Usage

### Base API URL

The base URL for the TinyGen API is `base_api_url` = [http://3.22.241.58](http://3.22.241.58)

You can access this URL on the web, and it will return a simple welcome message:
<img width="862" alt="Screenshot 2024-03-12 at 2 14 38 AM" src="https://github.com/Deniz-Jasa/tiny_gen/assets/46465622/b20b4cc9-fc80-4a98-bde5-3290efe7605b">

### Authorization

All API requests require the use of a generated API key. You can find your API key, or generate a new one, by navigating to the /settings endpoint, or clicking the “Settings” sidebar item.

```http
GET /api/campaigns/?api_key=12345678901234567890123456789012
```

### Send Body

```json
{
    "repoUrl": "a public GitHub URL",
    "prompt": "A prompt, ex: Change all the code to Java."
}
```

### Endpoints

`run` - Given a repoUrl and prompt, returns a unified diff (as a string) of changes in the code.

### Responses

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
| 201         | CREATED                |
| 400         | BAD REQUEST            |
| 404         | NOT FOUND              |
| 500         | INTERNAL SERVER ERROR  |

## Run in Postman Example

Click the button below to import the Postman collection and environment file. Play around with the `Welcome` and `Run` steps. The example in the collection below uses a simple multi-file python repository and asks a simple prompt to convert the code to Java. Feel free to play around with this example or use your own:

[<img src="https://run.pstmn.io/button.svg" alt="Run In Postman" style="width: 128px; height: 32px;">](https://app.getpostman.com/run-collection/15932234-bd2d4ba5-5fbc-42d8-bcd9-c0b0f236f852?action=collection%2Ffork&source=rip_markdown&collection-url=entityId%3D15932234-bd2d4ba5-5fbc-42d8-bcd9-c0b0f236f852%26entityType%3Dcollection%26workspaceId%3Dffed2e4e-5834-47b3-af33-a3c5f6ab80d5)

## Interactive Swagger Docs Tool

Explore the API endpoints using the interactive Swagger documentation tool at [http://3.22.241.58/docs](http://3.22.241.58/docs)


## Local Setup & Dependencies

Dependencies:

- Python
- FastAPI
- Python libraries: difflib, os, OpenAI, dotenv, github

`.env`  file or pass via secrets:

```python
# ChatGPT API Access
OPENAI_API_KEY=""

# GitHub API Access
GITHUB_TOKEN=""

# Supabase Configuration
SUPABASE_URL=""
SUPABASE_KEY=""
```

When running locally, go to the `app/` directory and run:

```python
python3 -m uvicorn main:app --reload
```

<br>