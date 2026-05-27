from abc import ABC, abstractmethod
from uuid import UUID

class BaseRepository:

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def get_by_id(self, id: UUID):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass