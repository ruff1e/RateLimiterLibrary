from abc import ABC, abstractmethod


class BaseBackend(ABC):

    @abstractmethod
    def is_allowed(self, key: str, limit: int, window: int) -> bool:
        pass
