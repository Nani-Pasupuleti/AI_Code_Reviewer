# main.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from agents.code_fetcher import fetch_code_from_file
from agents.code_reviewer import review_code
from agents.report_generator import generate_review_report

def find_suitable_model():
    """
    Lists available Gemini models and prioritizes finding a known free model.
    """
    print("Finding a suitable model for your API key...")
    try:
        # A list of preferred models known to be free
        preferred_models = [
            'models/gemini-1.5-flash-latest',
            'models/gemini-1.0-pro',
            'models/gemini-pro'
        ]
        
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

        for model_name in preferred_models:
            if model_name in all_models:
                print(f"Found preferred free model: {model_name}")
                return model_name

        # If no preferred models were found, return the first available one as a fallback
        if all_models:
            print(f"No preferred models found. Using first available: {all_models[0]}")
            return all_models[0]
            
        return None
    except Exception as e:
        print(f"Could not list models: {e}")
        return None

def main():
    try:
        # 1. Configure the Google AI Client
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            print("Error: GOOGLE_API_KEY not found in .env file.")
            return
        genai.configure(api_key=google_api_key)

        # 2. Find a working model dynamically
        model_name = find_suitable_model()
        if not model_name:
            print("\nError: Could not find any compatible models for your API key.")
            return
            
        # 3. Fetch the code
        file_to_review = "sample_code.py"
        code_to_review = fetch_code_from_file(file_to_review)
        
        if "Error:" in code_to_review:
            print(code_to_review)
            return

        # 4. Get the AI review, passing the found model name
        review_result = review_code(model_name, code_to_review)

        # 5. Generate and print the report
        final_report = generate_review_report(review_result)
        print(final_report)

    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")

if __name__ == "__main__":
    main()