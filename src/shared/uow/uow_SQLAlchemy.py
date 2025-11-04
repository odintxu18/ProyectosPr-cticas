from typing import Type
from sqlalchemy.orm import Session
from src.shared.dbmodels.database import SessionLocal
from src.shared.sql_alchemy_interface import SqlAlchemyInterface
from src.shared.uow.unit_of_work import IUnitOfWork


class UnitOfWorkSQLAlchemy(IUnitOfWork):
    def __init__(
        self,
        repositories: dict[str, Type[SqlAlchemyInterface]],
        session_factory=SessionLocal,
    ):
        self._session_factory = session_factory
        self._session: Session = None
        self._repositories = repositories
        self._connected_repositories = {}

    def connect(self):
        self._session = self.get_new_session()
        self._create_repositories(self._session)

    def disconnect(self, exc_type):
        if exc_type is None:
            self.commit()
        else:
            self.rollback()
        if self._session:
            self._session.close()

    def commit(self):
        if self._session:
            self._session.commit()

    def rollback(self):
        if self._session:
            self._session.rollback()

    def get_repository(self, repository_key: str):
        if repository_key in self._connected_repositories:
            return self._connected_repositories[repository_key]
        raise KeyError(f"Repository {repository_key} not exists")

    def get_new_session(self):
        return self._session_factory()

    def _create_repositories(self, session):
        for repository in self._repositories:
            self._connected_repositories[repository] = self._repositories[repository](
                session
            )
