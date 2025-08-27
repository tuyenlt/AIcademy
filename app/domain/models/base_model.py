from pydantic import BaseModel


class IBaseModel(BaseModel):
    id: str
    created_at: str
    updated_at: str
    deleted_at: str | None = None
