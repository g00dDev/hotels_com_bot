# -*- coding: utf-8 -*-
from data import config as cfg
from datetime import datetime, timedelta
import json
from keyboards.default.keyboard import (btn_curr, btn_no, btn_yes, btn_numeric, btn_locales)
import telebot as tb
from telebot.types import ReplyKeyboardRemove, CallbackQuery
import time
from typing import Callable, Optional, Tuple, Union
from utils.misc import stable_telebot as stb
from utils.db_api.models import (get_prm, save_prm, save_history, get_history,
                                 delete_history, set_chat_state_to_default)
from utils.http_api.http_requests import (city_request, hotels_request, hotel_photos_request)
import utils.misc.project_logging as logging
from utils.misc.custom_calendar import CallbackData, AdaptedCalendar


bot = stb.StableTeleBot(cfg.TB_TOKEN, parse_mode='HTML')

set_chat_state_to_default()
calendars: dict = dict()
cal_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


@bot.message_handler(content_types=['text'])
def main_message(msg) -> None:
    """(RU) Обработка всех текстовых команд, отправленных пользователем Telegram.\n
    (EN) To proceed all of text-commands sent by a Telegram-user"""
    msg_text: str = msg.text
    if get_prm(msg.chat.id, 'chat_state') == 'ready':
        if msg_text.lower() in ('/привет', '/hello', '/hello-world'):
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['hello'])
        elif msg_text == "/help":
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['help'],
                             reply_markup=ReplyKeyboardRemove())
        elif msg_text == "/start":
            save_prm(msg.chat.id, param_name='chat_state', param_value='conversation')
            markup = tb.types.ReplyKeyboardMarkup(row_width=len(btn_locales), resize_keyboard=True,
                                                  one_time_keyboard=True)
            markup.add(*btn_locales)
            from_user_req(msg, locale_setup, cfg.TB_START_MSG, reply_markup=markup)
        elif msg_text == "/lowprice":
            save_prm(msg.chat.id, param_name='user_command', param_value=msg_text)
            save_prm(msg.chat.id, param_name='sort_order', param_value=cfg.SORT_ORDER['lowprice'])
            save_prm(msg.chat.id, param_name='chat_state', param_value='conversation')
            from_user_req(msg, city_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['city_req'])
        elif msg_text == "/highprice":
            save_prm(msg.chat.id, param_name='user_command', param_value=msg_text)
            save_prm(msg.chat.id, param_name='sort_order', param_value=cfg.SORT_ORDER['highprice'])
            save_prm(msg.chat.id, param_name='chat_state', param_value='conversation')
            from_user_req(msg, city_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['city_req'])
        elif msg_text == "/bestdeal":
            save_prm(msg.chat.id, param_name='user_command', param_value=msg_text)
            save_prm(msg.chat.id, param_name='sort_order', param_value=cfg.SORT_ORDER['bestdeal'])
            save_prm(msg.chat.id, param_name='is_best_deal', param_value=True)
            save_prm(msg.chat.id, param_name='chat_state', param_value='conversation')
            from_user_req(msg, city_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['city_req'])
        elif msg_text == "/history":
            history: list = get_history(msg.chat.id)
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['history'])
            if history:
                counter: int = 0
                for record in history:
                    counter += 1
                    bot.send_message(msg.chat.id, record, disable_web_page_preview=True)
                    if counter == 5:
                        counter = 0
                        time.sleep(1)
                request_done(msg, err=False)
            else:
                bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['no_history'])
        elif msg_text == "/delete_history":
            delete_history(msg.chat.id, delete_all=False)
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['history_deleted'])
        elif msg_text == "/delete_all_history":
            if msg.chat.id == cfg.ADMIN_ID:
                delete_history(msg.chat.id, delete_all=True)
                bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['history_deleted'])
            else:
                from_user_req(msg, main_message, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['violation'])
        elif msg_text == "/stop":
            if msg.chat.id == cfg.ADMIN_ID:
                bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bot_stopped'])
                bot.stop_bot()
            else:
                from_user_req(msg, main_message, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['violation'])
        else:
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_command'])
    elif (get_prm(msg.chat.id, 'chat_state') == 'check_in_date' or
          get_prm(msg.chat.id, 'chat_state') == 'check_out_date'):
        # During date entry modes any of user messages will be deleted
        bot.delete_message(msg.chat.id, msg.message_id)
    else:
        pass


