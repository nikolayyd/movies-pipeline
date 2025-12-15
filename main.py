from create_tables import init_db
from models import *
from crud import *
from transforms import *
init_db()

from crud import load_movies_to_staging, read_movies_from_csv
movies_df = read_movies_from_csv("movies.csv")
load_movies_to_staging(movies_df)

clear_staging()
staging_movies = load_movies()
transform_movies(staging_movies)
