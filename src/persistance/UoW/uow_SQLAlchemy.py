from typing import Type
from sqlalchemy.orm import Session
from src.persistance.database import SessionLocal
from src.persistance.UoW.unit_of_work import IUnitOfWork
from src.repository.SQLAlchemy_repositories import RepositoryContainer


class UnitOfWorkSQLAlchemy(IUnitOfWork):
    def __init__(self, repository_container_class: Type, session_factory=SessionLocal):

        self._session_factory = session_factory
        self._session: Session = None
        self._repository_container_class = RepositoryContainer
        self.repositories = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()

    def connect(self):
        self._session = self.get_new_session()

        self.repositories = RepositoryContainer(self._session)

    def disconnect(self):
        if self._session:
            self._session.close()
            self._session = None

    def commit(self):
        if self._session:
            self._session.commit()

    def rollback(self):
        if self._session:
            self._session.rollback()

    def get_repository(self, repository_key: str):
        if not self.repositories:
            raise RuntimeError("Repositories not connected yet. Call connect() first.")
        repo = getattr(self.repositories, repository_key, None)
        if not repo:
            raise KeyError(f"Repository '{repository_key}' not found")
        return repo

    def get_new_session(self):
        return self._session_factory()

    def close(self):
        self.disconnect()
