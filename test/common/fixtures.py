import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.shared.dbmodels.dbmodels import Base, Jugada, Partida, Jugador


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///db1.db")  # tu DB de prueba
    SessionLocal = sessionmaker(bind=engine)
    session: Session = SessionLocal()
    yield session
    session.rollback()
