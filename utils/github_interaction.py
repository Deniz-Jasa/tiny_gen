from github import Github
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
github_token = os.environ['GITHUB_TOKEN']

def is_binary_string(bytes_data):
    """
    Checks if the given bytes data represents a binary string.
    """
    text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    return bool(bytes_data.translate(None, text_characters))

def get_repo_files_as_string(repo_url: str):
    g = Github(github_token)
    
    # Extract the repository's full name (user/repo) from the URL
    repo_name = repo_url.rstrip('/').split('/')[-2] + '/' + repo_url.rstrip('/').split('/')[-1]
    
    repo = g.get_repo(repo_name)
    contents = repo.get_contents("")
    
    repo_code = ""

    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            # Skip README.md files
            if file_content.name.lower().startswith('readme'):
                continue

            # Check if the content is binary
            if file_content.encoding == 'base64' and is_binary_string(base64.b64decode(file_content.content)):
                # Handle binary files differently if needed
                continue
            else:
                # Decode and append file content to repo_code
                content = file_content.decoded_content.decode('utf-8')
                repo_code += content + "\n\n"  # Separate files with newlines
    
    return repo_code.strip()  # Strip trailing newline
