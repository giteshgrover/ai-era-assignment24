import os
from dotenv import load_dotenv
import google.generativeai as genai
import math

def get_llm_model():
    # Load environment variables from .env file
    load_dotenv()
    # Access your API key
    api_key = os.getenv("GEMINI_API_KEY")
    # Configure the GenAI client
    genai.configure(api_key=api_key)
    # Create the model instance (you can use "gemini-pro", "gemini-1.5-pro", or "gemini-1.5-flash")
    model = genai.GenerativeModel("gemini-1.5-flash")
    return model

def strings_to_chars_to_int(string):
    return [ord(char) for char in string]

def int_list_to_exponential_sum(int_list):
    int_list = eval(int_list)
    return sum(math.exp(i) for i in int_list)

def fibonacci_numbers(n):
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]

def function_caller(func_name, params):
    """Simple function caller that maps function names to actual functions"""
    function_map = {
        "strings_to_chars_to_int": strings_to_chars_to_int,
        "int_list_to_exponential_sum": int_list_to_exponential_sum,
        "fibonacci_numbers": fibonacci_numbers
    }
    
    if func_name in function_map:
        return function_map[func_name](params)
    else:
        return f"Function {func_name} not found"

max_iterations = 3
last_response = None
iteration = 0
iteration_response = []
model = get_llm_model()

system_prompt = """You are a math agent solving problems in iterations. Respond with EXACTLY ONE of these formats:
1. FUNCTION_CALL: python_function_name|input
2. FINAL_ANSWER: [number] . Also include the detailed explanation.

where python_function_name is one of the followin:
1. strings_to_chars_to_int(string) It takes a word as input, and returns the ASCII INT values of characters in the word as a list
2. int_list_to_exponential_sum(list) It takes a list of integers and returns the sum of exponentials of those integers
3. fibonacci_numbers(int) It takes an integer, like 6, and returns first 6 integers in a fibonacci series as a list.
DO NOT include multiple responses. Give ONE response at a time."""

query= """Calculate the sum of exponentials of word "TSAI"""

while iteration < max_iterations:
    print(f"\n--- Iteration {iteration + 1} ---")
    if last_response == None:
        current_query = query
    else:
        current_query = current_query + "\n\n" + " ".join(iteration_response)
        current_query = current_query + "  What should I do next?"

    # Get model's response
    prompt = f"{system_prompt}\n\nQuery: {current_query}"
    # Generate content
    response = model.generate_content(prompt)
    
    response_text = response.text.strip()
    print(f"LLM Response: {response_text}")

    
    if response_text.startswith("FUNCTION_CALL:"):
        response_text = response.text.strip()
        _, function_info = response_text.split(":", 1)
        func_name, params = [x.strip() for x in function_info.split("|", 1)]
        iteration_result = function_caller(func_name, params)
    # Check if it's the final answer
    elif response_text.startswith("FINAL_ANSWER:"):
        print("\n=== Agent Execution Complete ===")
        break
        

    print(f"  Result: {iteration_result}")
    last_response = iteration_result
    iteration_response.append(f"In the {iteration + 1} iteration you called {func_name} with {params} parameters, and the function returned {iteration_result}.")

    iteration += 1