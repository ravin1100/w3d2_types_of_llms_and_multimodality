"""
Tool implementations for the reasoning system.
This package contains mathematical and string manipulation tools.
"""

from .math_tools import calculate_average, calculate_square_root, compare_numbers
from .string_tools import count_vowels, count_letters, analyze_text

__all__ = [
    'calculate_average',
    'calculate_square_root',
    'compare_numbers',
    'count_vowels',
    'count_letters',
    'analyze_text'
] 