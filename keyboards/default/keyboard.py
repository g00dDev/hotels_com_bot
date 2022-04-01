# -*- coding: utf-8 -*-
from data import config as cfg
import telebot as tb


btn_numeric: list = [tb.types.KeyboardButton(str(i)) for i in range(34)]
btn_curr: list = [tb.types.KeyboardButton(i) for i in cfg.CURRENCIES]
btn_locales: list = [tb.types.KeyboardButton(i) for i in cfg.LOCALES.keys()]
btn_yes: dict = dict([(key, val['YES']) for key, val in cfg.LEX_ASSERTION.items()])
btn_no: dict = dict([(key, val['NO']) for key, val in cfg.LEX_ASSERTION.items()])
