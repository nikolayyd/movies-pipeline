import pandas as pd
import sqlalchemy
from sqlalchemy.orm import Session

from db import SessionLocal,engine, Base
from models import *

def init_db():
    """
    Initialize the database: create schema and tables."""
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("CREATE SCHEMA IF NOT EXISTS movies;"))

    Base.metadata.create_all(bind=engine)
    print("DB initialized: schema + tables created.")

def read_movies_from_csv(file_path: str) -> pd.DataFrame:
    """
    Read movies from CSV file into DataFrame.
    :param file_path: path to CSV file
    :return: DataFrame with movie data
    """
    pd.set_option('display.max_columns', None)
    movies = pd.read_csv(file_path)
    return movies

def load_movies_to_staging(movies_df: pd.DataFrame):
    session = SessionLocal()
    try:
        movie_objs = []
        for _, row in movies_df.iterrows():
            existing = session.query(MovieStaging).filter_by(id=row['id']).first()
            if existing:
                continue

            movie_objs.append(MovieStaging(
                id=row['id'],
                budget=row['budget'],
                genres=row['genres'],
                homepage=row['homepage'],
                keywords=row['keywords'],
                original_language=row['original_language'],
                original_title=row['original_title'],
                overview=row['overview'],
                popularity=row['popularity'],
                production_companies=row['production_companies'],
                production_countries=row['production_countries'],
                release_date=row['release_date'],
                revenue=row['revenue'],
                runtime=row['runtime'],
                spoken_languages=row['spoken_languages'],
                status=row['status'],
                tagline=row['tagline'],
                title=row['title'],
                vote_average=row['vote_average'],
                vote_count=row['vote_count'],
                cast=row['cast'],
                crew=row['crew'],
                director=row['director']
            ))
        session.add_all(movie_objs)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def clear_staging():
    """
    Cleans staging table by converting None/NaN/NaT/non-string values into empty strings,
    except release_date which is converted to proper date or None.
    """
    session = SessionLocal()
    try:
        movies = session.query(MovieStaging).all()

        for movie in movies:
            for column in movie.__table__.columns:
                value = getattr(movie, column.name)

                if column.name == "release_date":
                    try:
                        if value and value not in ["NaN", "NaT"]:
                            value = pd.to_datetime(value).date()
                        else:
                            value = None
                    except (ValueError, TypeError):
                        value = None
                    setattr(movie, column.name, value)
                    continue

                if (
                    value is None
                    or value in ["NaN", "NaT"]
                    or (isinstance(value, float) and pd.isna(value))
                    or isinstance(value, pd._libs.tslibs.nattype.NaTType)
                ):
                    setattr(movie, column.name, "")
                else:
                    setattr(movie, column.name, str(value))

            session.add(movie)

        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def load_movies():
  """Load movies from staging table."""
  with SessionLocal() as session:
        movies = session.query(MovieStaging).all()
        return movies

def get_or_create_fields(items, model, session, lookup_keys=None):
    if not items:
        return []

    objects = []

    for item in items:
        if isinstance(item, dict):
            if not lookup_keys:
                raise ValueError("lookup_keys must be provided for JSON dicts")
            filter_dict = {key: item[key] for key in lookup_keys if key in item}
        else:
            filter_dict = {"name": item}

        obj = session.query(model).filter_by(**filter_dict).first()

        if obj is None:
            obj = model(**item) if isinstance(item, dict) else model(name=item)
            session.add(obj)
            session.flush()


        objects.append(obj)

    return objects

def link_tables(movie_id, related_field, related_id, link_model, session):
    if related_id is None:
        return

    exists = session.query(link_model).filter_by(
        movie_id=movie_id,
        **{related_field: related_id}
    ).first()

    if not exists:
        link_entry = link_model(movie_id=movie_id, **{related_field: related_id})
        session.add(link_entry)