def locale_setup(msg) -> None:
    """(RU) Установка языка для пользователя Telegram.\n
    (EN) To set locale value for a Telegram-user"""
    locale: str = msg.text
    if locale not in cfg.LOCALES.keys():
        save_prm(msg.chat.id, param_name='locale', param_value=cfg.DB_DEFAULTS.get('locale'))
        logging.logger_main.debug(f"User {msg.chat.id} avoided tapping a LOCALE button!")
        bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['default_locale'])
    else:
        logging.logger_main.info(f"User {msg.chat.id} chose '{locale}' locale button")
        save_prm(msg.chat.id, param_name='locale', param_value=cfg.LOCALES[locale])
        # definition of the bot commands in accordance with chosen language
        bot_set_commands(locale=cfg.LOCALES[locale], chat_id=msg.chat.id)
    markup = tb.types.ReplyKeyboardMarkup(row_width=len(cfg.CURRENCIES) // 2, resize_keyboard=True,
                                          one_time_keyboard=True)
    markup.add(*btn_curr)
    from_user_req(msg, currency_setup, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['choose_currency'],
                  reply_markup=markup)


def currency_setup(msg) -> None:
    """(RU) Установка валюты для пользователя Telegram.\n
    (EN) To set currency value for a Telegram-user"""
    currency: str = msg.text
    if currency.upper() in cfg.CURRENCIES:
        save_prm(msg.chat.id, param_name='chat_state', param_value='ready')
        logging.logger_main.info(f"User {msg.chat.id} chose '{currency}' currency button")
        save_prm(msg.chat.id, param_name='currency', param_value=currency)
        bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['greeting_1'],
                         reply_markup=tb.types.ReplyKeyboardRemove())
        time.sleep(1)
        bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['greeting_2'],
                         disable_web_page_preview=True)
        time.sleep(2)
        from_user_req(msg, main_message, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['help'])
    else:
        logging.logger_main.debug(f"User {msg.chat.id} avoided tapping a CURRENCY button!")
        from_user_req(msg, currency_setup, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_currency'])


def city_req(msg) -> None:
    """(RU) Запрос пользователю Telegram в каком городе производить поиск отелей.\n
    (EN) To ask a Telegram-user to determine a city to search for hotels in"""
    city: str = msg.text
    logging.logger_main.info(f"User {msg.chat.id} specified '{city}' city")
    save_prm(msg.chat.id, param_name='city', param_value=city)
    request_pending(msg)
    # Request to the DB or HTTP API
    result_city: Union[Tuple[str, str], None, int] = city_request(city, msg.chat.id)
    bot.delete_message(msg.chat.id, msg.message_id + 1)
    if result_city:
        if result_city == 429:
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_quota'],
                             disable_web_page_preview=True)
            request_done(msg, err=True)
        elif result_city == 451:
            request_done(msg, err=True, illegal=True)
        else:
            city_name, city_id = result_city
            save_prm(msg.chat.id, param_name='city_id', param_value=city_id)
            markup = tb.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                                  one_time_keyboard=True)
            markup.add(btn_yes[get_prm(msg.chat.id, 'locale')], btn_no[get_prm(msg.chat.id, 'locale')])
            save_prm(msg.chat.id, param_name='chat_state', param_value='assertion')
            from_user_req(msg, is_city_correct,
                          f"{cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['city_chosen']} {city_name}",
                          reply_markup=markup)
    else:
        from_user_req(msg, city_req, f"{cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_city']}.\n"
                                     f"{cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['another_city']}",
                      disable_web_page_preview=True)


