import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def ask_chatgpt(prompt, code_block):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": f"{prompt}. Code: {code_block},\n Please return the full modified code with all suggested changes incorporated."
            }
        ]
    )

    return completion.choices[0].message.content