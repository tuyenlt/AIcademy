from abc import ABC, abstractmethod


class IJWTService(ABC):
    @abstractmethod
    def generate_access_token(self, payload: dict) -> str:
        pass

    @abstractmethod
    def generate_refresh_token(self, payload: dict) -> str:
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> dict:
        pass

    @abstractmethod
    def verify_refresh_token(self, token: str) -> dict:
        pass
