from enum import Enum
from typing import Union
import bcrypt

class AppError(Exception):
    """Base class for application errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class DatabaseError(AppError):
    def __init__(self, db_error: str):
        super().__init__(f"Database error: {db_error}")


class HashingError(AppError):
    def __init__(self, bcrypt_error: str):
        super().__init__(f"Hashing error: {bcrypt_error}")


class NotFoundError(AppError):
    def __init__(self, resource: str):
        super().__init__(f"Not Found: {resource}")


class ValidationError(AppError):
    def __init__(self, validation_error: str):
        super().__init__(f"Validation error: {validation_error}")


class PasswordError(AppError):
    def __init__(self, reason: str):
        super().__init__(f"Password error: {reason}")


class TokenExpiredError(AppError):
    def __init__(self, message):
        super().__init__(message)


class TokenValidationError(AppError):
    def __init__(self, message):
        super().__init__(message)


class TokenGenerationError(AppError):
    def __init__(self, jwt_error: str):
        super().__init__(f"Token generation error: {jwt_error}")


class BcryptError(AppError):
    def __init__(self, bcrypt_error: str):
        super().__init__(f"Bcrypt error: {bcrypt_error}")


class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__("Invalid credentials")


class EmailAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__("Email already exists")
