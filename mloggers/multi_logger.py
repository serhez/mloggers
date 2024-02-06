from typing import Any, Dict, Optional, Union

from mloggers._log_levels import LogLevel
from mloggers.logger import Logger


class MultiLogger(Logger):
    """Logs to multiple loggers."""

    def __init__(
        self,
        loggers: list[Logger],
        default_mask: list[Logger] = [],
    ):
        """
        Initializes a multi-logger.

        ### Parameters
        ----------
        `loggers` -> a list of the initialized loggers to use.
        `default_mask` -> the default mask to use when logging.
        """

        self._loggers = loggers
        self._default_mask = default_mask

    def log(
        self,
        message: Union[str, Dict[str, Any]],
        level: Optional[Union[LogLevel, str]] = None,
        mask: Optional[list[Logger]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        """
        Logs a message to multiple loggers.

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
        `mask` -> a list of logger names to not be used to log this message.
        - If None, the default mask will be used.

        ### Raises
        ----------
        `TypeError` -> if the message is not a string, a dictionary or does not implement `__str__()`.
        """

        # NOTE: No need for checking the validity of the message, as the individual loggers will do that.
        # super(MultiLogger, self).log(message, level, *args, **kwargs)

        if mask is None:
            mask = self._default_mask

        for logger in [
            logger
            for logger in self._loggers
            if not any(isinstance(logger, type) for type in mask)
        ]:
            logger(message, level, *args, **kwargs)

    def info(
        self,
        message: Union[str, Dict[str, Any]],
        mask: Optional[list[Logger]] = None,
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
        `mask` -> a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.INFO, mask, *args, **kwargs)

    def warn(
        self,
        message: Union[str, Dict[str, Any]],
        mask: Optional[list[Logger]] = None,
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
        `mask` -> a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.WARN, mask, *args, **kwargs)

    def error(
        self,
        message: Union[str, Dict[str, Any]],
        mask: Optional[list[Logger]] = None,
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
        `mask` -> a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.ERROR, mask, *args, **kwargs)

    def debug(
        self,
        message: Union[str, Dict[str, Any]],
        mask: Optional[list[Logger]] = None,
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
        `mask` -> a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.DEBUG, mask, *args, **kwargs)
