# -*- coding: utf-8 -*-
from typing import Callable, List, Any, Optional
import functools
import json
from data import config as cfg
import datetime as dt
import time
import sqlite3 as db


def requests_cache(ttl: int) -> Callable:
    """(RU) Обёртка для кэширующего декоратора, передающая в него
    параметр времени жизни записей кэширующей базы данных.\n
    (EN) It's a wrapper for caching decorator, it passes Time-To-Live
    parameter of cached DB records into the decorator"""
    def cache_decorator(func: Callable) -> Callable:
        """(RU) Декоратор для кэширования HTTP API запроса в БД.\n
        (EN) It's a decorator for putting to DB a cached HTTP API request"""
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs) -> dict:
            cached_key: str = f"{json.dumps(args, ensure_ascii=False)}, " \
                              f"{json.dumps(kwargs, ensure_ascii=False)}"
            with db.connect(cfg.DB_CACHED) as conn:
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        CREATE TABLE `cached_requests` (
                            `time_id` REAL NOT NULL PRIMARY KEY,
                            `cached_key` TEXT,
                            `request_result` TEXT
                        );
                    """)
                except db.OperationalError:
                    pass
                finally:
                    # To delete records with expired term of keeping, i.e. more than ttl
                    cursor.execute(
                        "DELETE FROM `cached_requests` WHERE (?) - `time_id` > (?);",
                        (time.time(), ttl))
                    # To delete records, which contain an API service message or an error code, but not data
                    cursor.execute(
                        """DELETE FROM `cached_requests` WHERE 
                        (`request_result` LIKE (?) OR `request_result` LIKE (?) OR
                         `request_result` LIKE (?) OR `request_result` LIKE (?));""",
                        ('%message%', '401', '403', '429',))
                    # To get a cached record from DB
                    cursor.execute(
                        "SELECT `request_result` FROM `cached_requests` WHERE `cached_key`=(?);",
                        (cached_key,))
                    data: tuple = cursor.fetchone()
                    if data:
                        result_db, *_ = data
                        result: dict = json.loads(result_db)
                    else:
                        result: dict = func(*args, **kwargs)
                        result_db: str = json.dumps(result, ensure_ascii=False)
                        cursor.execute(
                            """INSERT INTO `cached_requests` (`time_id`, `cached_key`, `request_result`) 
                            values(?, ?, ?);""",
                            (time.time(), cached_key, result_db))
                    return result

        return wrapped_func
    return cache_decorator


def save_history(chat_id: int, user_command: str,
                 params: str, result: Optional[list]) -> None:
    """(RU) Сохраняет в БД историю команд пользователя Telegram и результатов выполнения.\n
    (EN) To save in DB a Telegram-user commands history and performed results

    :param chat_id: ID for selecting records
    :param user_command: A command from the Telegram chat
    :param params: A JSON string of serialized dictionary containing parameters
    :param result: A JSON string of serialized list of lists containing the result
    """
    if result is None:
        result: list = list()
    with db.connect(cfg.DB_CACHED) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                CREATE TABLE `tg_history` (
                    `time_id` REAL NOT NULL PRIMARY KEY,
                    `chat_id` INTEGER,
                    `user_command` TEXT,
                    `params` TEXT,
                    `result` TEXT NOT NULL
                );
            """)
        except db.OperationalError:
            pass
        finally:
            result_db: str = json.dumps(result, ensure_ascii=False)
            cursor.execute(
                """INSERT INTO `tg_history` (`time_id`, `chat_id`, `user_command`, `params`, `result`) 
                values(?, ?, ?, ?, ?);""",
                (time.time(), chat_id, user_command, params, result_db))


def get_history(chat_id: int) -> List[str]:
    """(RU) Получает из БД историю команд пользователя Telegram и результатов выполнения.\n
    (EN) To get a Telegram-user commands history and performed results from DB

    :param chat_id: ID for selecting records
    :return Returns a list of strings if data or None if an error
    """
    get_history_lst: list = []
    with db.connect(cfg.DB_CACHED) as conn:
        cursor = conn.cursor()
        try:
            # To delete records, which contain an error code, but not data
            cursor.execute(
                """DELETE FROM `tg_history` WHERE 
                (`result` LIKE (?) OR `result` LIKE (?) OR `result` LIKE (?));""",
                ('401', '403', '429',))
            cursor.execute(
                """SELECT `time_id`, `user_command`, `params`, `result` FROM `tg_history` 
                WHERE `chat_id`=(?) LIMIT 1000;""", (chat_id,))
            data: List[tuple] = cursor.fetchall()
            for record in data:
                time_id, user_command, params, result = record
                date_time: str = dt.datetime.utcfromtimestamp(time_id).strftime('%d.%m.%Y  %H:%M:%S (UTC)')
                params_text: str = '\n'.join(f"{k} {v}" for k, v in json.loads(params).items())
                res: list = json.loads(result)
                if res:
                    hotels_data: str = '\n'.join([f"{idx + 1}. {val.pop()}\n"
                                                  for idx, val in enumerate(res)])
                else:
                    hotels_data: str = cfg.TB_LEX[get_prm(chat_id, 'locale')]['req_failure']
                get_history_lst.append(
                    f"{cfg.API_LEX[get_prm(chat_id, 'locale')]['cmd_date_time']}\n{date_time}\n\n"
                    f"{cfg.API_LEX[get_prm(chat_id, 'locale')]['user_command']} {user_command}\n\n"
                    f"{cfg.API_LEX[get_prm(chat_id, 'locale')]['params']}\n{params_text}\n\n"
                    f"{cfg.API_LEX[get_prm(chat_id, 'locale')]['request_result']}\n{hotels_data}\n")
        except db.OperationalError:
            pass
        finally:
            return get_history_lst


