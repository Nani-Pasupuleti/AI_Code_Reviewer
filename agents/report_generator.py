def generate_review_report(review_data):
    """
    Formats the AI review data into a printable report.
    
    Args:
        review_data (dict): The dictionary containing suggestions and score.
        
    Returns:
        str: A formatted string report.
    """
    print("Generating final report...")
    score = review_data.get('score', 0)
    suggestions = review_data.get('suggestions', [])
    
    report = "\n" + "="*50 + "\n"
    report += "          AI CODE REVIEW REPORT\n"
    report += "="*50 + "\n\n"
    report += f"FINAL SCORE: {score}%\n\n"
    report += "--- SUGGESTIONS ---\n"
    
    if not suggestions:
        report += "Excellent! No issues found.\n"
    else:
        for i, suggestion in enumerate(suggestions, 1):
            report += f"\n{i}. {suggestion.get('comment', 'No comment provided.')}\n"
            
    report += "\n" + "="*50 + "\n"
    return report