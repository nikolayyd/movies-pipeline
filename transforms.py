import json
import spacy
from crud import *

# Load the small English NLP model
nlp = spacy.load("en_core_web_sm")


MULTI_GENRE_MAP = {
    ("Science", "Fiction"): "Science Fiction",
    ("TV", "Movie"): "TV Movie",
    ("Film", "Noir"): "Film Noir",
    ("Dark", "Fantasy"): "Dark Fantasy",
    ("Martial", "Arts"): "Martial Arts",
    ("Reality", "TV"): "Reality TV",
}

def transform_genres(genres_str: str):
    """Transform genres string into list of genres"""
    if not genres_str:
        return []

    words = genres_str.split()
    result = []
    i = 0

    while i < len(words):
        if i + 1 < len(words) and (words[i], words[i+1]) in MULTI_GENRE_MAP:
            result.append(MULTI_GENRE_MAP[(words[i], words[i+1])])
            i += 2
        else:
            result.append(words[i])
            i += 1
    return result

def transform_cast(cast_str: str):
    """Transform cast string into list of actor names"""
    if not cast_str:
        return []

    doc = nlp(cast_str)
    actors = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]

    return list(dict.fromkeys(actors))

def transform_keywords(keywords_str: str):
    """Transform keywords string into list of keywords
    :param keywords_str: string containing keywords
    :return: list of keywords
    """
    if not keywords_str:
        return []
    return [k.strip() for k in keywords_str.split()]


def transform_json(json_str: str):
    """
    Transform JSON string into list of dictionaries.
    :param json_str: string containing JSON data
    :return: list of dictionaries
    """
    if not json_str or json_str.strip() == "":
        return []
    try:
        fixed_str = json_str.replace("'", '"')
        data = json.loads(fixed_str)
        return data if isinstance(data, list) else [data]
    except json.JSONDecodeError:
        return []

def transform_movies(staging_movies):
    """
    Transform staging movies into final movie objects.
    :param staging_movies: Base movies from staging table
    """
    fields_config = [
        ("genres", Genre, MovieGenre, transform_genres, ["name"], "genre_id"),
        ("keywords", Keyword, MovieKeyword, transform_keywords, ["name"], "keyword_id"),
        ("cast", Cast, MovieCast, transform_cast, ["name"], "cast_id"),
        ("crew", Crew, MovieCrew, transform_json, ["id"], "crew_id"),
        ("production_companies", ProductionCompany, MovieProductionCompany, transform_json, ["id"], "company_id"),
        ("production_countries", ProductionCountry, MovieProductionCountry, transform_json, ["iso_3166_1"], "country_id"),
        ("spoken_languages", SpokenLanguage, MovieSpokenLanguage, transform_json, ["iso_639_1"], "language_id"),
    ]

    with SessionLocal() as session:
        with session.no_autoflush:
            for counter, sm in enumerate(staging_movies, start=1):
                if counter % 100 == 0:
                    print(f"Transformed {counter} movies...")

                m = session.get(Movie, sm.id)
                if m is None:
                    m = Movie(id=sm.id)
                    session.add(m)

                m.title = sm.title
                m.budget = int(sm.budget) if sm.budget else None
                m.homepage = sm.homepage
                m.original_language = sm.original_language
                m.original_title = sm.original_title
                m.overview = sm.overview
                m.popularity = float(sm.popularity) if sm.popularity else None
                m.release_date = sm.release_date
                m.revenue = int(sm.revenue) if sm.revenue else None
                m.runtime = float(sm.runtime) if sm.runtime else None
                m.status = sm.status
                m.tagline = sm.tagline
                m.vote_average = float(sm.vote_average) if sm.vote_average else None
                m.vote_count = int(sm.vote_count) if sm.vote_count else None
                m.director = sm.director

                session.flush()

                for attr, model, link_table, transformer, lookup_keys, fk_name in fields_config:
                    items = getattr(sm, attr)
                    if not items:
                        continue

                    transformed_items = transformer(items)
                    objs = get_or_create_fields(
                        transformed_items,
                        model,
                        session=session,
                        lookup_keys=lookup_keys
                    )

                    seen = set()
                    for obj in objs:
                        if obj.id not in seen:
                            link_tables(m.id, fk_name, obj.id, link_table, session)
                            seen.add(obj.id)

            session.commit()
            print("Transformed and loaded movies successfully.")