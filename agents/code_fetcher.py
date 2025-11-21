def fetch_code_from_file(file_path):
    """
    Reads the content of a given file.
    
    Args:
        file_path (str): The path to the file to be read.
        
    Returns:
        str: The content of the file, or an error message if it fails.
    """
    print(f"Fetching code from: {file_path}")
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: The file was not found."
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}"