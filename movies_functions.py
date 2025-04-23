import requests
import os
import ast
from dotenv import load_dotenv
from imdb import Cinemagoer

def functions_description():
    return """
1. check_new_movies_added(string) It takes a popular streaming platform name (such as netflix, prime, peacock, hulu) as input and It gets the newly added movies in that streaming platform and returns a list of movie titles
2. check_ratings(list) It takes a list of movie titles of type string and returns a dictionary whose keys are the movie titles and values are the float ratings
3. sort_by_ratings(dict) It takes a dictionary whose keys are whose keys are the movie titles and values are the float ratings and returns another dictionary sorted by the rating values.
4. select_top_movies(list, top_n) It takes the list of movie titles and the top n number and returns the first n values of the list 
"""

def functions_map():
    return {
        "check_new_movies_added": check_new_movies_added,
        "check_ratings": check_ratings,
        "sort_by_ratings": sort_by_ratings,
        "select_top_movies": select_top_movies
    }

def check_new_movies_added(catalog):
    # Call Netflix
    # Call Prime
    rapid_api_key = os.getenv("RAPID_API_KEY")
    url = "https://streaming-availability.p.rapidapi.com/changes"
    querystring = {
        "country": "us",
        # "catalogs": catalog,
        "change_type": "new",
        "item_type": "show",
        "show_type": "movie",
        "output_language":"en",
        "order_direction":"asc"
    }
    headers = {
        "X-RapidAPI-Key": rapid_api_key,
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }

    print(f"querystring: {querystring}")
    movies_list = []
    response = requests.get(url, headers=headers, params=querystring)
    # print(response.json())
    if response.status_code == 200:
        data = response.json()
        movies = data.get("shows", [])
        
        print(f"Found {len(movies)} new movies:")
        for movie_key in movies:
            print(movie_key)
            title = movies[movie_key].get("title")
            movies_list.append(title)
            release_year = movies[movie_key].get("releaseYear")
            streaming_info = movies[movie_key].get("streamingOptions", {})
            platforms = ", ".join(streaming_info.keys()) if streaming_info else "Unknown"
            print(f"- {title} ({release_year}) on {platforms}")
                
    else:
        print(f"Failed to fetch data: {response.status_code}")
        print(response.text)

    return movies_list

def check_ratings(movies_list):
    if(isinstance(movies_list, str)):
        movies_list = ast.literal_eval(movies_list)
    ratings_dict = {}
    for movie in movies_list:
        print(f"movie {movie}")
        rating = get_imdb_rating(movie)
        try:
            ratings_dict[movie] = float(rating)
        except Exception as e:
            ratings_dict[movie] = float(0)


def get_imdb_rating(title):
    omdb_api_key = os.getenv("OMDB_API_KEY")
    url = f"http://www.omdbapi.com/?t={title}&apikey={omdb_api_key}"
    response = requests.get(url)
    data = response.json()
    
    if data['Response'] == 'True':
        return data.get('imdbRating', 'N/A')
    else:
        print(f"Error: {data.get('Error', 'Movie not found')}")
        return 'N/A'



# def check_ratings(movies_list):
#     # Create an IMDb object
#     ia = Cinemagoer()
#     ratings_dict = {}
    
#     for movie in movies_list:
#         try:
#             # Search for the movie
#             search_results = ia.search_movie(movie)
            
#             if search_results:
#                 # Get the first result (most relevant)
#                 movie_id = search_results[0].movieID
#                 # Get the movie info
#                 movie_info = ia.get_movie(movie_id)
                
#                 # Get rating and convert to float
#                 if 'rating' in movie_info:
#                     ratings_dict[movie] = float(movie_info['rating'])
#                 else:
#                     ratings_dict[movie] = 0.0  # Default if no rating found
#             else:
#                 ratings_dict[movie] = 0.0  # Default if movie not found 
#         except Exception as e:
#             print(f"Error fetching rating for {movie}: {str(e)}")
#             ratings_dict[movie] = 0.0
            
#     return ratings_dict

def sort_by_ratings(movies_rating_dict):
    return dict(sorted(movies_rating_dict.items(), key=lambda item:item[1], reverse=True))

def select_top_movies(sorted_movies_dict, top_n):
    if len(sorted_movies_dict) > top_n:
        return sorted_movies_dict
    else:
        return sorted_movies_dict[:top_n]