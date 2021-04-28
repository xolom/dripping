from functools import wraps
from pathlib import Path
from typing import cast
from tinydb import TinyDB
from . import Func, die, exception_decorator, log

class Database():

    def __init__(self, json_file: Path) -> None:
        if not json_file.is_file():
            die(f'Database json does not exist: {json_file}')
        self._db = TinyDB(json_file)

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
        self._db.update(dict(self._dict, dividends_threshold=value))
        log.info(f'Dividends threshold changed to: {value}%')

