# -*- coding: utf-8 -*-
from data import config as cfg
import json
import re
import requests
from typing import Optional, Tuple, Union
from utils.db_api.models import requests_cache, get_prm
import utils.misc.project_logging as logging
from utils.http_api.html_fabric import hotel_html


@requests_cache(ttl=cfg.DB_TTL)
def request_result(*args, **kwargs) -> Union[dict, int, str]:
    """(RU) Запрос HTTP API.\n
    (EN) HTTP API request

    :return Returns: a dict if data, an integer if '429' error, a string if other error
    """
    res_text: str = ''
    tokens_counter: int = 0
    # Trying to get data with next API token when current API token is invalid
    while kwargs['headers']['x-rapidapi-key'] and tokens_counter < cfg.API_TOKENS_QTY:
        tokens_counter += 1
        response = requests.request(*args, **kwargs)
        res_status_code: int = response.status_code
        res_text: str = response.text
        if res_status_code == 429:
            logging.logger_requests.info(f"bad API token: '{cfg.API_TOKEN}'")
            cfg.API_TOKEN = cfg.next_api_token()
            logging.logger_requests.info(f"next API token: '{cfg.API_TOKEN}'")
            kwargs['headers']['x-rapidapi-key'] = cfg.API_TOKEN
            if tokens_counter == cfg.API_TOKENS_QTY:
                logging.logger_requests.debug(f"Couldn't request HTTP API any more because "
                                              f"all of tokens got over the quota:\n'{res_text}'")
                return res_status_code
        elif res_status_code != 200:
            logging.logger_requests.debug(f"Http API request failed! Response: '{res_text}'.")
            return res_text
        else:
            break
    return json.loads(res_text)


def city_request(city: str, chat_id: int) -> Union[Tuple[str, str], None, int]:
    """(RU) Используя HTTP API, получает город и его идентификатор.\n
    (EN) To get city name and city ID using HTTP API

    :param city: City specified by the user
    :param chat_id: ID for getting data from DB
    :return Returns: a tuple if data, an integer if '429' error, None if other error or data is empty
    """
    # version_1: GET locations/search
    # version_2: GET locations/v2/search
    url: str = cfg.URL_LOCATIONS_SEARCH[cfg.LOCATION_SEARCH_VER]
    response: dict = dict()
    params: dict = {
        "query": city,
        "locale": get_prm(chat_id, 'locale'),
        "currency": get_prm(chat_id, 'currency'),
    }
    headers: dict = {
        'x-rapidapi-host': cfg.HOST,
        'x-rapidapi-key': cfg.API_TOKEN
    }
    try:
        response: Optional[dict] = request_result("GET", url, headers=headers, params=params)
        if response:
            if response == 429:
                return 429
            else:
                entities_city: list = []
                entities_hotel: list = []
                for group in response["suggestions"]:
                    if group["group"] == "CITY_GROUP":
                        entities_city: list = group["entities"]
                    if group["group"] == "HOTEL_GROUP":
                        entities_hotel: list = group["entities"]
                if bool(entities_city):
                    suggested_entity, *_ = entities_city
                    return (re.sub('<.*?>', '', suggested_entity['caption']),
                            str(suggested_entity['destinationId']),)
                elif bool(entities_hotel):
                    return 451
                else:
                    logging.logger_requests.info(f"No city was found. User {chat_id} requested city: '{city}'.")
    except Exception as err:
        if err:
            logging.logger_requests.debug(f"Error while parsing response! Response: '{response}'.")


