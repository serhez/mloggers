from aenum import Enum, extend_enum


class LogLevel(Enum):
    """
    The available log levels.
    Each level is associated with a color.
    To register a new level use `mloggers.register_level`.
    """

    WARN = "yellow"
    ERROR = "red"
    DEBUG = "magenta"
    INFO = "cyan"


def register_level(level: str, color: str):
    """
    Register a customized logger level, which will then be available as a member of `LogLevel`,
    where its `name` is the argument `level` and its `value` is the argument `color`.
    Note: the name of the level will be uppercased.

    ### Parameters
    ----------
    `level` -> the level name to register.
    `color` -> the color to use for the level.
    - It must be a valid color name from the `termcolor` package.
    """

    level = level.upper()
    extend_enum(LogLevel, level, color)
