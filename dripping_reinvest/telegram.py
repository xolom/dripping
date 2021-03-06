import logging
from typing import List, Optional, Union
from strip_ansi import strip_ansi
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.constants import PARSEMODE_MARKDOWN
from telegram.message import Message
from web3 import Web3

from . import exception_decorator, log, STICKY_LEVELNO
from .database import Database
from .dripping import DrippingAccount
from .utils import parse_float, get_usd_per_drip

"""
Logging formatter to manipulate log messages in a way to make it more readable
"""
class TelegramLogFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        if record.levelno in [logging.ERROR, logging.WARNING]:
            record.msg = f'{record.levelname}: {record.msg}'

        if record.levelno == STICKY_LEVELNO:
            record.msg = record.msg.replace(', ', '\n')

        record.msg = f'`{strip_ansi(record.msg)}`'

        return super(TelegramLogFormatter , self).format(record)

"""
Logging handler for logging to telegram
"""
class TelegramLogHandler(logging.StreamHandler):

    def __init__(self, bot) -> None:
        super().__init__()
        self._bot = bot

    def emit(self, record: logging.LogRecord) -> None:
        self._bot.send_message(self.format(record), record.levelno == STICKY_LEVELNO)

"""
Telegram bot wrapper class for convinient bot usage with pre-defined user
"""
class TelegramBot():

    def __init__(self, db: Database, w3: Web3, drip_acc: DrippingAccount, token: str, user: Union[str, int]) -> None:
        self._db         = db
        self._w3         = w3
        self._drip_acc   = drip_acc
        self._bot        = Updater(token)
        self._user       = user
        self._sticky_msg = None
        self._init_logger()
        self._init_commands()
        self._bot.logger.disabled = True
        self._bot.start_polling()

    def _error_handler(self, update: object, context: CallbackContext) -> None:
        log.error(context.error.message)

    def _init_commands(self) -> None:
        dispatcher = self._bot.dispatcher
        dispatcher.add_error_handler(self._error_handler)
        dispatcher.add_handler(CommandHandler("drip_price", self._cmd_drip_price))
        dispatcher.add_handler(CommandHandler("total_reinvested", self._cmd_total_reinvested))
        dispatcher.add_handler(CommandHandler("set_dividends_thres", self._set_dividends_thres))
        dispatcher.add_handler(CommandHandler("get_dividends_thres", self._get_dividends_thres))

    def _init_logger(self) -> None:
        lh = TelegramLogHandler(self)
        lh.setFormatter(TelegramLogFormatter())
        log.addHandler(lh)

    def _parse_float_arg(self, msg: Message, args: List[str]) -> Optional[float]:
        if len(args) != 1:
            msg.reply_markdown('Invalid number of arguments!')
            return None

        val = parse_float(args[0])
        if not val:
            msg.reply_markdown('Unable to parse float value!')
            return None

        return val

    @exception_decorator()
    def _cmd_drip_price(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_markdown(f'`DRIP price: ${get_usd_per_drip(self._w3):.2f}`')

    @exception_decorator()
    def _cmd_total_reinvested(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_markdown(f'`Total reinvested: {self._drip_acc.reinvested:.2f} DRIP`')

    @exception_decorator()
    def _get_dividends_thres(self, update: Update, context: CallbackContext) -> None:
        msg = update.message or update.edited_message
        msg.reply_markdown(f'`Dividends threshold: {self._db.dividends_threshold}%`')

    @exception_decorator()
    def _set_dividends_thres(self, update: Update, context: CallbackContext) -> None:
        msg = update.message or update.edited_message
        val = self._parse_float_arg(msg, context.args)
        if val:
            self._db.dividends_threshold = val

    @exception_decorator()
    def send_message(self, msg: str, sticky = False) -> None:
        if sticky and self._sticky_msg:
            self._sticky_msg.delete()

        message = self._bot.bot.send_message(self._user, text=msg, parse_mode=PARSEMODE_MARKDOWN)

        if sticky:
            self._sticky_msg = message
