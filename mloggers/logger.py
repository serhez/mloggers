from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional, Union

from mloggers._log_levels import LogLevel


class Logger(ABC):
    @abstractmethod
    def log(
        self,
        message: Union[str, Dict[str, Any]],
        level: Optional[Union[LogLevel, str]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        """
        Log a message.

        ### Parameters
        ----------
        `message` -> the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        `level` -> the level of the message (e.g., INFO, WARN, ERROR, DEBUG, etc.).
        - If None, no level will be printed.
        - If a string is provided, it will be colored in green (when colors are used) and uppercased; otherwise, the color will be the one associated with the `LogLevel` at time of registration.

        ### Raises
        ----------
        `TypeError` -> if the message is not a string, a dictionary or does not implement `__str__()`.
        """

        if (
            not isinstance(message, dict)
            and not hasattr(message, "__str__")
            and not callable(getattr(message, "__str__"))
        ):
            raise TypeError(
                f"Expected message to be a string, a dictionary or to have implemented __str__(), but got {type(message)}."
            )

    def _call_impl(self, *args, **kwargs):
        return self.log(*args, **kwargs)

    __call__: Callable[..., Any] = _call_impl

    def info(
        self,
        message: Union[str, Dict[str, Any]],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level="INFO".

        ### Parameters
        ----------
        `message` -> the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.INFO, *args, **kwargs)

    def warn(
        self,
        message: Union[str, Dict[str, Any]],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level="WARN".

        ### Parameters
        ----------
        `message` -> the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.WARN, *args, **kwargs)

    def error(
        self,
        message: Union[str, Dict[str, Any]],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level="ERROR".

        ### Parameters
        ----------
        `message` -> the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.ERROR, *args, **kwargs)

    def debug(
        self,
        message: Union[str, Dict[str, Any]],
        *args: Any,
        **kwargs: Any,
    ):
        """
        Wrapper for calling `log` with level="DEBUG".

        ### Parameters
        ----------
        `message` -> the message to log.
        - If a stringifiable object (implements `__str__()`), the message will be logged as-is.
        - If a dictionary, the message will be logged as a JSON string.
            - The dictionary must be JSON serializable.
            - You can provide None dictionary values to mean that the key is a header or title of the message.
        """

        self.log(message, LogLevel.DEBUG, *args, **kwargs)