def hotels_request(hotels_qty: str, destination_id: str, sort_order: str,
                   price_min: int, price_max: int, distance_min: float,
                   distance_max: float, chat_id: int, nights: int) -> Union[list, None, int]:
    """(RU) Используя HTTP API, получает список данных об отелях.\n
    (EN) To get a list about hotels data using HTTP API

    :param hotels_qty: Quantity of hotels specified by the user
    :param destination_id: ID of the city in which hotels will be searched
    :param sort_order: Algorithm of sorting list of hotels
    :param price_min: Minimum price
    :param price_max: Maximum price
    :param distance_min: Minimum distance
    :param distance_max: Maximum distance
    :param chat_id: ID for getting data from DB
    :param nights: Quantity of nights in the hotel
    :return Returns: a list if data, an integer if '429' error, None if other error or data is empty
    """
    # GET properties/list
    url: str = cfg.URL_PROPERTIES_LIST
    check_in, _ = get_prm(chat_id, 'check_in_date').split()
    check_out, _ = get_prm(chat_id, 'check_out_date').split()
    hotels_lst: list = []
    response: dict = dict()
    params: dict = {
        "destinationId": destination_id,
        "pageNumber": cfg.PAGE,
        "pageSize": cfg.MAX_PAGE_SIZE,
        "checkIn": check_in,
        "checkOut": check_out,
        "adults1": cfg.ADULTS,
        "sortOrder": sort_order,
        "landmarkIds": destination_id,
        "priceMin": price_min,
        "priceMax": price_max,
        "priceMultiplier": str(nights),
        "locale": get_prm(chat_id, 'locale'),
        "currency": get_prm(chat_id, 'currency'),
    }
    headers: dict = {
        'x-rapidapi-host': cfg.HOST,
        'x-rapidapi-key': cfg.API_TOKEN,
    }
    try:
        response: dict = request_result("GET", url, headers=headers, params=params)
        if response == 429:
            return 429
        else:
            results: dict = response["data"]["body"]["searchResults"]["results"]
            dist_to_center_fl: float = 0.0
            for res in results:
                dist_to_center: str = ''
                for landmark in res['landmarks']:
                    if landmark['label'] in cfg.CITY_CENTER:
                        dist_to_center: str = landmark['distance']
                        # Conversion of 'miles' to 'km' for European EN locales.
                        # It's a bugfix for a revealed RapidAPI-HotelsAPI bug.
                        if (get_prm(chat_id, 'locale') in ('en_EN', 'en_GB', 'en_IE') and
                                'mile' in dist_to_center):
                            miles_num, *_ = dist_to_center.split()
                            dist_to_center = f"{miles_to_km(miles_num)} km"
                        dist_to_center_fl: float = float(re.sub(r'[^0-9,0-9]', '', dist_to_center).replace(',', '.'))
                        break
                if not dist_to_center:
                    logging.logger_requests.debug(f"Hotel data doesn't contain any of landmark labels: "
                                                  f"'{cfg.CITY_CENTER}'!\nHotel landmarks: {res['landmarks']}")
                    dist_to_center = cfg.API_LEX[get_prm(chat_id, 'locale')]['no_label']
                if distance_min <= dist_to_center_fl <= distance_max:
                    info: Optional[str] = (f"\n{res['ratePlan']['price'].get('info')}", "")[nights == 1]
                    hotels_lst.append(
                        (res['id'],
                         f"{hotel_html(res['id'], res['name'], get_prm(chat_id, 'locale'))}\n"
                         f"{cfg.API_LEX[get_prm(chat_id, 'locale')]['address']} "
                         f"{res['address'].get('locality', cfg.API_LEX[get_prm(chat_id, 'locale')]['no_city'])}, "
                         f"{res['address'].get('streetAddress', cfg.API_LEX[get_prm(chat_id, 'locale')]['no_street'])}"
                         f"\n{cfg.API_LEX[get_prm(chat_id, 'locale')]['dist_to_center']} {dist_to_center}\n"
                         f"{cfg.API_LEX[get_prm(chat_id, 'locale')]['curr_price']} "
                         f"{res['ratePlan']['price']['current']}{info}"))
                else:
                    logging.logger_requests.info(f"Hotel distance is out of range, determined by user '{chat_id}'.")
            return hotels_lst[0:int(hotels_qty)]

    except Exception as err:
        if err:
            logging.logger_requests.debug(f"Error while parsing response! Response: '{response}'.")


def hotel_photos_request(hotel_id: str, requested_qty: int) -> Optional[list]:
    """(RU) Используя HTTP API, получает список фотографий отеля.\n
    (EN) To get a list of a hotel photos using HTTP API

    :param hotel_id: ID of the hotel for getting photos
    :param requested_qty: Quantity of photos
    :return Returns: a list if data, None if an error
    """
    # GET properties/get-hotel-photos
    url: str = cfg.URL_PROPERTIES_GET_HOTEL_PHOTOS
    response: dict = dict()
    photos_lst: list = []
    counter: int = 0
    params: dict = {"id": hotel_id}
    headers: dict = {
        'x-rapidapi-host': cfg.HOST,
        'x-rapidapi-key': cfg.API_TOKEN,
    }
    try:
        response: dict = request_result("GET", url, headers=headers, params=params)
        limit_qty: int = len(response['hotelImages'])
        while counter < requested_qty and counter < limit_qty:
            photos_lst.append(re.sub(r'{size}', cfg.PHOTO_SUFFIX, response['hotelImages'][counter]['baseUrl']))
            counter += 1
    except Exception as err:
        if err:
            logging.logger_requests.debug(f"Error while parsing response! Response: '{response}'.")
    finally:
        return photos_lst


def miles_to_km(miles: str) -> Optional[str]:
    """(RU) Конвертер размерности, мили в км.\n
    (EN) Miles to km converter

    :param miles: Value as string
    """
    try:
        return str(round(float(miles) / cfg.MILES_TO_KM, 1))
    except ValueError:
        pass
