from src.core.handlers.middleware import *
from src.core.handlers.exceptions import *


class DuplicateAdminException(DuplicateResourceException): ...


class InvalidAdminLoginException(AuthException): ...


class AdminPermissionDeniedException(PermissionDeniedException): ...


class AdminDatabaseOperationError(DatabaseOperationError): ...
