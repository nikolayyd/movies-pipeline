import sqlalchemy
from db import engine, Base

def init_db():
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text("CREATE SCHEMA IF NOT EXISTS movies;"))

    Base.metadata.create_all(bind=engine)
    print("DB initialized: schema + tables created.")
