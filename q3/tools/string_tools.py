def count_vowels(text):
    """Count the number of vowels in a text."""
    vowels = 'aeiouAEIOU'
    return sum(1 for char in text if char in vowels)

def count_letters(text):
    """Count the number of letters in a text."""
    return sum(1 for char in text if char.isalpha())

def analyze_text(text):
    """Analyze text and return various metrics."""
    return {
        'vowels': count_vowels(text),
        'letters': count_letters(text),
        'length': len(text)
    } 