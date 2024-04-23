from mloggers.logger import Logger


class OptionalLogger(Logger):
    """
    A wrapper for a logger which can be `None`.
    This object can be useful library-side to not force your users to use `mloggers`.
    The benefit of this wrapper is that you never have to use `if logger is not None:` again!

    Example:
    ```python
    from mloggers import Logger, OptionalLogger

    def some_function(logger: Logger | None):
        my_logger = OptionalLogger(logger)

        # If the logger is None, nothing will happen (not even an error)
        my_logger.info("This will only log if the logger is not None.")
    ```
    """

    def __init__(self, logger: Logger | None = None):
        """
        Initialize the OptionalLogger.

        ### Parameters
        - [optional] `logger`: the logger to wrap.
        """

        # Hopefully this name is unique enough
        self.__internal_wrapped_logger__ = logger

    def log(self, _):
        pass

    def __getattribute__(self, attr: str):
        """Re-route all attribute access to the logger if it exists."""

        if attr == "__internal_wrapped_logger__":
            return object.__getattribute__(self, attr)

        try:
            return getattr(self.__internal_wrapped_logger__, attr)
        except AttributeError:
            return lambda *_: None
