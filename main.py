import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

from agents.code_fetcher import fetch_code_from_file
from agents.code_reviewer import review_code
from agents.report_generator import generate_review_report

def find_suitable_model():
    """
    Lists available Gemini models and prioritizes finding a known free model (Flash).
    """
    print("Finding a suitable model for your API key...")
    try:
        all_models = [m.name for m in genai.list_models()]
        
        # 1. Priority: Look for the standard Flash model (Best for free tier)
        for model in all_models:
            if 'gemini-1.5-flash' in model:
                print(f"Found preferred free model: {model}")
                return model

        # 2. Fallback: Look for any 'flash' model
        for model in all_models:
            if 'flash' in model:
                print(f"Found compatible flash model: {model}")
                return model

        # 3. Last Resort: Gemini 1.5 Pro
        for model in all_models:
            if 'gemini-1.5-pro' in model:
                print(f"Found fallback model: {model}")
                return model
        
        # If we get here, we hardcode a known working string to avoid grabbing experimental 2.5 models
        print("Using default fallback string.")
        return 'models/gemini-1.5-flash'

    except Exception as e:
        print(f"Could not list models: {e}")
        return 'models/gemini-1.5-flash'

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