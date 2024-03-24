import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def ask_chatgpt(prompt, code_block):
    """
    Sends a task and code block to GPT-3.5, returning a version of the code modified to meet the task's requirements.

    Parameters:
    - prompt (str): Description of the task to achieve.
    - code_block (str): Original code block that needs modification.

    Returns:
    - str: Modified version of the original code to fulfill the specified task.
    """
    full_prompt = (
        f"Given the full code:\n{code_block}\n"
        f"Based on the following task: {prompt}, "
        "rewrite the above code to incorporate the necessary changes. "
        "Please return the full code with modified changes."
    )
    
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": full_prompt
            }
        ],
        temperature=0.3,
        max_tokens=1024  # Can be adjusted to allow for larger repos. Note: Can result in slower response time.
    )

    return completion.choices[0].message.content
