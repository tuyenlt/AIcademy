from app.domain.adapters.hashing import IHashService
import bcrypt


class HashService(IHashService):
    def hash(self, plain_text: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(plain_text.encode("utf-8"), salt)
        return hashed.decode("utf-8")

    def verify(self, plain_text: str, hashed_text: str) -> bool:
        return bcrypt.checkpw(plain_text.encode("utf-8"), hashed_text.encode("utf-8"))
