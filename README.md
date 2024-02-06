# MLoggers

This package offers a collection of loggers well-suited for machine learning experiments.

## Getting started

You can download the package via `pip install mloggers`. Dependencies include:

- `numpy`
- `termcolor`
- `wandb` (for integration with Weights & Biases)
- `omegaconf` (for integration with Hydra via Weights & Biases)

## Usage

Example usage (with Hydra integration):

```python
import time

import hydra
from omegaconf import DictConfig

from mloggers import ConsoleLogger, MultiLogger, WandbLogger


@hydra.main(version_base=None, config_path="configs", config_name="train")
def main(config: DictConfig):
    run_id = str(int(time.time()))

    # Create a multi-logger
    logger = MultiLogger(
        [
            ConsoleLogger(),
            WandbLogger(
                config.project_name,
                config.group_name,
                config.experiment_name + "_" + run_id,
                config,
            ),
        ],
        default_mask=[WandbLogger],
    )

    # Run an experiment
    logger.info("Starting the experiment")
    try:
        # `run_experiment` returns a dictionary of results
        results = run_experiment(config, logger)
    except Exception as e:
        logger.error({"Exception occurred during training": e})
        results = {}

    # Log the experiment results
    logger(results, mask=[ConsoleLogger])
```

### Built-in loggers

At this moment, the built-in loggers are:

- `Filelogger`: records logs to a file.
- `ConsoleLogger`: records logs to the console.
- `WandbLogger`: sends logs to a Weights & Biases project; requires an API key.
- `MultiLogger`: aggregates any/all of the above loggers to record the same messages through multiple channels in a single `log()` call.

The available methods to log messages are:

- `log(message, level)`: logs a message of a given `LogLevel` (`INFO`, `WARN`, `ERROR`, `DEBUG` or a custom level).
- `info(message, mask)`: wrapper to call `log(message, LogLevel.INFO)`.
- `warn(message, mask)`: wrapper to call `log(message, LogLevel.WARN)`.
- `error(message, mask)`: wrapper to call `log(message, LogLevel.ERROR)`.
- `debug(message, mask)`: wrapper to call `log(message, LogLevel.DEBUG)`.

### Masks

Masks are used by the `MultiLogger` to filter loggers which are not supposed to record a given message. At the time of initialization, you can define a default mask to use for all messages for which a mask is not specified when calling `MultiLogger.log(message, level, mask)`. To create a mask, simply pass as argument a list of the class references for the loggers you would like to mask out.

### Customized loggers

You can extend the base class `Logger` in order to create a custom logger to suit your own needs. Make sure to implement all abstract methods.

### Customized log levels

You can register new log levels by using `register_level(level, color)`. Once you register a level `"MyLevel"`, you can use it as `logger.log(message, LogLevel.MYLEVEL)`. The method `log` also supports a string as a level, which will be upper-cased and given a default color; the level can also be `None`, which will simply log the message as a stand-alone.
