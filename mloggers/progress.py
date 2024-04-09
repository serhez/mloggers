from typing import Iterable, Sequence

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


# TODO: Improve, maybe with live display and support for nested progress bars
def log_progress(iterable: Iterable | Sequence):
    """
    Log an iterable or sequence using a progress bar.
    Wraps `rich.progress.Progress.track`.

    ### Parameters
    ----------
    `iterable`: the iterable whose progress to log.

    ### Returns
    -------
    The tracked iterable.
    """

    bar = Progress(
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        BarColumn(),
        MofNCompleteColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
        expand=True,
    )
    bar.__enter__()
    return bar.track(iterable)
