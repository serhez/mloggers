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
        *messages: str | dict[str, Any],
        level: LogLevel | str | None = None,
        mask: list[type[Logger]] | None = None,
        **kwargs: Any,
    ):
        """
        Logs a message to multiple loggers.

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

        # NOTE: No need for checking the validity of the message, as the individual loggers will do that.
        # super(MultiLogger, self).log(message, level, *args, **kwargs)

        if mask is None:
            mask = self._default_mask

        for logger in [
            logger
            for logger in self._loggers
            if not any(isinstance(logger, type) for type in mask)
        ]:
            logger(*messages, level=level, **kwargs)

    def info(
        self,
        *messages: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(*messages, level=LogLevel.INFO, mask=mask, **kwargs)  # type:ignore[reportArgumentType]

    def warn(
        self,
        *messages: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(*messages, level=LogLevel.WARN, mask=mask, **kwargs)  # type:ignore[reportArgumentType]

    # Alias warning to warn
    warning = warn

    def error(
        self,
        *messages: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(*messages, level=LogLevel.ERROR, mask=mask, **kwargs)  # type:ignore[reportArgumentType]

    def debug(
        self,
        *messages: str | dict[str, Any],
        mask: list[type[Logger]] | None = None,
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
        `mask`: a list of logger names to not be used to log this message.
        - If None, the default mask will be used.
        """

        self.log(*messages, level=LogLevel.DEBUG, mask=mask, **kwargs)  # type:ignore[reportArgumentType]
