from abc import ABC, abstractmethod
from typing import Any, Callable

from mloggers._log_levels import LogLevel

# This constant is used to assign an importance level to anything not using the LogLevel enum.
# It was chosen to be the same as LogLevel.INFO, but it can be changed to any other value.
DEFAULT_IMPORTANCE = LogLevel.INFO.value["level"]  # type:ignore[reportAttributeAccessIssue]


class Logger(ABC):
    """The abstract class for a logger."""

    def __init__(self, default_level: LogLevel | int = LogLevel.INFO):  # type:ignore[reportArgumentType]
        """
        Initialize the logger.

        ### Parameters
        ----------
        `log_level`: the default log level to use.
        - This parameter filters out messages with a lower importance level than the one provided. It can be either a `LogLevel` object or an integer.
        - When calling the logger with a level not from the `LogLevel` enum, the importance level will be set to 0 (same as `LogLevel.INFO`).
        - For example, if the log level is set to `LogLevel.INFO`, only messages with a level of `LogLevel.INFO` or higher will be printed (which excludes `LogLevel.DEBUG`).
        """

        self._log_level = (
            default_level.value["level"]
            if isinstance(default_level, LogLevel)
            else default_level
        )

    @abstractmethod
    def log(
        self,
        message: str | dict[str, Any],
        level: LogLevel | str | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        """
        Log a message.

        ### Parameters
        ----------
        `message`: the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        `level`: the level of the message (e.g., INFO, WARN, ERROR, DEBUG, etc.).
        - If None, no level will be printed.
        - If a string is provided, it will be colored in green (when colors are used) and uppercased; otherwise, the color will be the one associated with the `LogLevel` at time of registration.

        ### Raises
        ----------
        `TypeError`: if the message is not a string, a dictionary or does not implement `__str__()`.
        """

        if (
            not isinstance(message, dict)
            and not hasattr(message, "__str__")
            and not callable(getattr(message, "__str__"))
        ):
            raise TypeError(
                f"Expected message to be a string, a dictionary or to have implemented __str__(), but got {type(message)}."
            )

        # Filter out messages with a lower importance level than the current log level.
        if isinstance(level, LogLevel) and level.value["level"] < self._log_level:
            return False
        elif isinstance(level, str) and DEFAULT_IMPORTANCE < self._log_level:
            return False
        return True

    def set_level(self, level: LogLevel | int):
        """
        Set the log level.

        ### Parameters
        ----------
        `level`: the log level to set.
        - If a string, it must be a valid log level (e.g., INFO, WARN, ERROR, DEBUG, etc.).
        - If a `LogLevel` object, it will be used as-is.
        """
        self._log_level = level.value["level"] if isinstance(level, LogLevel) else level

    def _call_impl(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    __call__: Callable[..., Any] = _call_impl

    def info(
        self,
        message: str | dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.INFO.

        ### Parameters
        ----------
        `message`: the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.INFO, *args, **kwargs)  # type:ignore[reportArgumentType]

    def warn(
        self,
        message: str | dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.WARN.

        ### Parameters
        ----------
        `message`: the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.WARN, *args, **kwargs)  # type:ignore[reportArgumentType]

    # Alias warning to warn
    warning = warn

    def error(
        self,
        message: str | dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.ERROR.

        ### Parameters
        ----------
        `message`: the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.ERROR, *args, **kwargs)  # type:ignore[reportArgumentType]

    def debug(
        self,
        message: str | dict[str, Any],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.DEBUG.

        ### Parameters
        ----------
        `message`: the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.DEBUG, *args, **kwargs)  # type:ignore[reportArgumentType]
