# -*- coding: utf-8 -*-

import os
import sys
import vk_api

from vk_token import vk_token

vk_id_admin = 554086055
vk_key_admin = "0143"
vk = vk_api.VkApi(token=vk_token)

home_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '/'
main_db_path = "db/users.csv"
events_db_path = "plugins/add_meeting/events.csv"
added_users_db_path = "plugins/add_meeting/added_users.csv"
in_add_db_path = "plugins/add_meeting/in_add.csv"
admin_stat_path = "plugins/add_meeting/admin_stat.txt"

current_week_path = "plugins/calendar/current_week.csv"
next_week_path = "plugins/calendar/next_week.csv"
default_week_path = "plugins/calendar/default_week.csv"

courses_list = ["1", "2", "3", "4", "Магистратура"]
institutes_list = ["ЭнМИ", "ИТАЭ", "ИПЭЭф", "ИЭТ", "ИЭЭ", "АВТИ", "ИРЭ", "ГПИ", "ИнЭИ", "ИДДО", "ВИИ", "ИГВИЭ"]

week_days_en = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
week_days_ru = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]

week_days_en2ru_dict = {
    "monday": "понедельник",
    "tuesday": "вторник",
    "wednesday": "среда",
    "thursday": "четверг",
    "friday": "пятница",
    "saturday": "суббота",
    "sunday": "воскресеье"
}

week_days_ru2en_dict = {
    "понедельник": "monday",
    "вторник": "tuesday",
    "среда": "wednesday",
    "четверг": "thursday",
    "пятница": "friday",
    "суббота": "saturday",
    "воскресеье": "sunday"
}

week_days_en2num_dict = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}

week_days_ru2num_dict = {
    "понедельник": 0,
    "вторник": 1,
    "среда": 2,
    "четверг": 3,
    "пятница": 4,
    "суббота": 5,
    "воскресеье": 6
}

week_days_num2en_dict = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday"
}

month_strnum2ru_dict = {
    "01": "января",
    "02": 'февраля',
    "03": 'марта',
    "04": 'апреля',
    "05": 'мая',
    "06": 'июня',
    "07": 'июля',
    "08": 'августа',
    "09": 'сентября',
    "10": 'октября',
    "11": 'ноября',
    "12": 'декабря'
}
