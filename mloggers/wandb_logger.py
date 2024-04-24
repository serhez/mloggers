from typing import Any

import numpy.typing as npt
import wandb
from omegaconf import DictConfig
from termcolor import colored

from mloggers._log_levels import LogLevel
from mloggers.logger import Logger


class WandbLogger(Logger):
    """Logs to Weights & Biases."""

    def __init__(
        self,
        project: str,
        group: str,
        experiment: str,
        default_priority: LogLevel | int = LogLevel.INFO,  # type:ignore[reportArgumentType]
        config: DictConfig | None = None,
    ):
        """
        Initializes a Weights & Biases logger.

        ### Parameters
        ----------
        `project`: the name of the project to log to.
        `group`: the name of the group to log to.
        `experiment`: the name of the experiment to log to.
        `default_priority`: the default log level priority to use.
        [optional] `config`: the configuration of the experiment.
        """

        super().__init__(default_priority)

        if config is not None:
            config = vars(config)
        wandb.init(project=project, group=group, name=experiment, config=config)

    def log(
        self,
        *messages: str | dict[str, Any] | list[Any] | npt.NDArray[Any],
        level: LogLevel | str | None = None,
        **kwargs: Any,
    ):
        if not super(WandbLogger, self).log(*messages, level=level, **kwargs):
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

        if isinstance(message, dict):
            log = message
        else:
            message = str(
                message
            )  # This should be safe here as the super should have already checked that the message is a string or has a __str__ method.
            if level is not None:
                level_str = (
                    level.name if isinstance(level, LogLevel) else str(level).upper()
                )
                log = {level_str: message}
            else:
                log = {"message": message}

        try:
            wandb.log(log)
        except Exception as e:
            print(
                f'{colored("[ERROR]", "red")} [WandbLogger] Error while logging to wandb: {e}'
            )

    def __del__(self):
        """Finishes the connection with W&B."""

        wandb.finish()
