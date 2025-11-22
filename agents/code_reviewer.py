import google.generativeai as genai
import json
import re

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

    Your final output MUST be a raw JSON object with two keys: "suggestions" (a list of comments) and "score" (the final percentage).
    Do not include Markdown formatting like ```json.

    Code to review:
    ```python
    {code_content}
    ```
    """

    try:
        model = genai.GenerativeModel(model_name)
        
        # Send request
        response = model.generate_content(prompt)
        text_response = response.text.strip()

        # CLEANUP: Remove Markdown code blocks if present
        if text_response.startswith("```"):
            text_response = re.sub(r"^```(json)?|```$", "", text_response, flags=re.MULTILINE).strip()

        # Parse JSON
        review_result = json.loads(text_response)

        # Handle case where AI returns a string representation of JSON inside JSON (rare but happens)
        if isinstance(review_result, str):
            review_result = json.loads(review_result)

        print("AI review received successfully.")
        return review_result
        
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        # Return a valid structure so the program doesn't crash
        return {
            "suggestions": [{"comment": f"AI returned invalid format. Error: {e}"}],
            "score": 0
        }