import uuid
from typing import List, Dict

from app.infrastructure.configs.db_config import sync_engine, SyncSessionLocal, Base
from app.infrastructure.entities.user_entity import UserEntity
from app.infrastructure.services.hash_service import HashService


def get_seed_users() -> List[Dict]:
    """Return list of users to seed. Values can be overridden with SEED_* env vars."""
    return [
        {
            "email": "admin@aicademy.com",
            "full_name": "admin",
            "password": "admin123",
            "is_admin": True,
        },
        {
            "email": "user1@aicademy.local",
            "full_name": "User One",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user2@aicademy.local",
            "full_name": "User Two",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user3@aicademy.local",
            "full_name": "User Three",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user4@aicademy.local",
            "full_name": "User Four",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user5@aicademy.local",
            "full_name": "User Five",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user6@aicademy.local",
            "full_name": "User Six",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user7@aicademy.local",
            "full_name": "User Seven",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user8@aicademy.local",
            "full_name": "User Eight",
            "password": "UserPass123!",
            "is_admin": False,
        },
        {
            "email": "user9@aicademy.local",
            "full_name": "User Nine",
            "password": "UserPass123!",
            "is_admin": False,
        },
    ]


def seed_users():
    """Create tables (if needed) and insert seed users idempotently."""

    # Ensure tables exist
    Base.metadata.create_all(bind=sync_engine)

    db = SyncSessionLocal()
    try:
        # If there is already data, skip seeding completely
        if db.query(UserEntity).first():
            print("Users table already has data, skipping seeding.")
            return

        hash_service = HashService()
        users = get_seed_users()
        created = 0

        for u in users:
            user = UserEntity(
                id=str(uuid.uuid4()),
                email=u["email"],
                full_name=u["full_name"],
                hashed_password=hash_service.hash(u["password"]),
                is_active=True,
                is_admin=u.get("is_admin", False),
            )
            db.add(user)
            created += 1

        db.commit()
        print(f"Seed complete. Created {created} users.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_users()
