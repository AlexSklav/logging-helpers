import contextlib
import logging


@contextlib.contextmanager
def logging_restore():
    '''
    Save logging state upon entering context and restore upon leaving.

    Example
    -------

    Set logging level to ``DEBUG``, set logging level to ``INFO`` within
    context, and verify logging level is restored to ``DEBUG`` upon exiting
    context.

    >>> import logging_helpers as lh
    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG)
    >>> logging.debug('hello, world!')
    DEBUG:root:hello, world!
    >>> with lh.logging_restore():
    ...     logging.root.setLevel(logging.INFO)
    ...
    >>> logging.debug('hello, world!')
    DEBUG:root:hello, world!

    '''
    handlers = logging.root.handlers[:]
    level = logging.root.getEffectiveLevel()
    yield
    handlers_to_remove = logging.root.handlers[:]
    [logging.root.removeHandler(h) for h in handlers_to_remove]
    [logging.root.addHandler(h) for h in handlers]
    logging.root.setLevel(level)
