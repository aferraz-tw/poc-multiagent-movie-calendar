import mlflow
import pandas as pd

from dotenv import load_dotenv
from movies_newsletter_multi_agent.domain.movie import MovieReleaseDate
from utils.mlflow_utils import get_best_crew

mlflow.set_tracking_uri("http://localhost:5000")

def get_release_date_for_movies(movie_names: list[str]) -> list[MovieReleaseDate]:
   
    crew = get_best_crew()        
    movies_release_dates = pd.DataFrame()
    
    for movie_name in movie_names:
        data = {"movie_name": [movie_name]}
        movies_release_date = crew.predict(pd.DataFrame(data))
        movies_release_dates = pd.concat([movies_release_dates, movies_release_date], ignore_index=True)
    
    ordered_movies_release_dates = movies_release_dates.sort_values(by="release_date",
                                                                    ascending=True,
                                                                    na_position='last')
    
    return ordered_movies_release_dates

if __name__ == "__main__":
        
    dotenv_path = '.env'
    load_dotenv(dotenv_path)
    
    movies_names = ["Anora", "The Brustalist", "Sing Sing", "Nickel Boys",
                    "Blitz", "A Real pain", "Gladiador 2", "September 5", "Saturday Night",
                    "A Complete Unknown", "The apprentice", "Flow", "Ainda estou aqui",
                    "All we imagine as light", "Kneecap", "Parthenope", "The Girl with the needle",
                    "Piano Lesson", "Grand Tour", "I Saw the TV Glow", "The end", "Here",
                    "The Shrouds"]
    
    result = get_release_date_for_movies(movie_names=movies_names)
    
    print("Calendar: ")
    
    for _, movie in result.iterrows():
        print(f'''{movie.title} - {movie.release_date if movie.release_date else movie.comment}''')