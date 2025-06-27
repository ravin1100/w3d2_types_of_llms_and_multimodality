import os
from dotenv import load_dotenv
import google.generativeai as genai
from tools.math_tools import calculate_average, calculate_square_root, compare_numbers
from tools.string_tools import count_vowels, count_letters, analyze_text
import sys

# Load environment variables
load_dotenv()

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Check if API key is available
if not GOOGLE_API_KEY:
    print("Error: GOOGLE_API_KEY not found in .env file")
    print("Please make sure you have:")
    print("1. Created a .env file in the project root")
    print("2. Added your Gemini API key as: GOOGLE_API_KEY=your_api_key_here")
    sys.exit(1)

try:
    genai.configure(api_key=GOOGLE_API_KEY)
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Test the configuration with a simple generation
    model.generate_content("Test")
except Exception as e:
    print("Error initializing Gemini API:")
    print(str(e))
    print("\nPlease make sure:")
    print("1. Your API key is valid")
    print("2. You have internet connectivity")
    print("3. The API service is available")
    sys.exit(1)

def create_prompt(query):
    return f"""Analyze the following query and determine which tools to use from our available toolset.

Available tools:
1. count_vowels(text): Counts the number of vowels in a text
2. count_letters(text): Counts the number of letters in a text
3. analyze_text(text): Returns vowels, letters, and length metrics
4. calculate_average(*numbers): Calculates average of numbers
5. calculate_square_root(number): Calculates square root
6. compare_numbers(a, b): Compares two numbers

Query: {query}

You MUST use the following format in your response:
UNDERSTANDING: Write a brief explanation of what the query is asking for.
NEEDS_TOOLS: Write 'yes' if we need to use any tools, 'no' if not.
TOOLS_REQUIRED: List the exact tool names needed, separated by commas (e.g., count_vowels, analyze_text)
PARAMETERS: List the exact parameters to pass to each tool (e.g., devendra)
EXECUTION_PLAN: List the steps to solve this query using the tools.

For text analysis queries, ALWAYS use our tools instead of explaining how to implement the logic.
For math queries, ALWAYS use our calculator tools instead of explaining the math."""

def parse_llm_response(response):
    """Parse the LLM response to extract key information."""
    text = response.text
    
    # Extract key information using simple text parsing
    understanding = text.split('UNDERSTANDING:')[1].split('NEEDS_TOOLS:')[0].strip()
    needs_tools = 'yes' in text.split('NEEDS_TOOLS:')[1].split('TOOLS_REQUIRED:')[0].strip().lower()
    tools_required = text.split('TOOLS_REQUIRED:')[1].split('PARAMETERS:')[0].strip()
    parameters = text.split('PARAMETERS:')[1].split('EXECUTION_PLAN:')[0].strip()
    execution_plan = text.split('EXECUTION_PLAN:')[1].strip()
    
    return {
        'understanding': understanding,
        'needs_tools': needs_tools,
        'tools_required': [t.strip() for t in tools_required.split(',') if t.strip()],
        'parameters': parameters,
        'execution_plan': execution_plan
    }

def execute_tool_call(tool_name, parameters):
    """Execute the appropriate tool based on the tool name and parameters."""
    # Clean parameters string and extract values
    params = [p.strip() for p in parameters.split(',')]
    
    if tool_name == 'calculate_average':
        numbers = [float(n) for n in params]
        return calculate_average(*numbers)
    elif tool_name == 'calculate_square_root':
        return calculate_square_root(float(params[0]))
    elif tool_name == 'count_vowels':
        return count_vowels(params[0])
    elif tool_name == 'count_letters':
        return count_letters(params[0])
    elif tool_name == 'compare_numbers':
        return compare_numbers(float(params[0]), float(params[1]))
    elif tool_name == 'analyze_text':
        return analyze_text(params[0])
    else:
        raise ValueError(f"Unknown tool: {tool_name}")

def process_query(query):
    """Process a natural language query using the LLM and tools."""
    print(f"\nProcessing query: {query}")
    print("-" * 50)
    
    # Get LLM's reasoning
    response = model.generate_content(create_prompt(query))
    parsed_response = parse_llm_response(response)
    
    print("\nReasoning:")
    print(parsed_response['understanding'])
    print("\nExecution Plan:")
    print(parsed_response['execution_plan'])
    
    # Execute tools if needed
    if parsed_response['needs_tools']:
        print("\nUsing tools:", ", ".join(parsed_response['tools_required']))
        results = []
        for tool in parsed_response['tools_required']:
            result = execute_tool_call(tool, parsed_response['parameters'])
            results.append(result)
            print(f"Tool {tool} result:", result)
    else:
        print("\nNo tools needed.")
        results = []
    
    # Get final answer from LLM
    final_prompt = f"""Based on the original query: {query}
    And the tool results: {results}
    Provide a clear and concise final answer."""
    
    final_response = model.generate_content(final_prompt)
    print("\nFinal Answer:")
    print(final_response.text)

def main():
    # Example queries
    example_queries = [
        "What's the square root of the average of 18 and 50?",
        "How many vowels are in the word 'Multimodality'?",
        "Is the number of letters in 'machine' greater than the number of vowels in 'reasoning'?"
    ]
    
    print("Tool-Enhanced Reasoning System")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Try an example query")
        print("2. Enter your own query")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            print("\nExample queries:")
            for i, query in enumerate(example_queries, 1):
                print(f"{i}. {query}")
            query_choice = int(input("\nChoose a query (1-3): ")) - 1
            if 0 <= query_choice < len(example_queries):
                process_query(example_queries[query_choice])
        elif choice == '2':
            query = input("\nEnter your query: ")
            process_query(query)
        elif choice == '3':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main() 