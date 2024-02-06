from enum import Enum

__logger_level_members = {
    "WARN": "yellow",
    "ERROR": "red",
    "DEBUG": "magenta",
    "INFO": "cyan",
}

LogLevel = Enum("LogLevel", __logger_level_members)


def register_level(level: str, color: str):
    """
    Register a customized logger level, which will then be available as a member of `LogLevel`,
    where its `name` is the argument `level` and its `value` is the argument `color`.
    Note: the name of the level will be uppercased.

    ### Parameters
    ----------
    `level` -> the level name to register.
    `color` -> the color to use for the level.
    """

    level = level.upper()
    __logger_level_members.update({level: color})
    LogLevel[level] = color
