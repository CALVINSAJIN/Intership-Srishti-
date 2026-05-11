class UserManagementError(Exception):
    """Base class for exceptions in this module."""
    pass

class UserAlreadyExistsError(UserManagementError):
    """Raised when trying to register a user that already exists."""
    pass

class AuthenticationError(UserManagementError):
    """Raised when login or authentication fails."""
    pass