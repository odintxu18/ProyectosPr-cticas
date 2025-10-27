import pytest
from src.application.tablero import *

@pytest.fixture
def tablr():
    return Tablero()