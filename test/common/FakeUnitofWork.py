from src.shared.uow.unit_of_work import IUnitOfWork


class FakeUnitOfWork(IUnitOfWork):
    def __init__(self, repo_jugadores, repo_partidas=None):
        self.repo_jugadores = repo_jugadores
        self.repo_partidas = repo_partidas or repo_partidas
        self._committed = False

    def connect(self):
        pass

    def disconnect(self):
        pass

    def commit(self):
        self._committed = True

    def rollback(self):
        pass

    def close(self):
        pass

    def get_new_session(self):
        return None

    def get_repository(self, key: str):
        if key == "jugador":
            return self.repo_jugadores
        elif key == "partida":
            return self.repo_partidas
        elif key == "jugada":
            return self.repo_partidas
        raise KeyError(f"Repository '{key}' not found")
