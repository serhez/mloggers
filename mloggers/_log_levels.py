import sys
from dataclasses import dataclass

from aenum import Enum, extend_enum


class LogLevel(Enum):  # type:ignore[reportGeneralTypeIssues]
    """
    The available log levels.
    Each level is associated with a color and an importance level.
    The importance level is used to set the minimum level of logs to display (all logs higher than the set level will be displayed).
    To register a new level use `mloggers.register_level`.
    """

    @dataclass
    class Properties:
        color: str
        """The color to use when printing the log."""

        priority: int
        """The importance level of the log."""

    ERROR = "error"
    WARN = "warn"
    INFO = "info"
    DEBUG = "debug"


_log_level_properties: dict[str, LogLevel.Properties] = {
    LogLevel.ERROR: LogLevel.Properties(color="red", priority=sys.maxsize),
    LogLevel.WARN: LogLevel.Properties(color="yellow", priority=1),
    LogLevel.INFO: LogLevel.Properties(color="cyan", priority=0),
    LogLevel.DEBUG: LogLevel.Properties(color="magenta", priority=-1),
}


def register_level(name: str, properties: LogLevel.Properties):
    """
    Register a customized logger level, which will then be available as a member of `LogLevel`,
    where its `name` is the argument `level` and its `value` is the argument `level_info`.
    Note: the name of the level will be uppercased.

    ### Parameters
    ----------
    `level`: the level name to register.
    `properties`: the properties of the level.
    """

    extend_enum(LogLevel, name.upper(), name)
    _log_level_properties[name] = properties
