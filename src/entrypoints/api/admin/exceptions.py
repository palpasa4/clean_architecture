from src.entrypoints.api.handlers.middleware import *
from src.entrypoints.api.handlers.exceptions import *


class DuplicateAdminException(DuplicateResourceException): ...


class InvalidAdminLoginException(AuthException): ...


class AdminPermissionDeniedException(PermissionDeniedException): ...


class AdminDatabaseOperationError(DatabaseOperationError): ...
