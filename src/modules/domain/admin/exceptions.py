from src.core.handlers.middleware import *
from src.core.handlers.exceptions import *


class DuplicateUsernameException(DuplicateResourceException): ...


class DuplicateEmailException(DuplicateResourceException): ...


class InvalidAdminLoginException(AuthException): ...


class AdminPermissionDeniedException(PermissionDeniedException): ...


class AdminDatabaseOperationError(DatabaseOperationError): ...
