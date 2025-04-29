import os
from dotenv import load_dotenv
import google.generativeai as genai
from movies_functions import functions_map, functions_description
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    query: str

class MovieResponse(BaseModel):
    movies: List[dict]

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
def function_caller(func_name, *args):
    """Simple function caller that maps function names to actual functions"""
    if func_name in func_map:
        return func_map[func_name](*args)
    else:
        return f"Function {func_name} not found"

def process_movie_query(query: str) -> str:
    max_iterations = 5
    last_response = None
    iteration = 0
    iteration_response = []
    model = get_llm_model()

    system_prompt = f"""You are a agent solving problems in iterations. Respond with EXACTLY ONE of these formats:
    1. FUNCTION_CALL: python_function_name||inputParam1|inputParam2|inputParam3 ...
    2. FINAL_ANSWER: [movie title (releaseYear) - IMDB rating - streaming links].

    where python_function_name is one of the following:
    {functions_description()}
    DO NOT include multiple responses. Give ONE response at a time."""

    while iteration < max_iterations:
        if last_response is None:
            current_query = query
        else:
            current_query = current_query + "\n\n" + " ".join(iteration_response)
            current_query = current_query + "  What function should I call next? Respond exactly in the one of two formats suggested above"

        prompt = f"{system_prompt}\n\nQuery: {current_query}"
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        if response_text.startswith("FUNCTION_CALL:"):
            _, function_info = response_text.split(":", 1)
            func_details = [x.strip() for x in function_info.split("||")]
            func_name = func_details[0]
            params = [x.strip() for x in func_details[1].split("|")]
            iteration_result = function_caller(func_name, *params)
        elif response_text.startswith("FINAL_ANSWER:"):
            return response_text.replace("FINAL_ANSWER:", "").strip()

        iteration_response.append(f"In the {iteration + 1} iteration you called {func_name} with {params} parameters, and the function returned {iteration_result}.")
        last_response = iteration_result
        iteration += 1

    return "Maximum iterations reached without finding a final answer."

def parse_movie_info(movie_str: str) -> dict:
    """Parse a single movie string into a structured dictionary"""
    parts = movie_str.split(" - ")
    if len(parts) >= 3:
        title_year = parts[0].strip()
        rating = parts[1].strip()
        streaming_links = [link.strip() for link in parts[2].split(",")]
        
        # Extract title and year
        title = title_year.split("(")[0].strip()
        year = title_year.split("(")[1].split(")")[0].strip()
        
        return {
            "title": title,
            "year": year,
            "rating": rating,
            "streaming_links": streaming_links
        }
    return None

@app.post("/query", response_model=MovieResponse)
async def handle_query(request: QueryRequest):
    try:
        result = process_movie_query(request.query)
        print(f"result: {result}")
        
        # Split the result into individual movies
        movies = [movie.strip() for movie in result.split("\n") if movie.strip()]
        
        # Parse each movie
        parsed_movies = []
        for movie_str in movies:
            movie_info = parse_movie_info(movie_str)
            if movie_info:
                parsed_movies.append(movie_info)
        
        if not parsed_movies:
            raise HTTPException(status_code=400, detail="No valid movies found in response")
            
        return MovieResponse(movies=parsed_movies)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)