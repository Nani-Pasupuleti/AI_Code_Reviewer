import google.generativeai as genai
import json
import re

def review_code(model_name, code_content, filename):
    """
    Sends the code to a specified Google Gemini model for a review.
    Enforces Company Standards (Strict for App Code, Pythonic for Scripts).
    """
    print(f"Sending {filename} to Google AI for review using model: {model_name}...")
    
    prompt = f"""
    You are an Expert Senior Software Architect and Code Reviewer. 
    You are reviewing a file named: '{filename}'.

    Your goal is to enforce strict COMPANY STANDARDS.

    --- CODING STANDARDS ---
    
    1. **Naming Conventions (Language Specific):**
       - **Java / JavaScript / React:** 
         - Classes: `PascalCase`
         - Variables/Methods: `camelCase` (e.g., `userList`, `getData`)
       - **Python:** 
         - Classes: `PascalCase`
         - Variables/Methods: `snake_case` (e.g., `user_list`, `get_data`)
       - Constants (All): `UPPER_SNAKE_CASE`

    2. **Code Structure & Complexity:**
       - **Method Length:** Strictly ≤ 40 lines.
       - **Nesting:** Max depth 3 levels.
       - **No Hardcoding:** Use config/constants.
       - **Logs:** 
         - Frontend: Use `utils.log()`, NOT `console.log`.
         - Backend: Use Logger (SLF4J), NOT `System.out.println`.
         - Python Scripts: `print()` is allowed ONLY for CLI tools.

    3. **Tech Stack Specifics:**
       - **Spring Boot:** No `new Service()`. Use Dependency Injection.
       - **React:** Use `const` over `var`. Lists must have `keys`.
       - **SQL:** Keywords UPPERCASE. No concatenation (Injection risk).

    4. **Security:**
       - NO hardcoded passwords, tokens, or API keys.

    --- SCORING ---
    Start at 100%. Deduct:
    - **Critical (-20):** Security risks.
    - **Major (-10):** Logic errors, DB loops, Var in React.
    - **Medium (-5):** Bad naming, Hardcoding, Logging violations.

    Your output MUST be a raw JSON object with two keys: 
    - "suggestions": A list of objects, where each has a "comment" field.
    - "score": The final percentage as a number (integer).

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

        # Handle Lists vs Dictionaries (Crash Proofing)
        if isinstance(review_result, list):
            return { "suggestions": review_result, "score": 0 }
        
        if not isinstance(review_result, dict):
            return { "suggestions": [{"comment": "AI returned invalid JSON format."}], "score": 0 }

        print("AI review received successfully.")
        return review_result
        
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return { "suggestions": [{"comment": f"AI returned invalid format: {e}"}], "score": 0 }