from abc import ABC, abstractmethod
from typing import Any, Callable

import numpy.typing as npt

from mloggers._log_levels import LogLevel, _log_level_properties

# This constant is used to assign an importance level to anything not using the LogLevel enum.
# It was chosen to be the same as `LogLevel.INFO`, but it can be changed to any other value.
DEFAULT_IMPORTANCE = _log_level_properties[LogLevel.INFO].priority  # type:ignore[reportAttributeAccessIssue]


class Logger(ABC):
    """The abstract class for a logger."""

    def __init__(self, default_priority: LogLevel | int = LogLevel.INFO):  # type:ignore[reportArgumentType]
        """
        Initialize the logger.

        ### Parameters
        ----------
        `default_priority`: The default log level priority to use.
        - This parameter filters out messages with a lower importance level than the one provided. It can be either a `LogLevel` object or an integer.
        - When calling the logger with a level not from the `LogLevel` enum, the importance level will be set to 0 (same as `LogLevel.INFO`).
        - For example, if the log level is set to `LogLevel.INFO`, only messages with a level of `LogLevel.INFO` or higher will be printed (which excludes `LogLevel.DEBUG`).
        """

        self._min_priority = (
            _log_level_properties[default_priority].priority
            if isinstance(default_priority, LogLevel)
            else default_priority
        )

    @abstractmethod
    def log(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
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
            - If a list or numpy array, the message will be logged as a stringified list.
            - If a dictionary, the message will be logged as a JSON string.
                - The dictionary must be JSON serializable.
                - You can provide None dictionary values to mean that the key is a header or title of the message.
        - If multiple messages are provided, they must be either all dictionaries or none of them. Strings, lists and arrays will be joined into a single string, while dictionaries will be printed as separate log entries.
        `level`: the level of the message (e.g., INFO, WARN, ERROR, DEBUG, etc.).
        - If None, no level will be printed.
        - If a string is provided, it will be colored in green (when colors are used) and uppercased; otherwise, the color will be the one associated with the `LogLevel` at time of registration.

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

        # Filter out messages with a lower importance level than the current priority.
        if (
            isinstance(level, LogLevel)
            and _log_level_properties[level].priority < self._min_priority
        ):
            return False
        elif isinstance(level, str) and DEFAULT_IMPORTANCE < self._min_priority:
            return False
        return True

    def set_min_priority(self, value: LogLevel | int):
        """
        Set the minimum log level priority.

        ### Parameters
        ----------
        `value`: the log level priority to set.
        - If a `LogLevel`, the priority of that log level will be considered.
        - If an `int`, such number will be considered.
        """

        if isinstance(value, int):
            self._min_priority = value
        else:
            self._min_priority = _log_level_properties[value].priority

    def _call_impl(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    __call__: Callable[..., Any] = _call_impl

    def info(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with `level=LogLevel.INFO`.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
            - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
            - If a list or numpy array, the message will be logged as a stringified list.
            - If a dictionary, the message will be logged as a JSON string.
                - The dictionary must be JSON serializable.
                - You can provide None dictionary values to mean that the key is a header or title of the message.
        - If multiple messages are provided, they must be either all dictionaries or none of them. Strings, lists and arrays will be joined into a single string, while dictionaries will be printed as separate log entries.
        """

        self.log(*messages, level=LogLevel.INFO, **kwargs)  # type:ignore[reportArgumentType]

    def warn(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with `level=LogLevel.WARN`.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
            - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
            - If a list or numpy array, the message will be logged as a stringified list.
            - If a dictionary, the message will be logged as a JSON string.
                - The dictionary must be JSON serializable.
                - You can provide None dictionary values to mean that the key is a header or title of the message.
        - If multiple messages are provided, they must be either all dictionaries or none of them. Strings, lists and arrays will be joined into a single string, while dictionaries will be printed as separate log entries.
        """

        self.log(*messages, level=LogLevel.WARN, **kwargs)  # type:ignore[reportArgumentType]

    # Alias warning to warn
    warning = warn

    def error(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with `level=LogLevel.ERROR`.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
            - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
            - If a list or numpy array, the message will be logged as a stringified list.
            - If a dictionary, the message will be logged as a JSON string.
                - The dictionary must be JSON serializable.
                - You can provide None dictionary values to mean that the key is a header or title of the message.
        - If multiple messages are provided, they must be either all dictionaries or none of them. Strings, lists and arrays will be joined into a single string, while dictionaries will be printed as separate log entries.
        """

        self.log(*messages, level=LogLevel.ERROR, **kwargs)  # type:ignore[reportArgumentType]

    def debug(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with `level=LogLevel.DEBUG`.

        ### Parameters
        ----------
        `messages`: the messages to log.
        - These can be any number of messages, separated by commas. They can be of the following types:
            - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
            - If a list or numpy array, the message will be logged as a stringified list.
            - If a dictionary, the message will be logged as a JSON string.
                - The dictionary must be JSON serializable.
                - You can provide None dictionary values to mean that the key is a header or title of the message.
        - If multiple messages are provided, they must be either all dictionaries or none of them. Strings, lists and arrays will be joined into a single string, while dictionaries will be printed as separate log entries.
        """

        self.log(*messages, level=LogLevel.DEBUG, **kwargs)  # type:ignore[reportArgumentType]
