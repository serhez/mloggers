from typing import Any

from aenum import Enum, extend_enum
from numpy import inf


class LogLevel(Enum):  # type:ignore[reportGeneralTypeIssues]
    """
    The available log levels.
    Each level is associated with a color and an importance level.
    The importance level is used to set the minimum level of logs to display (all logs higher than the set level will be displayed).
    To register a new level use `mloggers.register_level`.
    """

    WARN = {"color": "yellow", "level": 1}
    ERROR = {"color": "red", "level": inf}
    DEBUG = {"color": "magenta", "level": -1}
    INFO = {"color": "cyan", "level": 0}


def register_level(level: str, level_info: dict[str, Any]):
    """
    Register a customized logger level, which will then be available as a member of `LogLevel`,
    where its `name` is the argument `level` and its `value` is the argument `level_info`.
    Note: the name of the level will be uppercased.

    ### Parameters
    ----------
    `level`: the level name to register.
    `level_info`: a dictionary with the following
        - `color`: the color to use when printing the log. (It must be a valid color name from the `termcolor` package.)
        - `level`: the importance level of the log. (It must be a number or `np.inf`.)
    """

    level = level.upper()
    extend_enum(LogLevel, level, level_info)
