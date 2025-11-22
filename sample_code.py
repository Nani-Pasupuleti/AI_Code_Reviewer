"""
This module contains sample functions for AI code review analysis.
"""

# Define constants to avoid "magic numbers" and hardcoded strings
SIGNIFICANCE_THRESHOLD = 10
MSG_PROCESSING = "Processing data"
MSG_SIGNIFICANT = "Data is significant"

def my_function(a, b):
    """
    Calculates the sum of two numbers.
    
    Args:
        a (int): The first number.
        b (int): The second number.
        
    Returns:
        int: The result of adding a and b.
    """
    result = a + b
    return result

class UserData:
    """
    Represents user information.
    """
    def __init__(self, name):
        """
        Initializes the UserData instance.
        
        Args:
            name (str): The name of the user.
        """
        self.name = name

def another_function(data):
    """
    Processes data and checks if it exceeds the threshold.
    
    Args:
        data (int): The numerical data to process.
    """
    # Use the defined constant for the print message
    print(MSG_PROCESSING)
    
    # Use the constant instead of the hardcoded number 10
    if data > SIGNIFICANCE_THRESHOLD:
        # Use the defined constant for the print message
        print(MSG_SIGNIFICANT)

def bad_function():
    x=5 # Bad spacing and missing docstring
    print("Done")

    