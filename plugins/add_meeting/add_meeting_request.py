# -*- coding: utf-8 -*-

import re

from plugins.keyboard.keyboards import kb_vyh
from plugins.keyboard.keyboards import kb_main
from plugins.keyboard.keyboards import kb_yes_no_vyh

from plugins.keyboard.kb_tools import list_to_keyboard
from plugins.keyboard.kb_tools import list_to_time_keyboard

from consts import added_users_db_path
from consts import week_days_ru2en_dict
from consts import in_add_db_path
from consts import institutes_list
from consts import courses_list
from consts import next_week_path
from consts import current_week_path
from consts import vk_id_admin
from consts import week_days_en
from consts import week_days_en2ru_dict

from plugins.db_tools.db_tools import take_param
from plugins.db_tools.db_tools import check_param
from plugins.db_tools.db_tools import set_param
from plugins.db_tools.db_tools import check_id
from plugins.db_tools.db_tools import back_just_dialog

from plugins.keyboard.keyboards import kb_institutes
from plugins.keyboard.keyboards import kb_courses

from plugins.calendar.calendar_tools import find_free_time_week
from plugins.calendar.calendar_tools import set_free_time_abs
from plugins.calendar.calendar_tools import check_free_time
from plugins.calendar.calendar_tools import free_time_dict_to_text
from plugins.calendar.calendar_tools import set_free_time
from plugins.calendar.calendar_tools import make_datetime_event

from vk_tools import send_message

from datetime import datetime


def add_user(vk_id, text):
    step = int(take_param(vk_id, "add_user_step", in_add_db_path))
    response = {
        "exit": False,
        "message": "no_text_add_user",
        "keyboard": kb_vyh,
        "attachments": None
    }
    if step == 0:
        set_param(vk_id, "add_user_step", 1, in_add_db_path)
        response["message"] = "Как к Вам обращаться?"
    elif step == 1:
        set_param(vk_id, "real_name", text, added_users_db_path)
        set_param(vk_id, "add_user_step", 2, in_add_db_path)
        response["message"] = "Выберите свой институт"
        response["keyboard"] = kb_institutes
    elif step == 2:
        if text.upper() in institutes_list or \
                text.lower() == "энми" or \
                text.lower() == "ипээф" or \
                text.lower() == "инэи":
            if text.lower() == "энми":
                text = "ЭнМИ"
            elif text.lower() == "ипээф":
                text = "ИПЭЭф"
            elif text.lower() == "инэи":
                text = "ИнЭИ"
            else:
                text = text.upper()
            set_param(vk_id, "add_user_step", 3, in_add_db_path)
            set_param(vk_id, "institute", text, added_users_db_path)
            response["message"] = "Укажите курс"
            response["keyboard"] = kb_courses
        else:
            response["message"] = "Такого института нет в МЭИ)"
            response["keyboard"] = kb_institutes
    elif step == 3:
        if text in courses_list:
            set_param(vk_id, "add_user_step", 4, in_add_db_path)
            set_param(vk_id, "course", text, added_users_db_path)
            response["message"] = "Сколько встреч было?"
            response["keyboard"] = list_to_keyboard(["0"])
        else:
            response["message"] = "Введи корректный курс"
            response["keyboard"] = kb_courses
    return response


def choose_week(vk_id, response, res_current, res_next):
    res = ""
    if res_current and res_next:
        res = "этой и следующей неделях. На какую неделю тебя записать?"
        response["keyboard"] = list_to_keyboard(["На эту", "На следующую"])
    elif res_current and not res_next:
        res = "этой неделе. Записать тебя на нее?"
        set_param(vk_id, "num_of_week", 1, in_add_db_path)
        response["keyboard"] = list_to_keyboard(["Да"])
    elif not res_current and res_next:
        res = "следующей неделе. Записать тебя на нее?"
        set_param(vk_id, "num_of_week", 2, in_add_db_path)
        response["keyboard"] = list_to_keyboard(["Да"])
    response["message"] = "Есть свободные часы на {}".format(res)
    return response


