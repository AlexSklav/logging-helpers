# coding: utf-8
import contextlib
import inspect
import logging
import os
import sys


@contextlib.contextmanager
def logging_restore(clear_handlers=False):
    '''
    Save logging state upon entering context and restore upon leaving.

    Parameters
    ----------
    clear_handlers : bool, optional
        If ``True``, clear active logging handlers while within context.

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
    if clear_handlers:
        for h in handlers:
            logging.root.removeHandler(h)
    yield
    handlers_to_remove = logging.root.handlers[:]
    [logging.root.removeHandler(h) for h in handlers_to_remove]
    [logging.root.addHandler(h) for h in handlers]
    logging.root.setLevel(level)


def _L(skip=0):
    '''Shorthand to get logger for current function frame.'''
    return logging.getLogger(caller_name(skip + 1))


# Public Domain, i.e. feel free to copy/paste
# Considered a hack in Python 2
#
# Ported from [here][1].
# See [here][2] for modifications.
#
# [1]: https://gist.github.com/techtonik/2151727
# [2]: https://gist.github.com/techtonik/2151727#gistcomment-2333747
def caller_name(skip=2):
    """
    Get a name of a caller in the format module.class.method

    `skip` specifies how many levels of stack to skip while getting caller
    name. skip=1 means "who calls me", skip=2 "who calls my caller" etc.

    An empty string is returned if skipped levels exceed stack height


    .. versionchanged:: X.X.X
        When executing from a frozen executable, infer module name from
        filename since :func:`inspect.getmodule` is ~20x slower (~1.5 ms vs 80
        µs) when called from a frozen executable versus calling from source.
    """
    def stack_(frame):
        framelist = []
        while frame:
            framelist.append(frame)
            frame = frame.f_back
        return framelist

    stack = stack_(sys._getframe(1))
    start = 0 + skip
    if len(stack) < start + 1:
        return ''
    parentframe = stack[start]

    name = []
    if getattr(sys, 'frozen', False):
        # Executing from a frozen executable.

        # Infer module name from filename since `inspect.getmodule` is ~20x
        # slower (~1.5 ms vs 80 µs) when called from a frozen executable versus
        # calling from source.
        filename = os.path.normpath(parentframe.f_code.co_filename)
        path_parts = filename.split(os.sep)
        module_name = '.'.join(path_parts[:-1] +
                               [os.path.splitext(path_parts[-1])[0]])
        name.append(module_name)
    else:
        module = inspect.getmodule(parentframe)
        # `modname` can be None when frame is executed directly in console
        # TODO(techtonik): consider using __main__
        if module:
            name.append(module.__name__)
    # detect classname
    if 'self' in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals['self'].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != '<module>':  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return ".".join(name)
