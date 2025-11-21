# agents/code_reviewer.py
import google.generativeai as genai
import json

# The function now accepts a 'model_name' argument
def review_code(model_name, code_content):
    """
    Sends the code to a specified Google Gemini model for a review.
    """
    print(f"Sending code to Google AI for review using model: {model_name}...")
    
    prompt = f"""
    You are an automated AI Code Review Agent. Review the following Python code based on these standards:
    1.  **Code Formatting:** Proper indentation and spacing.
    2.  **Naming Conventions:** `snake_case` for variables and functions, `PascalCase` for classes.
    3.  **Function Comments/Docstrings:** Every function must have a docstring.
    4.  **Unused Variables:** No unused variables should be present.
    5.  **Hardcoded Values:** Avoid "magic numbers" or strings.

    Calculate a "Code Quality Score" from 100%, deducting points for each violation:
    - Minor formatting/naming issue: -5 points
    - Missing docstring: -10 points
    - Unused variable: -5 points
    - Hardcoded value: -5 points

    Your final output MUST be a JSON object with two keys: "suggestions" (a list of comments) and "score" (the final percentage).

    Code to review:
    ```python
    {code_content}
    ```
    """

    try:
        # Use the model name that was passed into the function
        model = genai.GenerativeModel(model_name)
        
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json"
        )

        response = model.generate_content(prompt, generation_config=generation_config)
        
        review_result = json.loads(response.text)
        print("AI review received successfully.")
        return review_result
        
    except Exception as e:
        print(f"Error calling Google AI API: {e}")
        return {
            "suggestions": [{"comment": f"An error occurred during AI analysis: {e}"}],
            "score": 0
        }