# Tool-Enhanced Reasoning System

This project demonstrates a tool-enhanced reasoning system using Google's Gemini 1.5 Flash model. The system can interpret natural language queries, use chain-of-thought reasoning, and leverage various tools to provide accurate answers.

## Features

- Chain-of-thought (CoT) reasoning using Gemini 1.5 Flash
- Tool integration for mathematical and string operations
- Interactive command-line interface
- Structured output showing reasoning steps and tool usage

## Project Structure

```
q3/
├── main.py              # Main script with LLM integration and query processing
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (API keys)
├── .env.example        # Example environment file
├── .gitignore         # Git ignore patterns
├── README.md          # Project documentation
└── tools/             # Tool implementations
    ├── __init__.py    # Package initializer
    ├── math_tools.py  # Mathematical operations
    └── string_tools.py # String manipulation functions
```

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ravin1100/w3d2_types_of_llms_and_multimodality.git
cd q3
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Copy `.env.example` to `.env`
   - Add your Google API key to the `.env` file:
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

## Usage

Run the script using:
```bash
python main.py
```

The script provides an interactive interface where you can:
1. Try example queries
2. Enter your own queries
3. Exit the program

## Example Queries and Output

Here are some example queries and their output:

1. **Query**: "What's the square root of the average of 18 and 50?"
   ```
   Reasoning: Need to calculate average first, then find square root
   Tools Used: calculate_average, calculate_square_root
   Final Answer: The square root of the average of 18 and 50 is 5.83
   ```

2. **Query**: "How many vowels are in the word 'Multimodality'?"
   ```
   Reasoning: Need to count vowels in the given word
   Tools Used: count_vowels
   Final Answer: The word 'Multimodality' contains 5 vowels
   ```

3. **Query**: "Is the number of letters in 'machine' greater than the number of vowels in 'reasoning'?"
   ```
   Reasoning: Need to count letters and vowels, then compare
   Tools Used: count_letters, count_vowels, compare_numbers
   Final Answer: Yes, 'machine' has 7 letters which is greater than the 3 vowels in 'reasoning'
   ```

4. **Query**: "What's the total number of characters in 'artificial' plus the number of vowels in 'intelligence'?"
   ```
   Reasoning: Need to count string length and vowels, then add
   Tools Used: analyze_text, count_vowels
   Final Answer: The total is 14 (9 characters + 5 vowels)
   ```

5. **Query**: "Is the square root of 100 greater than the number of consonants in 'programming'?"
   ```
   Reasoning: Need square root and consonant count for comparison
   Tools Used: calculate_square_root, analyze_text
   Final Answer: No, square root of 100 (10) is not greater than the consonants in 'programming' (7)
   ```

## Prompt Design for Tool Usage

The system uses a structured prompt that helps the LLM decide when and how to use tools:

1. **Understanding Phase**: The prompt first asks for a clear understanding of the query
2. **Tool Identification**: It explicitly asks if tools are needed and which ones
3. **Execution Planning**: Requires a step-by-step plan for solving the query
4. **Parameter Specification**: Asks for clear identification of tool parameters

The prompt is designed to output in a parseable format with clear markers:
- UNDERSTANDING: [explanation]
- NEEDS_TOOLS: [yes/no]
- TOOLS_REQUIRED: [tool list]
- PARAMETERS: [parameter list]
- EXECUTION_PLAN: [steps]

This structured format ensures consistent and reliable tool usage decisions.

## Available Tools

### Math Tools
- `calculate_average`: Calculate average of numbers
- `calculate_square_root`: Find square root
- `compare_numbers`: Compare two numbers

### String Tools
- `count_vowels`: Count vowels in text
- `count_letters`: Count letters in text
- `analyze_text`: Get various text metrics

## Contributing

Feel free to submit issues and enhancement requests! 