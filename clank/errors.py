"""Command errors."""


class Error(Exception):
    """Base exception."""

    def __init__(self, message=None, retcode=1, cause=None):
        """Raise a command error with the given message, return code, and cause."""
        super(Exception, self).__init__(message)
        self.retcode = retcode
        self.cause = cause


class CommandError(Error):
    """Raise on command error."""


class ArgumentError(Error):
    """Raise on argument error."""
