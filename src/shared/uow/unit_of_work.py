from abc import ABC, abstractmethod


class IUnitOfWork(ABC):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass

    @abstractmethod
    def get_repository(self, repository_key: str):
        pass

    @abstractmethod
    def get_new_session(self):
        pass

    @abstractmethod
    def close(self):
        pass
