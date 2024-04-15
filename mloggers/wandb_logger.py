from typing import Any

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
        default_level: LogLevel | int = LogLevel.INFO,  # type:ignore[reportArgumentType]
        config: DictConfig | None = None,
    ):
        """
        Initializes a Weights & Biases logger.

        ### Parameters
        ----------
        `project`: the name of the project to log to.
        `group`: the name of the group to log to.
        `experiment`: the name of the experiment to log to.
        `default_level`: the default log level to use.
        [optional] `config`: the configuration of the experiment.
        """

        super().__init__(default_level)

        if config is not None:
            config = vars(config)
        wandb.init(project=project, group=group, name=experiment, config=config)

    def log(
        self,
        message: str | dict[str, Any],
        level: LogLevel | str | None = None,
        *args: Any,
        **kwargs: Any,
    ):
        if not super(WandbLogger, self).log(message, level, *args, **kwargs):
            return

        if isinstance(message, dict):
            log = message
        else:
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
