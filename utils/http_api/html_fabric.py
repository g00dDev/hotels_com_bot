# -*- coding: utf-8 -*-
from data import config as cfg


def hotel_html(hotel_id: str, hotel_name: str, got_locale: str) -> str:
    """(RU) Формирует HTML чанк отеля, используя идентификатор отеля и указанный язык.\n
    (EN) To build a hotel HTML chunk using ID of the hotel and the specified locale

    :param hotel_id: ID of the hotel
    :param hotel_name: Name of the hotel
    :param got_locale: Current locale of the user
    """
    # To find subdomain via locale
    locale: str = ''
    subdomain: str = ''
    for idx, val in enumerate(cfg.LOCALES.items()):
        subdomain, locale = val
        if got_locale == locale:
            subdomain += '.'
            break
    if 'en' in locale:
        return f"<a href='https://hotels.com/ho{hotel_id}'>{hotel_name}</a>"
    else:
        return f"<a href='https://{subdomain.lower()}hotels.com/ho{hotel_id}'>{hotel_name}</a>"


def html_chunk(link: str, link_text: str) -> str:
    """(RU) Формирует HTML чанк, используя ссылку и текст внутри чанка.\n
    (EN) To build a HTML chunk using a link and a piece of text inside the chunk

    :param link: HTML link
    :param link_text: Some text
    """
    return f"<a href='https://{link}'>{link_text}</a>"
