import google.generativeai as genai
import json
import re

def review_code(model_name, code_content, filename):
    """
    Sends the code to a specified Google Gemini model for a review.
    Enforces Company Standards + Industry Best Practices (Complexity, Security, Performance).
    """
    print(f"Sending {filename} to Google AI for review using model: {model_name}...")
    
    prompt = f"""
    You are an Expert Senior Software Architect and Code Reviewer. 
    You are reviewing a file named: '{filename}'.

    Your goal is to enforce strict COMPANY STANDARDS and INDUSTRY BEST PRACTICES.

    --- CODING STANDARDS & BEST PRACTICES ---
    
    1. **Naming Conventions:**
       - Classes: MUST use `PascalCase`.
       - Variables, Methods, Functions: MUST use `camelCase`.
       - Constants: MUST use `UPPER_SNAKE_CASE`.
       - Meaningful names: Avoid `x`, `temp`, `data` (unless generic).

    2. **Code Structure & Complexity (Critical):**
       - **Method Length:** Strictly ≤ 40 lines. Suggest refactoring if longer.
       - **Nesting:** Avoid deep nesting (e.g., `if` inside `if` inside `for`). Max depth: 3.
       - **No Hardcoding:** Use config files/constants. No "Magic Numbers" or hardcoded strings.
       - **DRY Principle:** Detect repeated logic and suggest creating a helper function.

    3. **Backend (Java/Spring Boot) Specifics:**
       - **Dependency Injection:** Use `@Autowired` or Constructor Injection. NEVER use `new Service()` inside a controller/service.
       - **Logging:** Use SLF4J/Log4j. DO NOT use `System.out.println`.
       - **Exception Handling:** Do not catch generic `Exception`. Catch specific exceptions. Never leave a catch block empty.
       - **Database:** NEVER perform a DB query inside a loop (N+1 Problem).

    4. **Frontend (React/JS/PPM) Specifics:**
       - **API Calls:** Must be in service files, not inside UI components.
       - **Logging:** Use `utils.log()`. DO NOT use `console.log`.
       - **React Best Practices:**
         - Ensure lists have unique `key` props.
         - Verify `useEffect` dependency arrays are correct.
         - Use `const` (immutable) over `let` or `var`.
       - **Components:** Logic should be broken into small, reusable components.

    5. **Security:**
       - **SQL Injection:** Ensure parameters are bound, no string concatenation in queries.
       - **Secrets:** Fail immediately if passwords, tokens, or keys are found.
       - **Data Exposure:** Sensitive data must be masked before sending to UI.

    --- SCORING RUBRIC ---
    Calculate a "Code Quality Score" (0-100%). Start at 100% and deduct:
    - **Critical (-20):** Security risks (Passwords, SQL Injection).
    - **Major (-10):** Logic errors, DB queries in loops, `new Service()` in Spring.
    - **Medium (-5):** Hardcoded values, `console.log`, `System.out.println`, methods > 40 lines.
    - **Minor (-2):** Naming conventions, missing comments.

    --- OUTPUT FORMAT ---
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

        # Handle Lists vs Dictionaries (Crash Proofing)
        if isinstance(review_result, list):
            print("⚠️ Warning: AI returned a List instead of an Object. Fixing structure...")
            return {
                "suggestions": review_result,
                "score": 0 
            }
        
        # Ensure it is a dictionary before returning
        if not isinstance(review_result, dict):
            return {
                "suggestions": [{"comment": "AI returned invalid JSON format."}],
                "score": 0
            }

        print("AI review received successfully.")
        return review_result
        
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        return {
            "suggestions": [{"comment": f"AI returned invalid format or failed: {e}"}],
            "score": 0
        }