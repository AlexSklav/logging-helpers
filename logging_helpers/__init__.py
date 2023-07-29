# coding: utf-8
import contextlib
import inspect
import logging

from ._version import get_versions

__version__ = get_versions()['version']
del get_versions


@contextlib.contextmanager
def logging_restore(clear_handlers: bool = False) -> None:
    """
    Save logging state upon entering the context and restore upon leaving.

    Parameters
    ----------
    clear_handlers : bool, optional
        If True, clear active logging handlers while within context.

    Example
    -------
    Set logging level to DEBUG, set logging level to INFO within context,
    and verify logging level is restored to DEBUG upon exiting context.

    import logging_helpers as lh
    import logging
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('hello, world!')
        DEBUG:root:hello, world!
    with lh.logging_restore():
        logging.root.setLevel(logging.INFO)
    logging.debug('hello, world!')
        DEBUG:root:hello, world!
    """
    handlers = logging.root.handlers[:]
    level = logging.root.getEffectiveLevel()
    if clear_handlers:
        for h in handlers:
            logging.root.removeHandler(h)
    yield
    handlers_to_remove = logging.root.handlers[:]
    [logging.root.removeHandler(h) for h in handlers_to_remove]
    [logging.root.addHandler(h) for h in handlers]
    logging.root.setLevel(level)


def _get_caller_name(skip: int = 0) -> str:
    """
    Get the name of the caller function based on the number of stack frames to skip.

    Parameters
    ----------
    skip : int, optional
        The number of levels of stack to skip while getting the caller's name.
        skip=0 means the immediate caller's name, skip=1 "who calls me", skip=2 "who calls my caller", etc.
        Default is 0 (get the immediate caller's name).
        (For legacy compatibility. Note that using `skip` might not always produce
        the expected results in complex scenarios with decorators or dynamically
        generated code.)

    Returns
    -------
    str
        The name of the caller function.
    """
    stack = inspect.stack()
    try:
        if len(stack) > skip + 1:
            caller_frame = stack[skip + 1]
            caller_name = caller_frame.function
        else:
            caller_name = ""
    finally:
        del stack
    return caller_name


def _L(skip: int = 0) -> logging.Logger:
    """
    Get the logger for the current function frame.

    Parameters
    ----------
    skip : int, optional
        The number of levels of stack to skip while getting the caller's name.
        skip=1 means "who calls me", skip=2 "who calls my caller", etc.
        Default is 0 (get the immediate caller's name).
        (For legacy compatibility. Note that using `skip` might not always produce
        the expected results in complex scenarios with decorators or dynamically
        generated code.)
    """
    caller_name = _get_caller_name(skip + 1)  # Add 1 to skip to account for _L function itself.
    return logging.getLogger(caller_name)
