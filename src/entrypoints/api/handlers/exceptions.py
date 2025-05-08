from src.entrypoints.api.handlers.middleware import *


class BaseApiException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class DuplicateResourceException(BaseApiException): ...


class ResourceNotFoundException(BaseApiException): ...


class AuthException(BaseApiException): ...  # invalid login


class PermissionDeniedException(BaseApiException): ...


class ValidationException(BaseApiException): ...


class DatabaseException(BaseApiException): ...
