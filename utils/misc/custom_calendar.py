import calendar
import datetime
from telebot_calendar import CallbackData, Calendar, Language, ENGLISH_LANGUAGE
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


GERMAN_LANGUAGE = Language(
    days=("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"),
    months=(
        "Januar",
        "Februar",
        "Marsch",
        "April",
        "Dürfen",
        "Juni",
        "Juli",
        "August",
        "September",
        "Oktober",
        "November",
        "Dezember",
    ),
)

FRENCH_LANGUAGE = Language(
    days=("Lu", "Ma", "Me", "Je", "Ve", "Sa", "Di"),
    months=(
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ),
)

ITALIAN_LANGUAGE = Language(
    days=("Lu", "Ma", "Me", "Gi", "Ve", "Sa", "Do"),
    months=(
        "Gennaio",
        "Febbraio",
        "Marzo",
        "Aprile",
        "Maggio",
        "Giugno",
        "Luglio",
        "Agosto",
        "Settembre",
        "Ottobre",
        "Novembre",
        "Dicembre",
    ),
)

SPAIN_LANGUAGE = Language(
    days=("Lu", "Ma", "Mi", "Ju", "Vi", "Sa", "Do"),
    months=(
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ),
)


class AdaptedCalendar(Calendar):
    """
    Calendar data factory.
    Class Calendar was adapted from telebot-calendar v1.2
    (Inline calendar for Telebot from https://github.com/FlymeDllVa/Telebot-Calendar)
    for using with RapidAPI and Hotels.com
    """

    __lang: Language

    def __init__(self, boundary_date: datetime, language: Language = ENGLISH_LANGUAGE):
        super(Calendar, self).__init__()
        self.__lang: Language = language
        self.__b_date: datetime = boundary_date

    def create_calendar(self, name: str = "calendar",
                        year: int = None, month: int = None) -> InlineKeyboardMarkup:
        """
        Create a built-in inline keyboard with calendar

        :param name:
        :param year: Year to use in the calendar
        :param month: Month to use in the calendar
        :return: Returns an InlineKeyboardMarkup object with a calendar.
        """

        if year is None:
            year: int = self.__b_date.year
        if month is None:
            month: int = self.__b_date.month

        calendar_callback = CallbackData(name, "action", "year", "month", "day")
        data_ignore = calendar_callback.new("IGNORE", year, month, "!")
        data_months = calendar_callback.new("MONTHS", year, month, "!")

        keyboard = InlineKeyboardMarkup(row_width=7)

        keyboard.add(
            InlineKeyboardButton(
                self.__lang.months[month - 1] + " " + str(year),
                callback_data=data_months,
            )
        )

        keyboard.add(
            *[
                InlineKeyboardButton(day, callback_data=data_ignore)
                for day in self.__lang.days
            ]
        )
        for week in calendar.monthcalendar(year, month):
            row = list()
            for day in week:
                if (day == 0 or month < self.__b_date.month or year < self.__b_date.year or
                        (day < self.__b_date.day and
                         month == self.__b_date.month and
                         year == self.__b_date.year)):
                    row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
                else:
                    row.append(
                        InlineKeyboardButton(
                            str(day),
                            callback_data=calendar_callback.new(
                                "DAY", year, month, day
                            ),
                        )
                    )
            keyboard.add(*row)

        keyboard.add(
            InlineKeyboardButton(
                "<",
                callback_data=calendar_callback.new("PREVIOUS-MONTH", year, month, "!"),
            ),
            InlineKeyboardButton(
                ">", callback_data=calendar_callback.new("NEXT-MONTH", year, month, "!")
            ),
        )

        return keyboard
