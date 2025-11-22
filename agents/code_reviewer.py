import google.generativeai as genai
import json
import re

def review_code(model_name, code_content, filename):
    """
    Sends the code to a specified Google Gemini model for a review.
    Dynamically adapts to the programming language based on filename.
    """
    print(f"Sending {filename} to Google AI for review using model: {model_name}...")
    
    prompt = f"""
    You are an Expert Senior Software Architect and Code Reviewer. 
    You are reviewing a file named: '{filename}'.

    Your task is to analyze the code below.
    1. **Detect the Language:** Identify if this is Python, Java, JavaScript (React), SQL, etc.
    2. **Apply Language-Specific Standards:** 
       - If Python: Check for PEP 8, snake_case naming.
       - If Java/C#: Check for camelCase naming, proper class structure.
       - If JavaScript/React: Check for functional components, hooks usage, const/let variables.
       - If SQL: Check for capitalization of keywords, injection risks.
    3. **Analyze for:**
       - Bugs or Logic Errors.
       - Security Vulnerabilities (e.g., SQL Injection, Hardcoded Secrets).
       - Code Cleanliness & Maintainability.
       - Missing Documentation/Comments.

    Calculate a "Code Quality Score" (0-100%).
    
    Your output MUST be a raw JSON object with two keys: 
    - "suggestions": A list of objects, where each has a "comment" field.
    - "score": The final percentage as a number (integer).

    Do not include Markdown formatting like ```json.

    Code to review:
    ```
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

        # Handle double-encoding
        if isinstance(review_result, str):
            review_result = json.loads(review_result)

        print("AI review received successfully.")
        return review_result
        
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return {
            "suggestions": [{"comment": f"AI returned invalid format or failed: {e}"}],
            "score": 0
        }