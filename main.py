import os
import sys
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
        
        # 1. Priority: Look for the standard Flash model
        for model in all_models:
            if 'gemini-1.5-flash' in model:
                print(f"Found preferred free model: {model}")
                return model

        # 2. Fallback: Look for any 'flash' model
        for model in all_models:
            if 'flash' in model:
                print(f"Found compatible flash model: {model}")
                return model
        
        # 3. Last Resort: Pro model
        return 'models/gemini-1.5-flash'

    except Exception as e:
        print(f"Could not list models: {e}")
        return 'models/gemini-1.5-flash'

def main():
    try:
        # 1. Configure the Google AI Client
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            print("Error: GOOGLE_API_KEY not found in environment variables.")
            return
        genai.configure(api_key=google_api_key)

        # 2. Find a working model dynamically
        model_name = find_suitable_model()
        if not model_name:
            print("\nError: Could not find any compatible models for your API key.")
            return
            
        # 3. Fetch the code
        # If GitHub Actions sends a filename, use it. Otherwise, default to sample_code.py (for local testing)
        if len(sys.argv) > 1:
            file_to_review = sys.argv[1]
        else:
            file_to_review = "sample_code.py"

        print(f"--- Starting Review for: {file_to_review} ---")
        code_to_review = fetch_code_from_file(file_to_review)
        
        if "Error:" in code_to_review:
            print(code_to_review)
            sys.exit(1) 

        # 4. Get the AI review (Passing Filename now!)
        review_result = review_code(model_name, code_to_review, file_to_review)

        # 5. Generate and print the report
        final_report = generate_review_report(review_result)
        print(final_report)

        # 6. Fail the pipeline if the score is low
        score = review_result.get('score', 0)
        try:
            score_int = int(str(score).replace('%', ''))
            if score_int < 70:
                print("❌ FAILED: Code Quality Score is below 70%.")
                sys.exit(1)
        except:
            pass 

    except Exception as e:
        print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()