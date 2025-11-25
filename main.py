import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv() # to load values from .env

from agents.code_fetcher import fetch_code_from_file
from agents.code_reviewer import review_code
from agents.report_generator import generate_review_report

# Constants to avoid "Magic Numbers"
MIN_PASS_SCORE = 70
DEFAULT_MODEL_NAME = 'models/gemini-1.5-flash'

def find_suitable_model():
    """
    Lists available Gemini models and prioritizes finding a known free model (Flash).
    
    Returns:
        str: The name of the best available model.
    """
    print("Finding a suitable model for your API key...")
    try:
        all_models = [m.name for m in genai.list_models()]
        
        # 1. Priority: Look for the standard Flash model (Exact match preferred)
        target_model = 'models/gemini-1.5-flash'
        if target_model in all_models:
            print(f"Found preferred free model: {target_model}")
            return target_model

        # 2. Fallback: Look for any 'flash' model using safer checking
        for model in all_models:
            if 'flash' in model and 'gemini' in model:
                print(f"Found compatible flash model: {model}")
                return model
        
        # 3. Last Resort: Default Flash model
        return DEFAULT_MODEL_NAME

    except Exception as e:
        print(f"Could not list models: {e}")
        return DEFAULT_MODEL_NAME

def main():
    """
    Main entry point for the AI Code Reviewer.
    Orchestrates fetching code, sending it to AI, and generating reports.
    """
    try:
        # 1. Configure the Google AI Client
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            print("Error: GOOGLE_API_KEY not found in environment variables.")
            return
        genai.configure(api_key=google_api_key) # package(google.generativeai)  already contains a method called configure().

        # 2. Find a working model dynamically
        model_name = find_suitable_model()
        if not model_name:
            print("\nError: Could not find any compatible models for your API key.")
            return
            
        # 3. Determine the file to review
        if len(sys.argv) > 1:
            file_to_review = sys.argv[1] # command-line arguments
        else:
            file_to_review = "main.py" # Review itself if no file provided

        print(f"--- Starting Review for: {file_to_review} ---")

        # 4. Fetch the code (Now handling Exceptions properly)
        try:
            code_to_review = fetch_code_from_file(file_to_review)
        except FileNotFoundError:
            print(f"Error: The file '{file_to_review}' was not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: An unexpected error occurred while reading file: {e}")
            sys.exit(1)

        # 5. Get the AI review
        review_result = review_code(model_name, code_to_review, file_to_review)

        # 6. Generate and print the report
        final_report = generate_review_report(review_result)
        print(final_report)

        # 7. Fail the pipeline if the score is low
        score = review_result.get('score', 0)
        
        # Fix: Proper error handling for score conversion
        try:
            score_str = str(score).replace('%', '').strip()
            score_int = int(score_str)
            
            if score_int < MIN_PASS_SCORE:
                print(f"❌ FAILED: Code Quality Score ({score_int}%) is below {MIN_PASS_SCORE}%.")
                sys.exit(1)
                
        except ValueError:
            print(f"Warning: Could not parse score '{score}'. Skipping threshold check.")

    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()