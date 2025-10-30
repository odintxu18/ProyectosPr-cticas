import uuid

import pytest
from _pytest.fixtures import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.juego.repository.sql_alchemy_jugador_repository import (
    JugadorRepositorySQLAlchemy,
)
from test.common.FakeRepositoryJugadaPartida import (
    FakePartidaJugadaRepositorySQLAlchemy,
)
from test.common.FakeRepositoryJugador import FakeJugadorRepositorySQLAlchemy
from test.common.object_mother import (
    jugador_mother,
    partida_mother,
    jugada_mother,
    nombre_mother,
    correo_mother,
)
from src.partida.repository.sql_alchemy_jugada_partida_repository import (
    PartidaJugadaRepositorySQLAlchemy,
)


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///db1.db")  # tu DB de prueba
    SessionLocal = sessionmaker(bind=engine)
    session: Session = SessionLocal()
    yield session
    session.rollback()


@fixture
def repo_jugadores(session):
    return JugadorRepositorySQLAlchemy(session)


@fixture
def repo_partidas(session):
    return PartidaJugadaRepositorySQLAlchemy(session)


@fixture
def fake_repo_jugadores(session):
    return FakeJugadorRepositorySQLAlchemy(session)


@fixture
def fake_repo_partidas(session):
    return FakePartidaJugadaRepositorySQLAlchemy(session)


@pytest.fixture
def jugador_x():
    return jugador_mother()


@fixture
def jugador_o():
    return jugador_mother()


@fixture
def partida(jugador_x, jugador_o):
    return partida_mother(jugador_x, jugador_o)


@fixture
def jugada(partida, jugador_x):
    return jugada_mother(partida, jugador_x)


@pytest.fixture
def nombre():
    return nombre_mother()


@pytest.fixture
def correo():
    return correo_mother()
