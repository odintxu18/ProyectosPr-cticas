from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Session, sessionmaker, declarative_base, relationship, declarative_base, session

from models.jugador import Jugador

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5432/tresenrayadatabase", echo=True)

Base = declarative_base()
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
with engine.connect() as conn:
    print("Conectado correctamente a PostgreSQL")

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()