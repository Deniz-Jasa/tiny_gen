import os
import cohere
from dotenv import load_dotenv

load_dotenv()

# Initialize Cohere client
cohere_client = cohere.Client(os.environ['COHERE_API_KEY'])

def modify_code(prompt, code_block):
    """
    Sends a task and code block to Cohere, returning a modified version of the code and PR description.
    """
    try:
        full_prompt = (
            "Goal:\n"
            f"{prompt}\n\n"
            "Return Format:\n"
            "You MUST format your response EXACTLY like this:\n\n"
            "MODIFIED_FILES:\n"
            "File <filename>:\n"
            "<complete file content with your changes>\n\n"
            "PR_DESCRIPTION:\n"
            "<brief description of your changes>\n\n"
            "Warnings:\n"
            "- Start with exactly 'MODIFIED_FILES:'\n"
            "- Follow with 'File <filename>:' for each modified file\n"
            "- End with exactly 'PR_DESCRIPTION:' and your description\n"
            "- Make ONLY the specific changes requested in the prompt\n"
            "- Do NOT modify any other content\n"
            "- Do NOT remove or change existing images or links\n"
            "- Keep all existing formatting and structure\n"
            "- Preserve all other content exactly as is\n\n"
            "Context:\n"
            f"Current content:\n{code_block}\n\n"
            "Make only the minimal changes needed to fulfill the prompt request."
        )
        
        print("Sending prompt to Cohere...")
        
        response = cohere_client.generate(
            prompt=full_prompt,
            model='command',
            max_tokens=1024,
            temperature=0.1,
        )
        
        if not response or not response.generations:
            raise Exception("No response received from Cohere")
        
        result = response.generations[0].text.strip()
        print(f"AI response starts with: {result[:100]}")  # Debug log
        
        # Split response into files and PR description
        parts = result.split('PR_DESCRIPTION:')
        if len(parts) != 2 or 'MODIFIED_FILES:' not in parts[0]:
            raise Exception("AI response not in correct format")
            
        files_part = parts[0].replace('MODIFIED_FILES:', '').strip()
        pr_description = parts[1].strip()
        
        return {
            'modified_files': files_part,
            'pr_description': pr_description
        }
        
    except Exception as e:
        print(f"Error in modify_code: {str(e)}")
        raise Exception(f"Failed to get AI response: {str(e)}")
