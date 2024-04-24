# MLoggers

This package offers a collection of loggers well-suited for machine learning experiments.

## Getting started

You can download the package via `pip install mloggers`. Python version $\geq$ 3.10 is required. Dependencies include:

- `aenum`
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
- `info(message)`: wrapper to call `log(message, LogLevel.INFO)`.
- `warn(message)`: wrapper to call `log(message, LogLevel.WARN)`.
- `error(message)`: wrapper to call `log(message, LogLevel.ERROR)`.
- `debug(message)`: wrapper to call `log(message, LogLevel.DEBUG)`.

In the case of the `MultiLogger`, the methods above have the additional optional argument `mask`, which can be used to prevent the given message from being propagated through the masked loggers.

All logging functions support multiple arguments, similar to the print function. For example, `logger.info("The value of x is ", x)` will log the message `"The value of x is 42"` if `x = 42`.
The input messages can also be a series of dictionaries, which will be all logged in separate log entries. If the logger is given both a dictionary and a string, it will fail.

### Masks

Masks are used by the `MultiLogger` to filter loggers which are not supposed to record a given message. At the time of initialization, you can define a default mask to use for all messages for which a mask is not specified when calling `MultiLogger.log(message, level, mask)` or the level-specific variants. To create a mask, simply pass as argument a list of the class references for the loggers you would like to mask out.

### Level filtering

Any logger is initialized with a `default_priority` argument, which is set to `LogLevel.INFO` by default. `LogLevel` elements have an `importance` attribute, which defines a hierarchy of levels. When a logger is initialized with a given level, it will only log messages with a level of equal or higher importance. For example, if a logger is initialized with `LogLevel.WARN`, it will log messages with levels `WARN` and `ERROR`, but not `INFO` or `DEBUG`.

The importance values for the built-in levels are:

- `DEBUG`: -1
- `INFO`: 0
- `WARN`: 1
- `ERROR`: `sys.maxsize` (a very large number, as errors should always be logged)

### Progress bars

You can make use of a pre-configured wrapper of the progress bars provided by the package `rich.progress`. The wrapper is provided via the function `mloggers.progress.log_progress`. Example usage:

```python
import time
from mloggers.progress import log_progress

for _ in log_progress(range(100)):
    time.sleep(0.1)
```

### Customized loggers

You can extend the base class `Logger` in order to create a custom logger to suit your own needs. Make sure to implement all abstract methods.

### Customized log levels

You can register new log levels by using `register_level(level, color)`. Once you register a level `"MyLevel"`, you can use it as `logger.log(message, LogLevel.MYLEVEL)`. The method `log` also supports a string as a level, which will be upper-cased and given a default color; the level can also be `None`, which will simply log the message as a stand-alone.

### Optional loggers
This library also includes a wrapper around the `Logger` class called `OptionalLogger`, which allows you to use a logger which could be `None` without having to check its validity before every use. Hence, instead of this:

```python
from mloggers import Logger


class MyClass:
    def __init__(self, logger: Logger | None):
        self._logger = logger

    def my_function(self):
        if self._logger is not None:
            self._logger.info("Message")
```

You can do this:

```python
from mloggers import Logger, OptionalLogger


class MyClass:
    def __init__(self, logger: Logger | None):
        self._logger = OptionalLogger(logger)

    def my_function(self):
        self._logger.info("Message")
```

If the logger is `None`, nothing will happen (not even an error!).
