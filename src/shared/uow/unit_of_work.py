from abc import ABC, abstractmethod


class IUnitOfWork(ABC):

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    @abstractmethod
    def connect(self):
        raise NotImplementedError()

    @abstractmethod
    def disconnect(self):
        raise NotImplementedError()

    @abstractmethod
    def commit(self):
        raise NotImplementedError()

    @abstractmethod
    def rollback(self):
        raise NotImplementedError()

    @abstractmethod
    def get_repository(self, repository_key: str):
        raise NotImplementedError()

    @abstractmethod
    def get_new_session(self):
        raise NotImplementedError()

    @abstractmethod
    def close(self):
        raise NotImplementedError()
