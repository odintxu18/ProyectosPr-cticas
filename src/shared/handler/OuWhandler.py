from contextlib import contextmanager
from src.shared.uow.unit_of_work import IUnitOfWork


class UowHandler:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    @contextmanager
    def context(self):
        try:
            self.uow.connect()
            yield self.uow
            self.uow.commit()
        except Exception as e:
            self.uow.rollback()
            raise e
        finally:
            self.uow.close()
