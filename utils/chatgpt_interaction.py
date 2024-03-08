import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

def run_intial_suggestion(prompt, original_code):
    completion = client.completions.create(
        model="text-davinci-003",
        prompt=prompt + "\n\nCode:\n" + original_code,
        max_tokens=1500,  # Adjust max_tokens as needed for your code block size
        temperature=0.7,  # Adjust temperature for creativity vs. conservatism
        stop=["\n\n"]  # Ensure that GPT returns the full code back
    )

    modified_code = completion.choices[0].text.strip().split("\n\n")[-1]

    return modified_code