from abc import ABC, abstractmethod


class IUnitOfWork(ABC):

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    @abstractmethod
    def connect(self):
        raise NotImplementedMethod

    @abstractmethod
    def disconnect(self):
        raise NotImplementedMethod

    @abstractmethod
    def commit(self):
        raise NotImplementedMethod

    @abstractmethod
    def rollback(self):
        raise NotImplementedMethod

    @abstractmethod
    def get_repository(self, repository_key: str):
        raise NotImplementedMethod

    @abstractmethod
    def get_new_session(self):
        raise NotImplementedMethod

    @abstractmethod
    def close(self):
        raise NotImplementedMethod