def delete_history(chat_id: int, delete_all: bool) -> None:
    """(RU) Удаляет из БД записи истории команд пользователя Telegram и результатов выполнения.
    (EN) To delete a Telegram-user commands history and performed results from DB

    :param chat_id: ID for selecting records
    :param delete_all: Delete all records if True
    """
    with db.connect(cfg.DB_CACHED) as conn:
        cursor = conn.cursor()
        try:
            if delete_all:
                cursor.execute("DELETE FROM `tg_history`;")
            else:
                cursor.execute("DELETE FROM `tg_history` WHERE `chat_id`=(?);", (chat_id,))
        except db.OperationalError:
            pass


def save_prm(chat_id: int, param_name: str, param_value: Any) -> None:
    """(RU) Сохраняет в БД для определенного Telegram-пользователя
    один из предустановленных параметров.\n
    (EN) To save in DB one of determined parameters for a certain Telegram-user

    :param chat_id: ID for selecting records
    :param param_name: Name of the parameter
    :param param_value: Value of the parameter
    """

    if param_name not in cfg.DB_DEFAULTS.keys():
        raise Exception(f"ERROR: Parameter '{param_name}' was not found in the default "
                        f"parameters list:\n{cfg.DB_DEFAULTS.keys()}")
    else:
        if type(param_value) is bool:
            param_value: int = int(param_value)
        with db.connect(cfg.DB_CACHED) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    CREATE TABLE `chat_properties` (
                        `chat_id` INTEGER NOT NULL PRIMARY KEY,
                        `locale` TEXT,
                        `currency` TEXT,
                        `sort_order` TEXT,
                        `city` TEXT,
                        `city_id` TEXT,
                        `check_in_date` TEXT,
                        `check_out_date` TEXT,
                        `price_min` INTEGER,
                        `price_max` INTEGER,
                        `dist_min` REAL,
                        `dist_max` REAL,
                        `hotels_qty` INTEGER,
                        `hotels_photos_qty` INTEGER,
                        `is_best_deal` INTEGER,
                        `user_command` TEXT,
                        `chat_state` TEXT
                    );
                """)
                cursor.execute(
                    f"UPDATE `chat_properties` SET `chat_state`=(?) WHERE `chat_id`=(?);",
                    (cfg.DB_DEFAULTS['chat_state'], chat_id))
            except db.OperationalError:
                pass
            finally:
                try:
                    cursor.execute(
                        f"INSERT INTO `chat_properties` (`chat_id`, `{param_name}`) values(?, ?);",
                        (chat_id, param_value))
                except db.IntegrityError:
                    try:
                        cursor.execute(
                            f"UPDATE `chat_properties` SET `{param_name}`=(?) WHERE `chat_id`=(?);",
                            (param_value, chat_id))
                    except Exception as err:
                        if err:
                            raise Exception(f"ERROR: There is a mismatch of `{param_name}` value "
                                            f"while writing to the database")


def get_prm(chat_id: int, param_name: str) -> Any:
    """(RU) Получает из БД значение параметра по ID Telegram-пользователя.
    (EN) To get from DB a parameter value by ID of a Telegram-user

    :param chat_id: ID for selecting records
    :param param_name: Name of the parameter
    :return Returns value of the parameter
    """
    result = None
    with db.connect(cfg.DB_CACHED) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"SELECT `chat_id`, `{param_name}` FROM `chat_properties` WHERE `chat_id`=(?);""",
                (chat_id,))
            data: tuple = cursor.fetchone()
            *_, result = data
        except db.OperationalError:
            pass
        finally:
            if result is not None:
                return result
            else:
                return cfg.DB_DEFAULTS.get(param_name)


def set_chat_state_to_default() -> None:
    """(RU) Устанавливает значение параметра `chat_state` в значение по умолчанию
    для всех имеющихся в БД пользователей Telegram.\n
    (EN) To set `chat_state` parameter value to default value for all Telegram-users kept in DB"""
    with db.connect(cfg.DB_CACHED) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE `chat_properties` SET `chat_state`=(?);",
                           (cfg.DB_DEFAULTS['chat_state'],))
        except db.OperationalError:
            pass
