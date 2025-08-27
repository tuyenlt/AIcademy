from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from sqlalchemy.ext.asyncio import AsyncSession

Query = Dict[str, Any]


class IBaseCrudRepository(ABC):

    @abstractmethod
    async def create(
        self, data: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> Any:
        pass

    @abstractmethod
    async def update(
        self, id: Any, data: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> Any:
        pass

    @abstractmethod
    async def upsert(
        self, data: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> Any:
        pass

    @abstractmethod
    async def delete(self, id: Any, session: Optional[AsyncSession] = None) -> None:
        pass

    @abstractmethod
    async def bulk_delete(
        self, ids: List[Any], session: Optional[AsyncSession] = None
    ) -> int:
        pass

    @abstractmethod
    async def soft_delete(self, id: Any, session: Optional[AsyncSession] = None) -> Any:
        pass

    @abstractmethod
    async def find_by_filter(
        self,
        filter_: Dict[str, Any],
        session: Optional[AsyncSession] = None,
        order_by: Optional[Dict[str, str]] = None,
    ) -> List[Any]:
        pass

    @abstractmethod
    async def find_one_by_filter(
        self,
        filter_: Dict[str, Any],
        session: Optional[AsyncSession] = None,
    ) -> Optional[Any]:
        pass

    @abstractmethod
    async def paginate(
        self,
        query_builder_func: Callable[[AsyncSession], Any],
        page: int = 1,
        per_page: int = 10,
        session: Optional[AsyncSession] = None,
    ) -> Dict[str, Any]:
        pass