def is_city_correct(msg) -> None:
    """(RU) Запрос пользователю о том, верно ли выбран город.\n
    (EN) To ask a Telegram-user to confirm the city choice"""
    assertion: str = msg.text
    logging.logger_main.info(f"User {msg.chat.id} chose '{assertion}' assertion while city choosing")
    if assertion.upper() == cfg.LEX_ASSERTION[get_prm(msg.chat.id, 'locale')]['NO']:
        from_user_req(msg, city_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['another_city'])
    elif msg.text.upper() == cfg.LEX_ASSERTION[get_prm(msg.chat.id, 'locale')]['YES']:
        save_prm(msg.chat.id, param_name='chat_state', param_value='check_in_date')
        date_picker(msg)
    else:
        if get_prm(msg.chat.id, 'chat_state') == 'assertion':
            logging.logger_main.debug(f"User {msg.chat.id} avoided tapping 'YES' or 'NO'"
                                      f" button for city assertion request!")
            from_user_req(msg, is_city_correct, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_assertion'])
        else:
            pass


def pre_hotels_qty_req(msg) -> None:
    """(RU) Вспомогательная функция, предваряющая функцию 'hotels_qty_req'.\n
    (EN) This is an auxiliary function before 'hotels_qty_req' function"""
    markup = tb.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True,
                                          one_time_keyboard=True)
    markup.add(btn_numeric[3], btn_numeric[5], btn_numeric[10], btn_numeric[15],
               btn_numeric[20], btn_numeric[25])
    from_user_req(msg, hotels_qty_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['hotels_qty_req'],
                  reply_markup=markup)


