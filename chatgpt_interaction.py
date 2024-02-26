import httpx

CHATGPT_API_URL = "https://api.openai.com/v1/completions"
OPENAI_API_KEY = "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" 

async def generate_diff_with_chatgpt(prompt: str) -> str:
    """
    Generate a diff or code snippet using OpenAI's GPT API based on the provided prompt.

    Args:
        prompt (str): The prompt or command for generating the diff.

    Returns:
        str: The generated diff or code snippet.
    """
    try:
        if not prompt:
            raise ValueError("Prompt cannot be empty")
        
        headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
        data = {"prompt": prompt, "max_tokens": 100, "temperature": 0.7}

        async with httpx.AsyncClient() as client:
            response = await client.post(CHATGPT_API_URL, headers=headers, json=data)
            response.raise_for_status()  # Raise an error for non-2xx responses
            response_data = response.json()
            generated_diff = response_data["choices"][0]["text"].strip()
            return generated_diff
    except Exception as e:
        # Handle any exceptions and return an empty string or raise an error based on your requirements
        return ""