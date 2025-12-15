import sqlalchemy
from db import Base

class MovieStaging(Base):
    __tablename__ = 'movie_staging'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    budget = sqlalchemy.Column(sqlalchemy.String)
    genres = sqlalchemy.Column(sqlalchemy.String)
    homepage = sqlalchemy.Column(sqlalchemy.String)
    keywords = sqlalchemy.Column(sqlalchemy.String)
    original_language = sqlalchemy.Column(sqlalchemy.String)
    original_title = sqlalchemy.Column(sqlalchemy.String)
    overview = sqlalchemy.Column(sqlalchemy.String)
    popularity = sqlalchemy.Column(sqlalchemy.String)
    production_companies = sqlalchemy.Column(sqlalchemy.String)
    production_countries = sqlalchemy.Column(sqlalchemy.String)
    release_date = sqlalchemy.Column(sqlalchemy.String)
    revenue = sqlalchemy.Column(sqlalchemy.String)
    runtime = sqlalchemy.Column(sqlalchemy.String)
    spoken_languages = sqlalchemy.Column(sqlalchemy.String)
    status = sqlalchemy.Column(sqlalchemy.String)
    tagline = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    vote_average = sqlalchemy.Column(sqlalchemy.String)
    vote_count = sqlalchemy.Column(sqlalchemy.String)
    cast = sqlalchemy.Column(sqlalchemy.String)
    crew = sqlalchemy.Column(sqlalchemy.String)
    director = sqlalchemy.Column(sqlalchemy.String)

class Movie(Base):
    __tablename__ = 'movie'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    budget = sqlalchemy.Column(sqlalchemy.BigInteger)
    homepage = sqlalchemy.Column(sqlalchemy.String)
    original_language = sqlalchemy.Column(sqlalchemy.String)
    original_title = sqlalchemy.Column(sqlalchemy.String)
    overview = sqlalchemy.Column(sqlalchemy.String)
    popularity = sqlalchemy.Column(sqlalchemy.Float)
    release_date = sqlalchemy.Column(sqlalchemy.Date)
    revenue = sqlalchemy.Column(sqlalchemy.BigInteger)
    runtime = sqlalchemy.Column(sqlalchemy.Float)
    status = sqlalchemy.Column(sqlalchemy.String)
    tagline = sqlalchemy.Column(sqlalchemy.String)
    title = sqlalchemy.Column(sqlalchemy.String)
    vote_average = sqlalchemy.Column(sqlalchemy.Float)
    vote_count = sqlalchemy.Column(sqlalchemy.BigInteger)
    director = sqlalchemy.Column(sqlalchemy.String)

    genres = sqlalchemy.orm.relationship("Genre", secondary="movies.movie_genre", back_populates="movies")
    keywords = sqlalchemy.orm.relationship("Keyword", secondary="movies.movie_keyword", back_populates="movies")
    cast = sqlalchemy.orm.relationship("Cast", secondary="movies.movie_cast", back_populates="movies")
    production_companies = sqlalchemy.orm.relationship("ProductionCompany", secondary="movies.movie_production_company", back_populates="movies")
    production_countries = sqlalchemy.orm.relationship("ProductionCountry", secondary="movies.movie_production_country", back_populates="movies")
    spoken_languages = sqlalchemy.orm.relationship("SpokenLanguage", secondary="movies.movie_spoken_language", back_populates="movies")
    crew = sqlalchemy.orm.relationship("Crew", secondary="movies.movie_crew", back_populates="movies")

class Genre(Base):
    __tablename__ = 'genre'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    movies = sqlalchemy.orm.relationship("Movie", secondary="movies.movie_genre", back_populates="genres")

class Keyword(Base):
    __tablename__ = 'keyword'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    movies = sqlalchemy.orm.relationship("Movie", secondary="movies.movie_keyword", back_populates="keywords")

class Cast(Base):
    __tablename__ = 'cast'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    movies = sqlalchemy.orm.relationship("Movie", secondary="movies.movie_cast", back_populates="cast")

class ProductionCompany(Base):
    __tablename__ = 'production_company'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    movies = sqlalchemy.orm.relationship("Movie", secondary="movies.movie_production_company", back_populates="production_companies")

class ProductionCountry(Base):
    __tablename__ = 'production_country'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    iso_3166_1 = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    movies = sqlalchemy.orm.relationship("Movie", secondary="movies.movie_production_country", back_populates="production_countries")

class SpokenLanguage(Base):
    __tablename__ = 'spoken_language'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    iso_639_1 = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    movies = sqlalchemy.orm.relationship("Movie", secondary="movies.movie_spoken_language", back_populates="spoken_languages")

class Crew(Base):
    __tablename__ = 'crew'
    __table_args__ = {'schema': 'movies'}
    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    gender = sqlalchemy.Column(sqlalchemy.Integer)
    department = sqlalchemy.Column(sqlalchemy.String)
    job = sqlalchemy.Column(sqlalchemy.String)
    credit_id = sqlalchemy.Column(sqlalchemy.String)
    movies = sqlalchemy.orm.relationship("Movie", secondary="movies.movie_crew", back_populates="crew")

# association tables

class MovieGenre(Base):
    __tablename__ = 'movie_genre'
    __table_args__ = {'schema': 'movies'}
    movie_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.movie.id'), primary_key=True)
    genre_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.genre.id'), primary_key=True)

class MovieKeyword(Base):
    __tablename__ = 'movie_keyword'
    __table_args__ = {'schema': 'movies'}
    movie_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.movie.id'), primary_key=True)
    keyword_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.keyword.id'), primary_key=True)

class MovieCast(Base):
    __tablename__ = 'movie_cast'
    __table_args__ = {'schema': 'movies'}
    movie_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.movie.id'), primary_key=True)
    cast_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.cast.id'), primary_key=True)

class MovieProductionCompany(Base):
    __tablename__ = 'movie_production_company'
    __table_args__ = {'schema': 'movies'}
    movie_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.movie.id'), primary_key=True)
    company_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.production_company.id'), primary_key=True)

class MovieProductionCountry(Base):
    __tablename__ = 'movie_production_country'
    __table_args__ = {'schema': 'movies'}
    movie_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.movie.id'), primary_key=True)
    country_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.production_country.id'), primary_key=True)

class MovieSpokenLanguage(Base):
    __tablename__ = 'movie_spoken_language'
    __table_args__ = {'schema': 'movies'}
    movie_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.movie.id'), primary_key=True)
    language_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.spoken_language.id'), primary_key=True)

class MovieCrew(Base):
    __tablename__ = 'movie_crew'
    __table_args__ = {'schema': 'movies'}
    movie_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.movie.id'), primary_key=True)
    crew_id = sqlalchemy.Column(sqlalchemy.BigInteger, sqlalchemy.ForeignKey('movies.crew.id'), primary_key=True)