def price_min_req(msg) -> None:
    """(RU) Запрос пользователю Telegram о минимальной цене.\n
    (EN) To ask a Telegram-user to specify minimum price value"""
    price_min: str = msg.text
    if price_min.isdecimal():
        logging.logger_main.info(f"User {msg.chat.id} chose '{price_min}' value for minimum price")
        price_min: int = int(msg.text)
        save_prm(msg.chat.id, param_name='price_min', param_value=price_min)
        from_user_req(msg, price_max_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['price_max_req'])
    else:
        logging.logger_main.info("A positive integer number expected, but got something else!")
        from_user_req(msg, price_min_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_int_number'])


def price_max_req(msg) -> None:
    """(RU) Запрос пользователю Telegram о максимальной цене.\n
    (EN) To ask a Telegram-user to specify maximum price value"""
    price_max: str = msg.text
    if price_max.isdecimal():
        logging.logger_main.info(f"User {msg.chat.id} chose '{price_max}' value for maximum price")
        price_max: int = int(msg.text)
        save_prm(msg.chat.id, param_name='price_max', param_value=price_max)
        if price_max < get_prm(msg.chat.id, 'price_min'):
            logging.logger_main.info("Max price is less than Min price. Must be more or equal!")
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_prices'])
            from_user_req(msg, price_min_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['price_min_req'])
        else:
            from_user_req(msg, dist_min_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['dist_min_req'])
    else:
        logging.logger_main.info("A positive integer number expected, but got something else!")
        from_user_req(msg, price_max_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_int_number'])


def dist_min_req(msg) -> None:
    """(RU) Запрос пользователю Telegram о минимальном расстоянии от отеля до Центра города.\n
    (EN) To ask a Telegram-user to specify minimum distance value from the hotel to the city center"""
    try:
        dist_min: float = float(msg.text)
        save_prm(msg.chat.id, param_name='dist_min', param_value=dist_min)
        from_user_req(msg, dist_max_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['dist_max_req'])
    except ValueError:
        logging.logger_main.info("A float number expected, but got something else!")
        from_user_req(msg, dist_min_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_float_number'])


def dist_max_req(msg) -> None:
    """(RU) Запрос пользователю Telegram о максимальном расстоянии от отеля до Центра города.\n
    (EN) To ask a Telegram-user to specify maximum distance value from a hotel to the city center"""

    try:
        dist_max: float = float(msg.text)
        save_prm(msg.chat.id, param_name='dist_max', param_value=dist_max)
        if dist_max < get_prm(msg.chat.id, 'dist_min'):
            logging.logger_main.info("Max distance is less than Min distance. Must be more or equal!")
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_distances'])
            from_user_req(msg, dist_min_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['dist_min_req'])
        else:
            pre_hotels_qty_req(msg)
    except ValueError:
        logging.logger_main.info("A float number expected, but got something else!")
        from_user_req(msg, dist_max_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_float_number'])


def hotels_qty_req(msg) -> None:
    """(RU) Запрос пользователю Telegram о количестве отелей.\n
    (EN) To ask a Telegram-user to specify quantity of hotels"""
    hotels_qty: str = msg.text
    if hotels_qty.isdecimal():
        logging.logger_main.info(f"User {msg.chat.id} chose '{hotels_qty}' hotels to search for")
        hotels_qty: int = int(msg.text)
        if 0 < hotels_qty <= int(cfg.MAX_PAGE_SIZE):
            save_prm(msg.chat.id, param_name='hotels_qty', param_value=str(hotels_qty))
            hotels_lex: str = (
                cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['hotels_2'],
                cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['hotels_1']
            )[str(hotels_qty)[-1] in ('2', '3', '4')]
            bot.send_message(
                msg.chat.id, f"{cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['seek']} {hotels_qty} {hotels_lex}",
                reply_markup=tb.types.ReplyKeyboardRemove())
            markup = tb.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True,
                                                  one_time_keyboard=True)
            markup.add(btn_yes[get_prm(msg.chat.id, 'locale')], btn_no[get_prm(msg.chat.id, 'locale')])
            save_prm(msg.chat.id, param_name='chat_state', param_value='assertion')
            from_user_req(msg, hotels_need_photos_tg, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['need_photos'],
                          reply_markup=markup)
        else:
            logging.logger_main.debug(f"User {msg.chat.id} avoided tapping a numerical button and "
                                      f"entered an invalid number for hotels quantity!")
            from_user_req(msg, hotels_qty_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['invalid_number'])
    else:
        logging.logger_main.debug(f"User {msg.chat.id} avoided tapping a numerical button "
                                  f"for hotels quantity request!")
        from_user_req(msg, hotels_qty_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_int_number'])


def params_history(msg) -> str:
    """(RU) Формирование JSON-строки из параметров запроса.\n
    (EN) To form a JSON-string from request parameters

    :return Returns a JSON-string
    """
    params_dict: dict = dict()
    city: str = get_prm(msg.chat.id, 'city')
    check_in_date: str = datetime.fromisoformat(get_prm(msg.chat.id, 'check_in_date')).strftime('%d.%m.%Y')
    check_out_date: str = datetime.fromisoformat(get_prm(msg.chat.id, 'check_out_date')).strftime('%d.%m.%Y')
    price_min: int = get_prm(msg.chat.id, 'price_min')
    price_max: int = get_prm(msg.chat.id, 'price_max')
    dist_min: float = get_prm(msg.chat.id, 'dist_min')
    dist_max: float = get_prm(msg.chat.id, 'dist_max')
    params_dict[cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['city_chosen']] = city
    params_dict[cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['history_check_in']] = check_in_date
    params_dict[cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['history_check_out']] = check_out_date
    if get_prm(msg.chat.id, 'is_best_deal'):
        params_dict[cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['history_prices']] = \
            f"{price_min}-{price_max} {get_prm(msg.chat.id, 'currency')}"
        params_dict[cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['history_distances']] = \
            f"{dist_min}-{dist_max} {cfg.TB_DIMENSION[get_prm(msg.chat.id, 'locale')]}"
    return json.dumps(params_dict, ensure_ascii=False)


def nights_qty(msg) -> int:
    """(RU) Вычисляет количество ночей бронирования.\n
    (EN) To count quantity of nights to book in"""
    nights: timedelta = (datetime.fromisoformat(get_prm(msg.chat.id, 'check_out_date')) -
                         datetime.fromisoformat(get_prm(msg.chat.id, 'check_in_date')))
    return int(nights.total_seconds() // 86400)


def hotels_need_photos_tg(msg) -> None:
    """(RU) Запрос пользователю Telegram о необходимости вывести фотографии отелей.\n
    (EN) To ask a Telegram-user if to display hotels photos"""
    assertion: str = msg.text
    if get_prm(msg.chat.id, 'chat_state') == 'assertion':
        logging.logger_main.info(f"User {msg.chat.id} chose '{assertion}' assertion while photo choosing")
    if assertion.upper() == cfg.LEX_ASSERTION[get_prm(msg.chat.id, 'locale')]['NO']:
        request_pending(msg)
        # Request to the DB or HTTP API
        result_hotels: Union[list, None, int] = hotels_request(get_prm(msg.chat.id, 'hotels_qty'),
                                                               get_prm(msg.chat.id, 'city_id'),
                                                               get_prm(msg.chat.id, 'sort_order'),
                                                               get_prm(msg.chat.id, 'price_min'),
                                                               get_prm(msg.chat.id, 'price_max'),
                                                               get_prm(msg.chat.id, 'dist_min'),
                                                               get_prm(msg.chat.id, 'dist_max'), msg.chat.id,
                                                               nights_qty(msg))
        bot.delete_message(msg.chat.id, msg.message_id + 1)
        # Saving commands history
        save_history(msg.chat.id, get_prm(msg.chat.id, 'user_command'), params_history(msg), result_hotels)
        if result_hotels:
            if result_hotels == 429:
                bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_quota'],
                                 disable_web_page_preview=True)
            else:
                params_text: str = '\n'.join(f"{k!s} {v!s}" for k, v in json.loads(params_history(msg)).items())
                bot.send_message(msg.chat.id, params_text)
                bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['hotels_list'])
                bot.send_message(msg.chat.id,
                                 '\n\n'.join(list(map(
                                     str, [f"{idx + 1}. {el[1]}" for idx, el in enumerate(result_hotels)]))),
                                 disable_web_page_preview=True)
                request_done(msg, err=False)
        else:
            request_done(msg, err=True)

    elif msg.text.upper() == cfg.LEX_ASSERTION[get_prm(msg.chat.id, 'locale')]['YES']:
        markup = tb.types.ReplyKeyboardMarkup(row_width=6, resize_keyboard=True, one_time_keyboard=True)
        markup.add(btn_numeric[1], btn_numeric[3], btn_numeric[5], btn_numeric[9], btn_numeric[12],
                   btn_numeric[15], btn_numeric[18], btn_numeric[21], btn_numeric[24], btn_numeric[27],
                   btn_numeric[30], btn_numeric[33])
        save_prm(msg.chat.id, param_name='chat_state', param_value='conversation')
        from_user_req(msg, hotels_photos_qty_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['photos_qty'],
                      reply_markup=markup)
    else:
        if get_prm(msg.chat.id, 'chat_state') == 'assertion':
            logging.logger_main.debug(f"User {msg.chat.id} avoided tapping 'YES' or 'NO' "
                                      f"button for hotels photos request!")
            from_user_req(msg, hotels_need_photos_tg, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_assertion'])
        else:
            pass


def hotels_photos_qty_req(msg) -> None:
    """(RU) Запрос пользователю Telegram о количестве фотографий отелей.
    Если количество фотографий превышает лимит, то фотографии пользователю отправляются блоками,
    пока не будет достигнуто запрошенное количество или пока не будет достигнуто количество,
    имеющееся в наличии.\n
    (EN) To ask a Telegram-user to specify photos quantity of each hotel.
    If asked quantity exceeds the limit, photos to be grouped in blocks and to be sent until
    asked quantity is achieved or existing photos quantity is achieved"""
    hotels_photos_qty: str = msg.text
    if hotels_photos_qty.isdecimal():
        logging.logger_main.info(f"User {msg.chat.id} chose '{hotels_photos_qty}' photos for each hotel")
        hotels_photos_qty: int = int(msg.text)
        if hotels_photos_qty <= len(btn_numeric) - 1:
            save_prm(msg.chat.id, param_name='hotels_photos_qty', param_value=hotels_photos_qty)
            from_user_req(msg, hotels_need_photos_tg,
                          f"{cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['photos_chosen_1']} {hotels_photos_qty} "
                          f"{cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['photos_chosen_2']}",
                          reply_markup=tb.types.ReplyKeyboardRemove())
            request_pending(msg)
            # Request to the DB or HTTP API
            result_hotels: Union[list, None, int] = hotels_request(get_prm(msg.chat.id, 'hotels_qty'),
                                                                   get_prm(msg.chat.id, 'city_id'),
                                                                   get_prm(msg.chat.id, 'sort_order'),
                                                                   get_prm(msg.chat.id, 'price_min'),
                                                                   get_prm(msg.chat.id, 'price_max'),
                                                                   get_prm(msg.chat.id, 'dist_min'),
                                                                   get_prm(msg.chat.id, 'dist_max'),
                                                                   msg.chat.id, nights_qty(msg))
            bot.delete_message(msg.chat.id, msg.message_id + 2)
            # Saving commands history
            save_history(msg.chat.id, get_prm(msg.chat.id, 'user_command'), params_history(msg), result_hotels)
            if result_hotels:
                if result_hotels == 429:
                    bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_quota'],
                                     disable_web_page_preview=True)
                else:
                    params_text: str = '\n'.join(f"{k} {v}" for k, v in json.loads(params_history(msg)).items())
                    bot.send_message(msg.chat.id, params_text)
                    bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['hotels_list'])
                    _hotel_info: str = ''
                    for _idx, _hotel in enumerate(result_hotels):
                        try:
                            _hotel_id, _hotel_info = _hotel
                            bot.send_message(msg.chat.id, f"{_idx + 1}. {_hotel_info}", disable_web_page_preview=True)
                            # Request to the DB or HTTP API
                            _hotel_photos: Optional[list] = hotel_photos_request(_hotel_id, hotels_photos_qty)
                            if _hotel_photos:
                                if result_hotels == 429:
                                    bot.send_message(msg.chat.id,
                                                     cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_quota'],
                                                     disable_web_page_preview=True)
                                    break
                                else:
                                    _media_group: list = [tb.types.InputMediaPhoto(photo_link)
                                                          for photo_link in _hotel_photos]
                                    # Splitting media groups into blocks that do not exceed the length limit
                                    if hotels_photos_qty <= cfg.MEDIA_LIMIT:
                                        bot.send_media_group(msg.chat.id, _media_group)
                                    else:
                                        _media_group_len: int = len(_media_group)
                                        # The number of requested photos is less than the number of photos
                                        # received from the site
                                        if hotels_photos_qty < _media_group_len:
                                            # считаем кол-во блоков:
                                            if hotels_photos_qty % cfg.MEDIA_LIMIT:
                                                media_blocks: int = hotels_photos_qty // cfg.MEDIA_LIMIT + 1
                                            else:
                                                media_blocks: int = hotels_photos_qty // cfg.MEDIA_LIMIT
                                        # The number of requested photos is greater than the number of photos
                                        # received from the site
                                        else:
                                            # counting the number of blocks:
                                            if _media_group_len % cfg.MEDIA_LIMIT:
                                                media_blocks: int = _media_group_len // cfg.MEDIA_LIMIT + 1
                                            else:
                                                media_blocks: int = _media_group_len // cfg.MEDIA_LIMIT
                                        shift: int = 0
                                        for _ in range(media_blocks):
                                            bot.send_media_group(msg.chat.id,
                                                                 _media_group[0 + shift:cfg.MEDIA_LIMIT + shift])
                                            time.sleep(2)
                                            shift += cfg.MEDIA_LIMIT
                            else:
                                bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_photos'])
                            time.sleep(2)
                        except Exception as err:
                            if err:
                                logging.logger_main.critical(
                                    f"Critical error. Can't notify user {msg.chat.id} about the "
                                    f"error and couldn't lead the conversation to the endpoint.\n"
                                    f"{str(err)}")
                                save_prm(msg.chat.id, param_name='chat_state', param_value='ready')
                    request_done(msg, err=False)
            else:
                request_done(msg, err=True)
        else:
            logging.logger_main.debug(f"User {msg.chat.id} avoided tapping a numerical button and "
                                      f"entered an invalid number for hotels photos quantity!")
            from_user_req(msg, hotels_photos_qty_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['invalid_number'])

    else:
        logging.logger_main.debug(f"User {msg.chat.id} avoided tapping a numerical button "
                                  f"for hotel photos quantity request!")
        from_user_req(msg, hotels_photos_qty_req, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['bad_int_number'])


def from_user_req(msg, next_call: Callable, bot_speech: str,
                  disable_web_page_preview: Optional[bool] = None,
                  reply_markup=None) -> None:
    """(RU) Выводит пользователю сообщение и после реакции пользователя
     передаёт управление следующей функции.\n
     (EN) To display to a Telegram-user a message and after the user's response
     to pass management to the next function

    :param msg: Message object
    :param next_call: Next handler
    :param bot_speech: Text shown to the Telegram user
    :param disable_web_page_preview: Boolean, Optional. Disables web preview if a web-link exists.
    :param reply_markup: Reply-markup object or None
    """
    bot.send_message(msg.chat.id, bot_speech, reply_markup=reply_markup,
                     disable_web_page_preview=disable_web_page_preview)
    bot.register_next_step_handler(msg, next_call)


def request_pending(msg) -> None:
    """(RU) Сообщает пользователю, что запрос обрабатывается.\n
    (EN) To inform a Telegram-user that the request is pending"""
    bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['pending'],
                     reply_markup=tb.types.ReplyKeyboardRemove())


def request_done(msg, err: bool, illegal: Optional[bool] = None) -> None:
    """(RU) Сообщает пользователю об успешном или неуспешном результате обработки
    запроса. Восстанавливает флаги и значения параметров в значения по умолчанию.\n
    (EN) To inform a Telegram-user about successful or unsuccessful result of
    the request and to restore flags and parameters values to default values

    :param msg: Message object
    :param err: Error flag. If False - request was successful
    :param illegal: Illegal flag. If True - request was unavailable for legal reasons
    """
    save_prm(msg.chat.id, param_name='check_in_date', param_value=cfg.DB_DEFAULTS['check_in_date'])
    save_prm(msg.chat.id, param_name='check_out_date', param_value=cfg.DB_DEFAULTS['check_out_date'])
    save_prm(msg.chat.id, param_name='dist_max', param_value=cfg.DB_DEFAULTS['dist_max'])
    save_prm(msg.chat.id, param_name='dist_min', param_value=cfg.DB_DEFAULTS['dist_min'])
    save_prm(msg.chat.id, param_name='price_max', param_value=cfg.DB_DEFAULTS['price_max'])
    save_prm(msg.chat.id, param_name='price_min', param_value=cfg.DB_DEFAULTS['price_min'])
    save_prm(msg.chat.id, param_name='is_best_deal', param_value=cfg.DB_DEFAULTS['is_best_deal'])
    save_prm(msg.chat.id, param_name='chat_state', param_value='ready')

    if err:
        if illegal:
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['illegal'],
                             disable_web_page_preview=True)
        else:
            bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['request_failure'],
                             reply_markup=tb.types.ReplyKeyboardRemove())
    else:
        bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['request_success'],
                         reply_markup=tb.types.ReplyKeyboardRemove())
    from_user_req(msg, main_message, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')]['help'])


def date_picker(msg) -> None:
    """(RU) Вывод пользователю Telegram календаря для выбора даты заезда в отель или выезда в отель.\n
    (EN) To display to a Telegram-user the calendar for picking the hotel check-in or check-out date"""
    if get_prm(msg.chat.id, 'chat_state') == 'check_in_date':
        boundary_date: datetime = datetime.now() + timedelta(days=cfg.DAYS_BEFORE_CHECK_IN)
        cal_header: str = 'choose_check_in_date'
    else:
        boundary_date = datetime.fromisoformat(get_prm(msg.chat.id, 'check_in_date')) + timedelta(days=1)
        cal_header: str = 'choose_check_out_date'
    calendar = AdaptedCalendar(boundary_date=boundary_date,
                               language=cfg.CAL_LOCALE[get_prm(msg.chat.id, 'locale')])
    calendars[msg.chat.id] = calendar
    bot.send_message(msg.chat.id, cfg.TB_LEX[get_prm(msg.chat.id, 'locale')][cal_header],
                     reply_markup=calendar.create_calendar(name=cal_1_callback.prefix,
                                                           year=boundary_date.year,
                                                           month=boundary_date.month))


@bot.callback_query_handler(func=lambda call: call.data.startswith(cal_1_callback.prefix))
def callback_inline(call: CallbackQuery) -> None:
    """(RU) Обработка inline callback вызова с кнопки календаря.\n
    (EN To proceed an inline callback call from a calendar button"""
    param_name: str = get_prm(call.from_user.id, 'chat_state')
    name, action, year, month, day = call.data.split(cal_1_callback.sep)
    date: datetime = calendars[call.from_user.id].calendar_query_handler(
        bot=bot, call=call, name=name, action=action, year=year, month=month, day=day)
    if action == "DAY":
        del calendars[call.from_user.id]
        bot.send_message(
            chat_id=call.from_user.id,
            text=f"{cfg.TB_LEX[get_prm(call.from_user.id, 'locale')][param_name]} {date.strftime('%d.%m.%Y')}",
            reply_markup=ReplyKeyboardRemove())
        save_prm(call.from_user.id, param_name=param_name, param_value=date)
        if get_prm(call.from_user.id, 'chat_state') == 'check_in_date':
            save_prm(call.from_user.id, param_name='chat_state', param_value='check_out_date')
            date_picker(call.message)
        elif get_prm(call.from_user.id, 'chat_state') == 'check_out_date':
            save_prm(call.from_user.id, param_name='chat_state', param_value='ready')
            if get_prm(call.from_user.id, 'is_best_deal'):
                save_prm(call.from_user.id, param_name='chat_state', param_value='conversation')
                bot.send_message(call.from_user.id,
                                 f"{cfg.TB_LEX[get_prm(call.from_user.id, 'locale')]['currency']} "
                                 f"{get_prm(call.from_user.id, 'currency')}")
                from_user_req(call.message, price_min_req,
                              cfg.TB_LEX[get_prm(call.from_user.id, 'locale')]['price_min_req'])
            else:
                pre_hotels_qty_req(call.message)

    elif action == "IGNORE":
        pass


def bot_set_commands(locale: str, chat_id=None) -> None:
    """(RU) Установка команд бота в соответствии с языком пользователя Telegram.\n
    (EN) To set the bot commands in accordance to the Telegram-user locale

    :param locale: Locale (language) of commands
    :param chat_id: Chat ID for setting commands
    """
    scope = None
    commands: list = []
    if chat_id:
        scope = tb.types.BotCommandScopeChat(chat_id)
    bot.delete_my_commands(scope=scope, language_code=None)
    commands_text: list = cfg.TB_LEX[locale]['help'].split('\n')
    for line in commands_text:
        command, description = line.split(' — ')
        commands.append(tb.types.BotCommand(command, description))
    bot.set_my_commands(commands=commands, scope=scope)


bot.infinity_polling()
