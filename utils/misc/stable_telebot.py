# -*- coding: utf-8 -*-
import functools
import time
from telebot import TeleBot
from typing import Callable
import utils.misc.project_logging as logging


def stable_methods_dec(func: Callable) -> Callable:
    """(RU) Декоратор для обработки ошибок при выполнении функции(метода)
    для обеспечения выполнения этой функции(метода).\n
    (EN) Decorator for handling errors when executing a function(method)
    for supplying stable performing of the function(method)"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> None:
        while True:
            chat_id = None
            try:
                if len(args) > 1:
                    _, chat_id, *_ = args
                else:
                    chat_id = kwargs.get('chat_id')
                func(*args, **kwargs)
                break
            except Exception as ex:
                if ex:
                    ex_str = str(ex)
                    if 'Error code: 429' in ex_str:
                        *_, term_of_ban = ex_str.split()
                        logging.logger_main.debug(f"Too many requests per time to Telegram from user {chat_id}.\n"
                                                  f"Error code: 429\n{ex_str}\nBanned for: {term_of_ban}s")
                        time.sleep(int(term_of_ban) + 1)
                    elif 'Error code: 400' in ex_str:
                        logging.logger_main.debug(f"Bad Request to Telegram. Error code: 400\n{ex_str}")
                    else:
                        logging.logger_main.error(f"An unrecoverable error occurred while sending "
                                                  f"data to Telegram API.\n{ex_str}")
                        break
    return wrapper


class StableTeleBot(TeleBot):
    """(RU) Данный класс содержит несколько декорированных
    методов родительского класса TeleBot.\n
    (EN) This class contains several decorated methods
    of the parent class TeleBot"""

    def __init__(self, *args, **kwargs):
        TeleBot.__init__(self, *args, **kwargs)

    send_message = stable_methods_dec(TeleBot.send_message)
    send_media_group = stable_methods_dec(TeleBot.send_media_group)
    register_next_step_handler = stable_methods_dec(TeleBot.register_next_step_handler)
