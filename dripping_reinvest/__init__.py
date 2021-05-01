import os
import sys
import traceback
import atexit
import colorlog
import logging
from functools import wraps
from typing import Any, Callable, TypeVar, cast

IMPORTANT_LEVELNO = 21

def _important(self, message: str, *args, **kws) -> None:
    if self.isEnabledFor(IMPORTANT_LEVELNO):
        self._log(IMPORTANT_LEVELNO, message, args, **kws)

logging.addLevelName(IMPORTANT_LEVELNO, "INFO")
logging.Logger.important = _important

Func = TypeVar('Func', bound=Callable[..., Any])

def _init_logger() -> logging.Logger:
    log_format = '{log_color}[{asctime}][{levelname}] {message}'
    log_time_format = '%Y-%m-%d %H:%M:%S'
    log_colors = {
        'DEBUG':    'reset',
        'INFO':     'reset',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bold',
    }

    formatter = colorlog.ColoredFormatter(log_format, log_time_format, '{', log_colors)

    lh = colorlog.StreamHandler()
    lh.setFormatter(formatter)
    lg = colorlog.getLogger(__file__)
    lg.setLevel(logging.INFO)
    lg.addHandler(lh)
    return lg

def die(msg=None, *args, code=1) -> None:
    if msg:
        log.critical(str(msg), *args)
    sys.exit(code)

def exception_decorator(die_enabled=False) -> Func:
    def actual_exception_decorator(func: Func) -> Func:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                exc_frame = traceback.extract_stack()[-2]
                exc_msg   = f'{os.path.basename(exc_frame.filename)}:{exc_frame.lineno}:{exc_frame.name}(): {e}'
                if die_enabled:
                    die(exc_msg)
                log.error(exc_msg)
        return cast(Func, wrapper)
    return cast(Func, actual_exception_decorator)

@atexit.register
def exit_func() -> None:
    log.debug('Script exited')

log = _init_logger()
