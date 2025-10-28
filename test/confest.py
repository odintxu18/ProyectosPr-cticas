import pytest
from src.partida.domain.tablero import *


@pytest.fixture
def tablr():
    return Tablero()
