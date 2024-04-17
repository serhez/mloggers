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
        *messages: str | dict[str, Any],
        level: LogLevel | str | None = None,
        **kwargs: Any,
    ):
        """
        Log a message.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
            - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
            - If a dictionary, the message will be logged as a JSON string.
                - The dictionary must be JSON serializable.
                - You can provide None dictionary values to mean that the key is a header or title of the message.
            `level`: the level of the message (e.g., INFO, WARN, ERROR, DEBUG, etc.).
            - If None, no level will be printed.
            - If a string is provided, it will be colored in green (when colors are used) and uppercased; otherwise, the color will be the one associated with the `LogLevel` at time of registration.
        - If multiple messages are provided, they must be either all strings or all dictionaries. Strings will be joined into a single string, while dictionaries will be printed as separate log entries.

        ### Raises
        ----------
        `TypeError`: if the message is not a string, a dictionary or does not implement `__str__()`.
        `TypeError`: if the messages are a mix of strings and dictionaries.
        """

        # Check if the messages are of the correct type.
        for message in messages:
            if (
                not isinstance(message, dict)
                and not hasattr(message, "__str__")
                and not callable(getattr(message, "__str__"))
            ):
                raise TypeError(
                    f"Expected message to be a string, a dictionary or to have implemented __str__(), but got {type(message)}."
                )

        # Check if there is both a string and a dictionary in the messages.
        if any(isinstance(message, dict) for message in messages) and any(
            not isinstance(message, dict) for message in messages
        ):
            raise TypeError(
                "Expected all messages to be either strings or dictionaries, but got a mix of both."
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
        *messages: str | dict[str, Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.INFO.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(*messages, level=LogLevel.INFO, **kwargs)  # type:ignore[reportArgumentType]

    def warn(
        self,
        *messages: str | dict[str, Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.WARN.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(*messages, level=LogLevel.WARN, **kwargs)  # type:ignore[reportArgumentType]

    # Alias warning to warn
    warning = warn

    def error(
        self,
        *messages: str | dict[str, Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.ERROR.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(*messages, level=LogLevel.ERROR, **kwargs)  # type:ignore[reportArgumentType]

    def debug(
        self,
        *messages: str | dict[str, Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level=LogLevel.DEBUG.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(*messages, level=LogLevel.DEBUG, **kwargs)  # type:ignore[reportArgumentType]
