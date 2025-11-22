def generate_review_report(review_data):
    """
    Formats the AI review data into a printable report.
    Handles both Dictionary and String formats for suggestions.
    """
    print("Generating final report...")
    
    report = "\n" + "="*50 + "\n"
    report += "          AI CODE REVIEW REPORT\n"
    report += "="*50 + "\n\n"

    # 1. Safety Check: If the entire review_data is a string (Critical Failure)
    if isinstance(review_data, str):
        report += "⚠️  WARNING: RAW AI OUTPUT RECEIVED\n"
        report += "The AI did not return valid JSON.\n\n"
        report += f"{review_data}\n"
        report += "="*50 + "\n"
        return report

    # 2. Get Score
    score = review_data.get('score', 'N/A')
    report += f"FINAL SCORE: {score}%\n\n"
    report += "--- SUGGESTIONS ---\n"
    
    # 3. Get Suggestions
    suggestions = review_data.get('suggestions', [])
    
    if not suggestions:
        report += "Excellent! No issues found.\n"
    else:
        for i, suggestion in enumerate(suggestions, 1):
            # FIX: Check if the suggestion is just a simple text string
            if isinstance(suggestion, str):
                report += f"\n{i}. {suggestion}\n"
            else:
                # It is a dictionary, so use .get()
                comment = suggestion.get('comment', 'No comment provided.')
                report += f"\n{i}. {comment}\n"
            
    report += "\n" + "="*50 + "\n"
    return report