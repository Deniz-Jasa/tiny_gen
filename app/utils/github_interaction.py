from github import Github
import base64
import os
from dotenv import load_dotenv

load_dotenv()
github_token = os.environ['GITHUB_TOKEN']

def is_binary_string(bytes_data):
    """
    Determines if the provided bytes data represents a binary string. Helper function used to skip binary files.
    
    Parameters:
    - bytes_data (bytes): The bytes data to check.

    Returns:
    - bool: True if the bytes_data represents a binary string; False otherwise.
    """
    text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
    return bool(bytes_data.translate(None, text_characters))


def get_repo_files_as_string(repo_url: str):
    """
    Retrieves the contents of a repository from the given repository URL and returns it as a string.
    
    Parameters:
    - repo_url (str): The URL of the repository from which files will be retrieved.
    
    Returns:
    - str: A string representation of the repository files' contents.
    
    """
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
            # Check if the content is binary, skip!
            try:
                if file_content.encoding == 'base64' and is_binary_string(base64.b64decode(file_content.content)):
                    continue
                
                content = file_content.decoded_content.decode('utf-8')
                file_name = file_content.path
                repo_code += f"File {file_name}:\n{content}\n\n"
                
            except Exception as e:
                print(f"Error processing file {file_content.path}: {e}")
    
    return repo_code.strip()