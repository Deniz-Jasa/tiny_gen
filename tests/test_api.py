from fastapi.testclient import TestClient
from unittest.mock import patch
from your_application_file import app  # Update with the path to your FastAPI app

client = TestClient(app)

def test_base_url():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Deniz Jasarbasic's Implementation of the TinyGen API!"}

@patch('your_application_file.get_repo_files_as_string')
@patch('your_application_file.ask_chatgpt')
@patch('your_application_file.calculate_code_diff')
@patch('your_application_file.store')
def test_run_tiny_gen(mock_store, mock_calculate_code_diff, mock_ask_chatgpt, mock_get_repo_files_as_string):
    # Setup mock responses
    mock_get_repo_files_as_string.return_value = "Original code"
    mock_ask_chatgpt.return_value = "Modified code"
    mock_calculate_code_diff.return_value = "Diff"
    mock_store.return_value = None  # Assuming storing function returns nothing

    request_data = {
        "repoUrl": "https://github.com/example/repo",
        "prompt": "Please refactor the code for readability."
    }

    response = client.post("/run", json=request_data)
    assert response.status_code == 200
    assert "diff" in response.json()
    assert response.json()["diff"] == "Diff"

    # Verify mock interactions
    mock_get_repo_files_as_string.assert_called_with("https://github.com/example/repo")
    mock_ask_chatgpt.assert_called_with("Please refactor the code for readability.", "Original code")
    mock_calculate_code_diff.assert_called_with("Original code", "Modified code")
    mock_store.assert_called_once()