def add_meeting_request(vk_id, text):
    free_time_current_week_dict = find_free_time_week(current_week_path)
    free_time_next_week_dict = find_free_time_week(next_week_path)
    res_current = check_free_time(free_time_current_week_dict)
    res_next = check_free_time(free_time_next_week_dict)
    check_id(vk_id, added_users_db_path)
    check_id(vk_id, in_add_db_path)
    step = int(take_param(vk_id, "add_user_step", in_add_db_path))
    response = {
        "exit": False,
        "message": "no_text_add_meeting",
        "keyboard": kb_vyh,
        "attachments": None
    }
    if not res_next and not res_current:
        back_just_dialog(vk_id, in_add_db_path)
        response["exit"] = True
        response["message"] = "Свободное времени на этой и следующей неделях отсутствует"
        response["keyboard"] = kb_main
    elif text.lower() == "выход":
        back_just_dialog(vk_id, in_add_db_path)
        response["exit"] = True
        response["message"] = "Запись на консультацию отменена"
        response["keyboard"] = kb_main
    elif step <= 3 and take_param(vk_id, "course", added_users_db_path) == "0":
        response = add_user(vk_id, text)
    elif step == 0 and check_param(vk_id, "course", added_users_db_path):
        if not check_param(vk_id, "overwrite", in_add_db_path):
            user_real_name = take_param(vk_id, "real_name", added_users_db_path)
            user_institute = take_param(vk_id, "institute", added_users_db_path)
            user_course = take_param(vk_id, "course", added_users_db_path)
            set_param(vk_id, "overwrite", 1, in_add_db_path)
            response["message"] = "Вы уже есть в базе данных.\n" \
                                  "Имя: {}\n" \
                                  "Институт: {}\n" \
                                  "Курс: {}\n" \
                                  "Все верно?".format(user_real_name, user_institute, user_course)
            response["keyboard"] = kb_yes_no_vyh
        elif check_param(vk_id, "overwrite", in_add_db_path):
            if text.lower() == "да":
                user_real_name = take_param(vk_id, "real_name", added_users_db_path)
                user_institute = take_param(vk_id, "institute", added_users_db_path)
                user_course = take_param(vk_id, "course", added_users_db_path)
                set_param(vk_id, "add_user_step", 4, in_add_db_path)
                set_param(vk_id, "real_name", user_real_name, in_add_db_path)
                set_param(vk_id, "institute", user_institute, in_add_db_path)
                set_param(vk_id, "course", user_course, in_add_db_path)
                response["message"] = "Какая по счету встреча с психологом Службы психологической поддержки МЭИ?\n" \
                                      "Если не помнишь, или ни разу не был, отправь 0"
                response["keyboard"] = list_to_keyboard(["0"])
            elif text.lower() == "нет":
                back_just_dialog(vk_id, added_users_db_path)
                response = add_user(vk_id, text)
            else:
                response["message"] = "На этот вопрос нужно ответить 'Да' или 'Нет'"
                response["keyboard"] = kb_yes_no_vyh
    elif step == 4:
        try:
            count = int(text)
            if count < 0:
                raise Exception(ValueError)
            set_param(vk_id, "count_was_here", count, in_add_db_path)
            set_param(vk_id, "add_user_step", 5, in_add_db_path)
            response["message"] = "Опиши свой запрос, что ты хочешь обсудить на встрече?"
            response["keyboard"] = list_to_keyboard(["Не хочу писать о проблеме"])
        except Exception as e:
            del e
            response["message"] = "Введи корректное число"
    elif step == 5:
        set_param(vk_id, "subject", text, in_add_db_path)
        set_param(vk_id, "add_user_step", 6, in_add_db_path)
        response = choose_week(vk_id, response, res_current, res_next)
    elif step == 6:
        ps = "Выбери день недели"
        if text.lower() == 'да' and \
                take_param(vk_id, "num_of_week", in_add_db_path) == '1' and \
                res_current:
            set_param(vk_id, "add_user_step", 7, in_add_db_path)
            free_time_text = free_time_dict_to_text(free_time_current_week_dict)
            response["message"] = "Хорошо. Запишем тебя на эту неделю." + free_time_text + ps
            weekdays = []
            for day in week_days_en:
                if len(free_time_current_week_dict[day]) != 0:
                    weekdays.append(week_days_en2ru_dict[day].title())
            response["keyboard"] = list_to_keyboard(weekdays)
        elif text.lower() == 'да' and \
                take_param(vk_id, "num_of_week", in_add_db_path) == '2' and \
                res_next:
            set_param(vk_id, "add_user_step", 7, in_add_db_path)
            free_time_text = free_time_dict_to_text(free_time_next_week_dict)
            response["message"] = "Хорошо. Запишем тебя на следующую неделю." + free_time_text + ps
            weekdays = []
            for day in week_days_en:
                if len(free_time_next_week_dict[day]) != 0:
                    weekdays.append(week_days_en2ru_dict[day].title())
            response["keyboard"] = list_to_keyboard(weekdays)
        elif text.lower() == "на эту" and \
                take_param(vk_id, "num_of_week", in_add_db_path) == '0' and \
                res_current:
            set_param(vk_id, "add_user_step", 7, in_add_db_path)
            set_param(vk_id, "num_of_week", 1, in_add_db_path)
            free_time_text = free_time_dict_to_text(free_time_current_week_dict)
            response["message"] = "Хорошо. Запишем тебя на эту неделю." + free_time_text + ps
            weekdays = []
            for day in week_days_en:
                if len(free_time_current_week_dict[day]) != 0:
                    weekdays.append(week_days_en2ru_dict[day].title())
            response["keyboard"] = list_to_keyboard(weekdays)
        elif text.lower() == "на следующую" and \
                take_param(vk_id, "num_of_week", in_add_db_path) == '0' and \
                res_next:
            set_param(vk_id, "add_user_step", 7, in_add_db_path)
            set_param(vk_id, "num_of_week", 2, in_add_db_path)
            free_time_text = free_time_dict_to_text(free_time_next_week_dict)
            response["message"] = "Хорошо. Запишем тебя на следующую неделю." + free_time_text + ps
            weekdays = []
            for day in week_days_en:
                if len(free_time_next_week_dict[day]) != 0:
                    weekdays.append(week_days_en2ru_dict[day].title())
            response["keyboard"] = list_to_keyboard(weekdays)
        else:
            response = choose_week(vk_id, response, res_current, res_next)
    elif step == 7:
        num_of_week = int(take_param(vk_id, "num_of_week", in_add_db_path))
        if num_of_week == 1:
            weekdays = []
            for day in week_days_en:
                if len(free_time_current_week_dict[day]) != 0:
                    weekdays.append(week_days_en2ru_dict[day])
            if text.lower() in weekdays:
                set_param(vk_id, "weekday", week_days_ru2en_dict[text.lower()], in_add_db_path)
                set_param(vk_id, "add_user_step", 8, in_add_db_path)
                hhmms = ""
                day = week_days_ru2en_dict[text.lower()]
                for hhmm in free_time_current_week_dict[day]:
                    hhmms += hhmm
                    if hhmm != free_time_current_week_dict[day][-1]:
                        hhmms += ", "
                response["message"] = "Выбери удобное время из предложенных вариантов (встреча длится 60 минут, " \
                                      "ты можешь записаться на начало следующего часа – ... 00; либо на половину " \
                                      "часа – ... 30)\n{}".format(hhmms)
                response["keyboard"] = list_to_time_keyboard(hhmms.split(", "))
            else:
                response["message"] = "Выбери другой день недели"
                for i in range(len(weekdays)):
                    weekdays[i] = weekdays[i].title()
                response["keyboard"] = list_to_keyboard(weekdays)
        elif num_of_week == 2:
            weekdays = []
            for day in week_days_en:
                if len(free_time_next_week_dict[day]) != 0:
                    weekdays.append(week_days_en2ru_dict[day])
            if text.lower() in weekdays:
                set_param(vk_id, "weekday", week_days_ru2en_dict[text.lower()], in_add_db_path)
                set_param(vk_id, "add_user_step", 8, in_add_db_path)
                hhmms = ""
                day = week_days_ru2en_dict[text.lower()]
                for hhmm in free_time_next_week_dict[day]:
                    hhmms += hhmm
                    if hhmm != free_time_next_week_dict[day][-1]:
                        hhmms += ", "
                response["message"] = "Выбери удобное время из предложенных вариантов (встреча длится 60 минут, " \
                                      "ты можешь записаться на начало следующего часа – ... 00; либо на половину " \
                                      "часа – ... 30)\n{}".format(hhmms)
                response["keyboard"] = list_to_time_keyboard(hhmms.split(", "))
            else:
                response["message"] = "Выбери другой день недели"
                for i in range(len(weekdays)):
                    weekdays[i] = weekdays[i].title()
                response["keyboard"] = list_to_keyboard(weekdays)
    elif step == 8:
        dataset = re.findall(r"\d+", text)
        if len(dataset) == 2:
            week_day = take_param(vk_id, "weekday", in_add_db_path)
            meeting_time = dataset[0] + ":" + dataset[1]
            if (take_param(vk_id, "num_of_week", in_add_db_path) == "1" and meeting_time in free_time_current_week_dict[
                week_day]) or \
                    (take_param(vk_id, "num_of_week", in_add_db_path) == "2" and meeting_time in
                     free_time_next_week_dict[week_day]):
                response["message"] = "Заявка отправлена. Ожидайте подтверждения. Если хочешь отменить встречу, " \
                                      "напиши – Отмена"
                response["keyboard"] = list_to_keyboard(["Отмена"])
                datetime_event = -1
                if take_param(vk_id, "num_of_week", in_add_db_path) == "1":
                    datetime_event = make_datetime_event(week_day, meeting_time, 1)
                    set_free_time(week_day, meeting_time, current_week_path, 1)
                elif take_param(vk_id, "num_of_week", in_add_db_path) == "2":
                    datetime_event = make_datetime_event(week_day, meeting_time, 2)
                    set_free_time(week_day, meeting_time, next_week_path, 1)
                response["exit"] = True
                response["keyboard"] = kb_main
                set_param(vk_id, "add_user_step", 9, in_add_db_path)
                set_param(vk_id, "meeting_time", meeting_time, in_add_db_path)
                set_param(vk_id, "datetime_added", str(datetime.now()), in_add_db_path)
                set_param(vk_id, "datetime_event", str(datetime_event), in_add_db_path)
                send_message(vk_id_admin, "Новая запись")
            else:
                response["message"] = "Выбранное время недоступно"
        else:
            response["message"] = "Выбери удобное время из предложенных вариантов (встреча длится 60 минут, ты можешь " \
                                  "записаться на начало следующего часа – ... 00; либо на половину часа – ... 30)"
            hhmms = ""
            day = take_param(vk_id, "weekday", in_add_db_path)
            for hhmm in free_time_next_week_dict[day]:
                hhmms += hhmm
                if hhmm != free_time_next_week_dict[day][-1]:
                    hhmms += ", "
            response["keyboard"] = list_to_time_keyboard(hhmms.split(", "))
    elif step == 9:
        response["exit"] = True
        if text.lower() == "отмена":
            set_free_time_abs(vk_id)
            back_just_dialog(vk_id, in_add_db_path)
            response["message"] = "Запись на консультацию отменена"
            response["keyboard"] = kb_main
        else:
            response["message"] = "Ожидайте подтверждения"
            response["keyboard"] = kb_main
    return response
