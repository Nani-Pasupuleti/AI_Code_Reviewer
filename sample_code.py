# This file has intentional errors for the AI to find.

import os

unused_variable = "I am not used"

def myfunc( a,b): # Bad formatting and bad name
    # Missing a docstring explaining the function
    result = a+b
    return result

class user_data: # Class name should be PascalCase (UserData)
    def __init__(self, name):
        self.name = name

def anotherFunction(data): # Should be snake_case (another_function)
    print("Processing data")
    if data > 10: # 10 is a "magic number"
        print("Data is significant")