from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from passlib.context import CryptContext

crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordHasher:
    def get_hash(self, plain_password: str) -> str:
        return crypt_context.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return crypt_context.verify(plain_password, hashed_password)
