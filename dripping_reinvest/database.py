from functools import wraps
from pathlib import Path
from typing import cast
from tinydb import TinyDB
from . import Func, die, exception_decorator, log
from .constants import INITIAL_DIVIDENDS_THRESHOLD

class Database():

    def __init__(self, json_file: Path) -> None:
        self._db = TinyDB(json_file)
        if not self._db.all():
            log.debug('Empty databse, initializing..')
            self._init_database()

    def _init_database(self):
        self._db.insert({
            'dividends_threshold': INITIAL_DIVIDENDS_THRESHOLD
        })

    @property
    def _dict(self) -> dict:
        return self._db.all()[0]

    def _db_exc_decorator(func: Func) -> Func:
        @wraps(func)
        def wrapper(self):
            try:
                return func(self)
            except KeyError as e:
                die(f'Broken database, key not found: {func.__name__}')
        return cast(Func, wrapper)

    @property
    @_db_exc_decorator
    def dividends_threshold(self) -> float:
        return self._dict['dividends_threshold']

    @dividends_threshold.setter
    def dividends_threshold(self, value: float) -> None:
        self._db.update({'dividends_threshold': value})
        log.info(f'Dividends threshold changed to: {value}%')

