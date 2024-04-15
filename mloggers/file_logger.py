import json
import os
from datetime import datetime
from typing import Any

import numpy as np
from termcolor import colored

from mloggers._log_levels import LogLevel
from mloggers.logger import Logger


class FileLogger(Logger):
    """Logs to a file."""

    def __init__(self, file_path: str, default_level: LogLevel | int = LogLevel.INFO):  # type:ignore[reportArgumentType]
        """
        Initializes a file logger.

        ### Parameters
        ----------
        `file_path`: the path to the file to log to.
        - The file will be created if it does not exist. If it does, the logs will be appended to it.

        `default_level`: the default log level to use.
        """

        super().__init__(default_level)

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
        message: str | dict[str, Any],
        level: LogLevel | str | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        if not super(FileLogger, self).log(message, level, *args, **kwargs):
            return

        # Convert numpy's ndarrays to lists so that they are JSON serializable
        if isinstance(message, dict):
            for key, value in message.items():
                if isinstance(value, np.ndarray):
                    message[key] = value.tolist()
        elif hasattr(message, "__str__") and callable(getattr(message, "__str__")):
            message = str(message)

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
