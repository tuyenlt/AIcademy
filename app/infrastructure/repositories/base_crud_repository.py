import datetime
from typing import Any, Dict, List, Optional, Callable, Type
from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound

from app.infrastructure.configs.db_config import AsyncSessionLocal


class BaseCrudRepository:

    model: Type  # SQLAlchemy declarative model, set in subclass

    def __init__(self, model: Type):
        self.model = model

    # --- session handling ---
    async def _get_session(
        self, session: Optional[AsyncSession] = None
    ) -> AsyncSession:
        return session or AsyncSessionLocal()

    # --- basic CRUD ---
    async def create(
        self, data: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> Any:
        db = await self._get_session(session)
        async with db.begin():
            obj = self.model(**data)
            db.add(obj)
            await db.flush()
            return obj

    async def update(
        self, id: Any, data: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> Any:
        db = await self._get_session(session)
        async with db.begin():
            obj = await db.get(self.model, id)
            if not obj:
                raise NoResultFound(f"{self.model.__name__} with id={id} not found")
            for k, v in data.items():
                setattr(obj, k, v)
            await db.flush()
            return obj

    async def upsert(
        self, data: Dict[str, Any], session: Optional[AsyncSession] = None
    ) -> Any:
        db = await self._get_session(session)
        async with db.begin():
            obj = None
            if "id" in data:
                obj = await db.get(self.model, data["id"])
            if obj:
                for k, v in data.items():
                    setattr(obj, k, v)
            else:
                obj = self.model(**data)
                db.add(obj)
            await db.flush()
            return obj

    async def delete(self, id: Any, session: Optional[AsyncSession] = None) -> None:
        db = await self._get_session(session)
        async with db.begin():
            obj = await db.get(self.model, id)
            if not obj:
                raise NoResultFound(f"{self.model.__name__} with id={id} not found")
            await db.delete(obj)

    async def bulk_delete(
        self, ids: List[Any], session: Optional[AsyncSession] = None
    ) -> int:
        db = await self._get_session(session)
        async with db.begin():
            stmt = delete(self.model).where(self.model.id.in_(ids))
            result = await db.execute(stmt)
            return result.rowcount

    async def soft_delete(self, id: Any, session: Optional[AsyncSession] = None) -> Any:
        db = await self._get_session(session)
        async with db.begin():
            obj = await db.get(self.model, id)
            if not obj:
                raise NoResultFound(f"{self.model.__name__} with id={id} not found")
            setattr(obj, "deleted_at", datetime.datetime.now())
            await db.flush()
            return obj

    # --- find / query ---
    async def find_by_filter(
        self,
        filter_: Dict[str, Any],
        session: Optional[AsyncSession] = None,
        order_by: Optional[Dict[str, str]] = None,
    ) -> List[Any]:
        db = await self._get_session(session)
        async with db.begin():
            q = select(self.model)
            for k, v in filter_.items():
                q = q.where(getattr(self.model, k) == v)
            if order_by:
                for k, direction in order_by.items():
                    col = getattr(self.model, k)
                    q = q.order_by(
                        col.asc() if direction.upper() == "ASC" else col.desc()
                    )
            result = await db.execute(q)
            return result.scalars().all()

    async def find_one_by_filter(
        self,
        filter_: Dict[str, Any],
        session: Optional[AsyncSession] = None,
    ) -> Optional[Any]:
        db = await self._get_session(session)
        async with db.begin():
            q = select(self.model)
            for k, v in filter_.items():
                q = q.where(getattr(self.model, k) == v)
            result = await db.execute(q)
            return result.scalars().first()

    # --- pagination with query builder ---
    async def paginate(
        self,
        query_builder_func: Callable[[AsyncSession], Any],
        page: int = 1,
        per_page: int = 10,
        session: Optional[AsyncSession] = None,
    ) -> Dict[str, Any]:
        db = await self._get_session(session)
        async with db.begin():
            q = query_builder_func(db)
            total = await db.execute(select([q.count()]))
            total_count = total.scalar() or 0
            data_result = await db.execute(
                q.offset((page - 1) * per_page).limit(per_page)
            )
            data_list = data_result.scalars().all()
            return {
                "total": total_count,
                "total_pages": ceil(total_count / per_page),
                "current_page": page,
                "limit": per_page,
                "data_list": data_list,
            }
