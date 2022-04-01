# -*- coding: utf-8 -*-
from collections import deque
import data.lexicon as lex
from environs import Env
from typing import Optional
from telebot_calendar import ENGLISH_LANGUAGE, RUSSIAN_LANGUAGE
from utils.misc.custom_calendar import (GERMAN_LANGUAGE, FRENCH_LANGUAGE,
                                        ITALIAN_LANGUAGE, SPAIN_LANGUAGE)


def api_tokens_build():
    """To bild a container of API tokens from .env variables"""
    for idx in range(3):
        API_TOKENS_QUEUE.append(env.str(f"API_TOKEN_{idx}"))


def next_api_token() -> Optional[str]:
    """To fetch next API token from the deque container

    :return Returns API token from tokens queue or None if the queue is empty
    """
    if API_TOKENS_QUEUE:
        api_token = API_TOKENS_QUEUE.pop()
        API_TOKENS_QUEUE.appendleft(api_token)
        return api_token
    else:
        return None


# Application constants
env = Env()
env.read_env()


# RapidAPI constants (https://rapidapi.com)
ADULTS: str = '1'
API_LEX: dict = lex.API_LEX
API_TOKENS_QUEUE: deque = deque()
api_tokens_build()
API_TOKENS_QTY = len(API_TOKENS_QUEUE)
API_TOKEN: str = next_api_token()
CITY_CENTER: tuple = ('City center', 'City centre', 'Stadtzentrum', 'Centre-ville',
                      'Центр города', 'Centro', 'Centro de la ciudad')
HOST: str = 'hotels4.p.rapidapi.com'
LOCATION_SEARCH_VER: str = 'version_2'
MAX_PAGE_SIZE: str = '25'
PAGE: str = '1'
PHOTO_SUFFIX: str = 'y'  # b, d, e, g, l, n, s, t, w, z   are available
SORT_ORDER: dict = {
    'lowprice': 'PRICE',
    'highprice': 'PRICE_HIGHEST_FIRST',
    'bestdeal': 'PRICE',
}
URL_GET_META_DATA: str = 'https://hotels4.p.rapidapi.com/get-meta-data'
URL_LOCATIONS_SEARCH: dict = {
    'version_1': 'https://hotels4.p.rapidapi.com/locations/search',
    'version_2': 'https://hotels4.p.rapidapi.com/locations/v2/search',
}
URL_PROPERTIES_GET_DETAILS: str = 'https://hotels4.p.rapidapi.com/properties/get-details'
URL_PROPERTIES_GET_HOTEL_PHOTOS: str = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'
URL_PROPERTIES_LIST: str = 'https://hotels4.p.rapidapi.com/properties/list'
MILES_TO_KM: float = 1.609344


# Calendar constants:
DAYS_BEFORE_CHECK_IN: int = 0
CAL_LOCALE: dict = {
    'de_DE': GERMAN_LANGUAGE,
    'en_IE': ENGLISH_LANGUAGE,
    'en_US': ENGLISH_LANGUAGE,
    'es_ES': SPAIN_LANGUAGE,
    'fr_FR': FRENCH_LANGUAGE,
    'it_IT': ITALIAN_LANGUAGE,
    'ru_RU': RUSSIAN_LANGUAGE,
}

# Telebot (pyTelegramBotAPI) constants
ADMIN_ID: int = env.int("ADMIN_ID")
CURRENCIES: tuple = ('RUB', 'EUR', 'USD', 'GBP', 'KZT', 'UAH', 'CNY', 'JPY',)
CURRENCY_DEF, *_ = CURRENCIES
MEDIA_LIMIT: int = 9
MESSAGE_LIMIT: int = 4000
LEX_ASSERTION: dict = lex.LEX_ASSERTION
LOCALES: dict = lex.LOCALES
LOCALE_DEF: str = lex.LOCALE_DEF
TB_DIMENSION: dict = {
    'de_DE': 'km',
    'en_IE': 'km',
    'en_US': 'miles',
    'es_ES': 'km',
    'fr_FR': 'km',
    'it_IT': 'km',
    'ru_RU': 'км',
}
TB_LEX: dict = lex.TB_LEX
TB_TOKEN: str = env.str("TB_TOKEN")
TB_START_MSG: str = ('(RU) Выберите язык\n\n(EN) Choose a language\n\n(DE) Wählen Sie die Sprache\n\n'
                     '(FR) Choisissez la langue\n\n(IT) Scegli la lingua\n\n(ES) Elige el idioma')


# Structure of function calls (not used in the code, just for information)
MAIN_CALLS: dict = {
    '/lowprice': {
        0: 'main_message',
        1: 'city_req',
        2: 'is_city_correct',
        3: 'date_picker',
        4: 'callback_inline',
        5: 'date_picker',
        6: 'callback_inline',
        7: 'pre_hotels_qty_req',
        8: 'hotels_qty_req',
        9: {
            'hotels_need_photos_tg': {
                'NO': {
                    0: 'save_history',
                    1: 'request_done',
                },
                'YES': {
                    0: 'hotels_photos_qty_req',
                    1: 'save_history',
                    2: 'request_done',
                },
            },
        },
    },
    '/highprice': {
        0: 'main_message',
        1: 'city_req',
        2: 'is_city_correct',
        3: 'date_picker',
        4: 'callback_inline',
        5: 'date_picker',
        6: 'callback_inline',
        7: 'pre_hotels_qty_req',
        8: 'hotels_qty_req',
        9: {
            'hotels_need_photos_tg': {
                'NO': {
                    0: 'save_history',
                    1: 'request_done',
                },
                'YES': {
                    0: 'hotels_photos_qty_req',
                    1: 'save_history',
                    2: 'request_done',
                },
            },
        },
    },
    '/bestprice': {
        0: 'main_message',
        1: 'city_req',
        2: 'is_city_correct',
        3: 'date_picker',
        4: 'callback_inline',
        5: 'date_picker',
        6: 'callback_inline',
        7: 'price_min_req',
        8: 'price_max_req',
        9: 'dist_min_req',
        10: 'dist_max_req',
        11: 'pre_hotels_qty_req',
        12: 'hotels_qty_req',
        13: {
            'hotels_need_photos_tg': {
                'NO': {
                    0: 'save_history',
                    1: 'request_done',
                },
                'YES': {
                    0: 'hotels_photos_qty_req',
                    1: 'save_history',
                    2: 'request_done',
                },
            },
        },
    },
}


# Database constants
DB_CACHED: str = './db_cached.db'
DB_DEFAULTS: dict = {
    'check_in_date': '',
    'check_out_date': '',
    'city': '',
    'city_id': '',
    'currency': CURRENCY_DEF,
    'dist_max': 1000.0,
    'dist_min': 0.0,
    'hotels_photos_qty': '',
    'hotels_qty': '',
    'is_best_deal': False,
    'locale': LOCALE_DEF,
    'price_max': 9999999,
    'price_min': 0,
    'sort_order': '',  # Accessible values listed in SORT_ORDER dictionary
    'user_command': '',
    'chat_state': 'ready',  # Values allowed:
                            # 'ready', 'conversation', 'assertion', 'check_in_date', 'check_out_date'
}
DB_TTL: int = 86400  # Specify in seconds. E.g. 86400 -> 1 day, 3600 -> 1 hour
