import math

def calculate_average(*numbers):
    """Calculate the average of given numbers."""
    return sum(numbers) / len(numbers)

def calculate_square_root(number):
    """Calculate the square root of a number."""
    return math.sqrt(number)

def compare_numbers(a, b):
    """Compare two numbers and return the relationship."""
    if a > b:
        return f"{a} is greater than {b}"
    elif a < b:
        return f"{a} is less than {b}"
    else:
        return f"{a} is equal to {b}" 