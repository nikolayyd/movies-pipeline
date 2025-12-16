import pandas as pd
import sqlalchemy
from sqlalchemy.orm import Session

from db import SessionLocal,engine, Base
from models import *

def init_db():
    """
    Initialize the database: create schema and tables.
    """
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
    """
    Load movies from DataFrame into staging table.

    :param movies_df: DataFrame with movie data
    :type movies_df: pd.DataFrame
    """
    session = SessionLocal()
    try:
        for _, row in movies_df.iterrows():
            obj = session.get(MovieStaging, row["id"])

            if obj is None:
                obj = MovieStaging(id=row["id"])
                session.add(obj)

            for col in movies_df.columns:
                if hasattr(obj, col):
                    setattr(obj, col, row[col])

        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

def clear_staging():
    """
    Cleans staging table by converting None/NaN/NaT/non-string
    values into empty strings, except release_date
    which is converted to proper date or None.
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

def load_movies() -> list[MovieStaging]:
  """Load movies from staging table.
  :return: list of MovieStaging objects"""
  with SessionLocal() as session:
        movies = session.query(MovieStaging).all()
        return movies

def get_or_create_fields(items, model, session, lookup_keys=None) -> list:
    """
    Get or create related field objects.

    :param items: List of items to get or create
    :param model: SQLAlchemy model class
    :param session: SQLAlchemy session
    :param lookup_keys: List of keys to use for lookup
    :return: List of objects
    """
    if not items:
        return []

    objects = []

    for item in items:
        filter_dict = {k: item[k] for k in lookup_keys} if isinstance(item, dict) else {"name": item}
        obj = session.query(model).filter_by(**filter_dict).first()

        if obj is None:
            obj = model(**item) if isinstance(item, dict) else model(name=item)
            session.add(obj)
            session.flush()
        objects.append(obj)

    return objects

def link_tables(movie_id, related_field, related_id, link_model, session):
    """
    Link a movie to a related field.

    :param movie_id: ID of the movie
    :param related_field: Name of the related field
    :param related_id: ID of the related object
    :param link_model: Link model class
    :param session: SQLAlchemy session
    """
    if related_id is None:
        return

    exists = session.query(link_model).filter_by(
        movie_id=movie_id,
        **{related_field: related_id}
    ).first()

    if not exists:
        session.add(link_model(movie_id=movie_id, **{related_field: related_id}))