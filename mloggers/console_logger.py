import json
from datetime import datetime
from typing import Any

from termcolor import colored

from mloggers._log_levels import LogLevel
from mloggers.logger import Logger


class ConsoleLogger(Logger):
    """Logs to the console (i.e., standard I/O)."""

    def __init__(self, default_level: LogLevel = LogLevel.INFO):  # type:ignore[reportArgumentType]
        super().__init__(default_level)

    def log(
        self,
        message: str | dict[str, Any],
        level: LogLevel | str | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        if not super(ConsoleLogger, self).log(message, level, *args, **kwargs):
            return

        time = "[" + datetime.now().strftime("%H:%M:%S") + "]"

        if level is None:
            level_str = ""
            level_clr = ""
        else:
            # Create the level string to be printed
            if isinstance(level, LogLevel):
                level_str = "[" + level.name + "] "
            else:
                level_str = "[" + str(level).upper() + "] "

            # Color the level string
            if isinstance(level, LogLevel):
                level_clr = colored(level_str, level.value["color"])
            else:
                level_clr = colored(level_str, "green")

        # The first level of the dictionary is printed as a multiline
        # indented message.
        # The rest of the levels are printed as a single line
        # pretifyed depending on the type of the value.
        if isinstance(message, dict):
            first = True
            for key, value in message.items():
                if not first:
                    time = " " * len(time)
                    level_clr = " " * len(level_str)

                if isinstance(value, float):
                    print(f"{level_clr}{time} {key}: {value:.5f}")
                elif isinstance(value, dict | list):
                    value = json.dumps(value, indent=4)
                    print(f"{level_clr}{time} {key}: {value}")
                elif value is None:  # Used for headers, titles, etc.
                    print(f"{level_clr}{time} {key}")
                else:
                    print(f"{level_clr}{time} {key}: {value}")

                first = False

        elif hasattr(message, "__str__") and callable(getattr(message, "__str__")):
            print(f"{level_clr}{time} {str(message)}")
