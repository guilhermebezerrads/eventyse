from abc import ABC, abstractmethod

class IDatabase(ABC):
    @abstractmethod
    def create_connection(self):
        pass
