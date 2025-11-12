import uuid
from datetime import datetime

import pytest
from _pytest.fixtures import fixture
from sqlalchemy.orm import sessionmaker, Session

from src.jugador.handler import handler_jugador
from src.jugador.repository.sql_alchemy_jugador_repository import (
    JugadorRepositorySQLAlchemy,
)
from src.shared.dbmodels.database import SessionLocal
from src.shared.dbmodels.dbmodels import Partida, Jugada
from test.common.FakeRepositoryJugadaPartida import (
    FakePartidaJugadaRepositorySQLAlchemy,
)
from test.common.FakeRepositoryJugador import FakeJugadorRepositorySQLAlchemy
from test.common.FakeUnitofWork import FakeUnitOfWork
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


@pytest.fixture
def fake_uow(fake_repo_jugadores):
    return FakeUnitOfWork(fake_repo_jugadores)


@pytest.fixture
def jugador_handler(fake_uow):

    return handler_jugador(fake_uow)


@pytest.fixture
def setup_partida(session):
    # Crear IDs de jugadores
    id_jugador_x = str(uuid.uuid4())
    id_jugador_o = str(uuid.uuid4())

    # Crear partida
    partida = Partida(
        id=str(uuid.uuid4()),
        id_jugador_x=id_jugador_x,
        id_jugador_o=id_jugador_o,
        fecha_inicio=datetime.now(),
    )
    session.add(partida)
    session.commit()

    # Crear jugada asociada
    jugada = Jugada(
        id=str(uuid.uuid4()),
        id_partida=partida.id,
        id_jugador=id_jugador_x,
        turno=1,
        fila=0,
        columna=0,
        fecha_jugada=datetime.now(),
    )
    session.add(jugada)
    session.commit()

    return session, jugada
