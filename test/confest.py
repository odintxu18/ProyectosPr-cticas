import pytest
from tablero import *


@pytest.fixture
def tablr():
    return Tablero()
