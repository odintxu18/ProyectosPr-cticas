from typing import Type
from sqlalchemy.orm import Session
from src.shared.dbmodels.database import SessionLocal
from src.shared.uow.unit_of_work import IUnitOfWork
from src.shared.uow.SQLAlchemy_repositories import (
    RepositoryContainer,
)


class UnitOfWorkSQLAlchemy(IUnitOfWork):
    def __init__(
        self,
        repository_container_class: Type[RepositoryContainer],
        session_factory=SessionLocal,
    ):

        self._session_factory = session_factory
        self._session: Session = None
        self._repository_container_class = repository_container_class
        self.repositories = None

    def __enter__(self):

        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        if exc_type is None:

            self.commit()
        else:
            self.rollback()
        self.disconnect()

    def connect(self):
        self._session = self.get_new_session()
        repository_storage = self._repository_container_class(self._session)
        self.repositories = repository_storage.get_repositories()

    def disconnect(self):
        if self._session:
            self._session.close()

    def commit(self):
        if self._session:
            self._session.commit()
            self._committed = True

    def rollback(self):
        if self._session:
            self._session.rollback()

    def get_repository(self, repository_key: str):
        if not self.repositories:
            raise RuntimeError("Repositories not connected yet. Call connect() first.")

        repo = self.repositories.get(repository_key)
        if not repo:
            raise KeyError(f"Repository '{repository_key}' not found")
        return repo

    def get_new_session(self):
        return self._session_factory()

    def close(self):
        self.disconnect()
