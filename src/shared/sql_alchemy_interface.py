from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class SqlAlchemyInterface(ABC):
    def __init__(self, session: Session):
        self.session: Session = session
