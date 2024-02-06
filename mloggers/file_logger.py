import json
import os
from datetime import datetime
from typing import Any, Dict, Optional, Union

import numpy as np
from termcolor import colored

from mloggers._log_levels import LogLevel
from mloggers.logger import Logger


class FileLogger(Logger):
    """Logs to a file."""

    def __init__(self, file_path: str):
        """
        Initializes a file logger.

        ### Parameters
        ----------
        `file_path` -> the path to the file to log to.
        - The file will be created if it does not exist. If it does, the logs will be appended to it.
        """

        # Create the file if it does not exist
        if not os.path.exists(file_path):
            with open(file_path, "w") as file:
                file.write("[]")

        print(f'{colored("[INFO]", "cyan")} Logging to file {file_path}')

        self._file_path = file_path

    def log(
        self,
        message: Union[str, Dict[str, Any]],
        level: Optional[Union[LogLevel, str]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        super(FileLogger, self).log(message, level, *args, **kwargs)

        # Convert numpy's ndarrays to lists so that they are JSON serializable
        if isinstance(message, dict):
            for key, value in message.items():
                if isinstance(value, np.ndarray):
                    message[key] = value.tolist()
        elif hasattr(message, "__str__") and callable(getattr(message, "__str__")):
            message = str(message)

        try:
            with open(self._file_path) as file:
                try:
                    logs = json.load(file)
                except json.decoder.JSONDecodeError:
                    print(
                        f'{colored("[ERROR]", "red")} Could not read the log file. Logs will not be saved.'
                    )

            log = {
                "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "message": message,
            }
            if level is not None:
                log["level"] = level.name if isinstance(level, LogLevel) else str(level).upper()
            logs.append(log)

            with open(self._file_path, "w") as file:
                file.seek(0)
                json.dump(logs, file, indent=4)

        except Exception as e:
            print(
                f'{colored("[ERROR]", "red")} Exception thrown while logging to a file: {e}'
            )
