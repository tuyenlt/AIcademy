from app.domain.models import IBaseModel


class IUser(IBaseModel):
    email: str
    full_name: str
    hashed_password: str
    hashed_refresh_token: str | None = None
    is_active: bool = True
    is_admin: bool = False
