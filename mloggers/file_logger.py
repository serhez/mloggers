import json
import os
from datetime import datetime
from typing import Any

import numpy.typing as npt
from termcolor import colored

from mloggers._log_levels import LogLevel
from mloggers.logger import Logger
from mloggers.utils import serialize


class FileLogger(Logger):
    """Logs to a file."""

    def __init__(
        self,
        file_path: str,
        default_priority: LogLevel | int = LogLevel.INFO,  # type:ignore[reportArgumentType]
    ):
        """
        Initializes a file logger.

        ### Parameters
        ----------
        `file_path`: the path to the file to log to.
        - The file will be created if it does not exist. If it does, the logs will be appended to it.
        `default_priority`: The default log level priority to use.
        """

        super().__init__(default_priority)

        # Create the file if it does not exist
        if not os.path.exists(file_path):
            dir_path = os.path.dirname(file_path)
            try:
                # If dir path is empty, it means the file is in the current directory
                if dir_path != "":
                    os.makedirs(dir_path)
            except FileExistsError:
                pass
            with open(file_path, "w") as file:
                file.write("")

        print(f'{colored("[INFO]", "cyan")} [FileLogger] Logging to file {file_path}')

        self._file_path = file_path

    def log(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
        level: LogLevel | str | None = None,
        **kwargs: Any,
    ):
        if not super(FileLogger, self).log(*messages, level=level, **kwargs):
            return

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
                message = " ".join([str(message) for message in messages])
            # If the messages are dictionaries, log them separately.
            else:
                for message in messages:
                    self.log(message, level=level)
                return
        else:
            message = messages[0]

        # JSON-serialize the message
        try:
            message = serialize(message)
        except TypeError as e:
            print(
                f'{colored("[ERROR]", "red")} [FileLogger] Could not convert the message to a JSON serializable format: {e}'
            )
            return

        # Read the existing logs
        try:
            with open(self._file_path, "r") as file:
                existing_content = file.read()
                if (
                    existing_content == ""
                    or existing_content.isspace()
                    or existing_content == "[]"
                ):
                    prev_logs = []
                else:
                    try:
                        file.seek(0)
                        prev_logs = json.load(file)
                    except json.decoder.JSONDecodeError:
                        print(
                            f'{colored("[WARNING]", "yellow")} [FileLogger] Could not decode existing logs, new logs will not be appended to the file.'
                        )
                        return
        except Exception as e:
            print(
                f'{colored("[ERROR]", "red")} [FileLogger] Exception thrown while reading from the logging file: {e}'
            )
            return

        # Create the new log and write it to the file
        new_logs = prev_logs.copy()
        try:
            log: dict[str, Any] = {
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            }
            if level is not None:
                log["level"] = (
                    level.name if isinstance(level, LogLevel) else str(level).upper()
                )
            log["message"] = message
            new_logs.append(log)

            with open(self._file_path, "w") as file:
                file.seek(0)
                json.dump(new_logs, file, indent=4)

        except Exception as e:
            print(
                f'{colored("[ERROR]", "red")} [FileLogger] Exception thrown while logging to a file: {e}'
            )

            # Rollback the changes
            try:
                with open(self._file_path, "w") as file:
                    file.seek(0)
                    json.dump(prev_logs, file, indent=4)
            except Exception as e:
                print(
                    f'{colored("[ERROR]", "red")} [FileLogger] Exception thrown while rolling back the changes: {e}'
                )
