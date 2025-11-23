import os

def fetch_code_from_file(file_path):
    """
    Reads the content of a given file.
    
    Args:
        file_path (str): The path to the file to be read.
        
    Returns:
        str: The content of the file.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If the file cannot be read due to permissions.
        Exception: For other unexpected errors.
    """
    print(f"Fetching code from: {file_path}")
    
    # We allow the exceptions to bubble up to main.py
    # This fixes the "Return string starting with Error" issue
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()