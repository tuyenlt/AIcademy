from typing import Generic, List, Optional, TypeVar
from pydantic.generics import GenericModel

T = TypeVar("T")


class BasePaginationResponseDto(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    has_next: Optional[bool] = False
    has_prev: Optional[bool] = False
