import json
from datetime import datetime
from typing import Any

import numpy.typing as npt
from termcolor import colored

from mloggers._log_levels import LogLevel, _log_level_properties
from mloggers.logger import Logger


class ConsoleLogger(Logger):
    """Logs to the console (i.e., standard I/O)."""

    def __init__(self, default_priority: LogLevel = LogLevel.INFO):  # type:ignore[reportArgumentType]
        super().__init__(default_priority)

    def log(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
        level: LogLevel | str | None = None,
        **kwargs: Any,
    ):
        if not super(ConsoleLogger, self).log(*messages, level=level, **kwargs):
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
                level_clr = colored(level_str, _log_level_properties[level].color)  # type:ignore[reportArgumentType]
            else:
                level_clr = colored(level_str, "green")

        # The first level of the dictionary is printed as a multiline
        # indented message.
        # The rest of the levels are printed as a single line
        # prettifyed depending on the type of the value.

        # Handle multiple messages
        if len(messages) > 1:
            messages = list(messages)
            # If the messages are strings, join them into a single string.
            if all(
                hasattr(message, "__str__")
                and callable(getattr(message, "__str__"))
                and not isinstance(message, dict)
                for message in messages
            ):
                messages = " ".join([str(message) for message in messages])
            # If the messages are dictionaries, log them separately.
            else:
                for message in messages:
                    self.log(message, level=level)
                return
        else:
            messages = messages[0]

        if isinstance(messages, dict):
            first = True
            for key, value in messages.items():
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

        elif hasattr(messages, "__str__") and callable(getattr(messages, "__str__")):
            print(f"{level_clr}{time} {str(messages)}")
