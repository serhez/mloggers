from typing import Any

from mloggers._log_levels import LogLevel
from mloggers.logger import Logger


class MultiLogger(Logger):
    """Logs to multiple loggers."""

    def __init__(
        self,
        loggers: list[Logger],
        default_mask: list[type[Logger]] = [],
        default_level: LogLevel | int = LogLevel.INFO,  # type:ignore[reportArgumentType]
    ):
        """
        Initializes a multi-logger.

        ### Parameters
        ----------
        `loggers`: a list of the initialized loggers to use.
        `default_mask`: the default mask to use when logging.
        `default_level`: the default log level to use.
        """

        super().__init__(default_level)

        self._loggers = loggers
        self._default_mask = default_mask

        for logger in self._loggers:
            logger.set_level(self._log_level)

    def set_level(self, level: LogLevel | int):
        """
        Sets the log level of the multi-logger.

        ### Parameters
        ----------
        `level`: the level to set.
        """

        super(MultiLogger, self).set_level(level)

        for logger in self._loggers:
            logger.set_level(self._log_level)

    def log(
        self,
        message: str | dict[str, Any],
        level: LogLevel | str | None = None,
        mask: list[type[Logger]] | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        """
        Logs a message to multiple loggers.

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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.

        ### Raises
        ----------
        `TypeError`: if the message is not a string, a dictionary or does not implement `__str__()`.
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
        message: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.INFO, mask, *args, **kwargs)  # type:ignore[reportArgumentType]

    def warn(
        self,
        message: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.WARN, mask, *args, **kwargs)  # type:ignore[reportArgumentType]

    # Alias warning to warn
    warning = warn

    def error(
        self,
        message: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.ERROR, mask, *args, **kwargs)  # type:ignore[reportArgumentType]

    def debug(
        self,
        message: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(message, LogLevel.DEBUG, mask, *args, **kwargs)  # type:ignore[reportArgumentType]
