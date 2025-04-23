import os
from dotenv import load_dotenv
import google.generativeai as genai
from movies_functions import functions_map, functions_description



def get_llm_model():
    # Load environment variables from .env file
    load_dotenv()
    # Access your API key
    api_key = os.getenv("GEMINI_API_KEY")
    # Configure the GenAI client
    genai.configure(api_key=api_key)
    # Create the model instance (you can use "gemini-pro", "gemini-1.5-pro", or "gemini-1.5-flash")
    model = genai.GenerativeModel("gemini-2.0-flash")
    return model

func_map = functions_map()
def function_caller(func_name, params):
    """Simple function caller that maps function names to actual functions"""
    if func_name in func_map:
        return func_map[func_name](params)
    else:
        return f"Function {func_name} not found"

max_iterations = 3
last_response = None
iteration = 0
iteration_response = []
model = get_llm_model()

system_prompt = f"""You are a math agent solving problems in iterations. Respond with EXACTLY ONE of these formats:
1. FUNCTION_CALL: python_function_name|input
2. FINAL_ANSWER: [number] . Also include the detailed explanation.

where python_function_name is one of the followin:
{functions_description()}
DO NOT include multiple responses. Give ONE response at a time."""

# query= """Calculate the sum of exponentials of word "TSAI"""
query= """Find the top 5 new released movies in netflix"""

while iteration < max_iterations:
    print(f"\n--- Iteration {iteration + 1} ---")
    if last_response == None:
        current_query = query
    else:
        current_query = current_query + "\n\n" + " ".join(iteration_response)
        current_query = current_query + "  What should I do next?"

    # Get model's response
    prompt = f"{system_prompt}\n\nQuery: {current_query}"
    # print(f"prompt: {prompt}")
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