from pydantic import BaseModel, Field
from typing import Optional


class BasePaginationQueryDTO(BaseModel):
    page: int = Field(1, ge=1, description="Page number (starting from 1)")
    page_size: int = Field(10, ge=1, le=100, description="Number of items per page")
    search: Optional[str] = Field(None, description="Search query string")
    sort: Optional[str] = Field(None, description="Sort order (e.g. 'asc', 'desc')")
    filter: Optional[dict] = Field(None, description="Filter criteria")
