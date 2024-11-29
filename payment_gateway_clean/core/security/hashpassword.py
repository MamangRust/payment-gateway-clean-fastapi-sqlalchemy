import bcrypt
from typing import Union
from core.errors import BcryptError, HashingError


class Hashing:
    """
    A utility class for password hashing and verification using bcrypt.
    """

    def __init__(self):
        pass

    async def hash_password(self, password: str) -> str:
        """
        Hashes a plain-text password.

        :param password: The plain-text password to be hashed.
        :return: The hashed password as a string.
        :raises HashingError: If the password cannot be hashed.
        """
        try:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            return hashed.decode("utf-8")
        except Exception as e:
            raise HashingError(f"Error hashing password: {str(e)}")

    async def compare_password(self, hashed_password: str, password: str) -> None:
        """
        Compares a plain-text password with a hashed password.

        :param hashed_password: The hashed password.
        :param password: The plain-text password to be verified.
        :raises BcryptError: If the passwords do not match or if there is an error during verification.
        """
        try:
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
                return  # Password matches
            else:
                raise BcryptError("Passwords do not match.")
        except Exception as e:
            raise BcryptError(f"Error verifying password: {str(e)}")
