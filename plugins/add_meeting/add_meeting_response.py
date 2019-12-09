# -*- coding: utf-8 -*-

import pandas as pd

from consts import home_path, week_days_en2ru_dict
from consts import admin_stat_path
from consts import vk_id_admin
from consts import in_add_db_path
from consts import events_db_path

from plugins.calendar.calendar_tools import set_free_time_abs

from plugins.db_tools.db_tools import take_param

from vk_tools import send_message
from vk_tools import file_to_doc_attachment


def set_stat(stat, k, stat_path):
    file = open(home_path + stat_path)
    full = file.read()
    stat_list = full.split("\n")
    for i in range(len(stat_list)):
        if stat in stat_list[i]:
            stat_list[i] = stat + ":= " + str(k)
            break
    file.close()
    file = open(home_path + stat_path, "w")
    for s in stat_list:
        if len(s) != 0:
            file.write(str(s) + "\n")
    file.close()


def take_stat_key(stat, stat_path):
    file = open(home_path + stat_path)
    full = file.read()
    stat_list = full.split("\n")
    k = None
    for i in range(len(stat_list)):
        if stat in stat_list[i]:
            k = stat_list[i].split(":= ")
            k = k[1]
            break
    file.close()
    return k


def take_user_info(vk_id, db_path):
    info = ""
    info = info + "Имя: " + take_param(vk_id, "real_name", db_path) + '\n' + \
                  "Страница в ВК: vk.com/id" + take_param(vk_id, "vk_id", db_path) + '\n' + \
                  "Планируемые день и место встречи: " + take_param(vk_id, "datetime_event", db_path) + ', ' + \
                  week_days_en2ru_dict[take_param(vk_id, "weekday", db_path)] + '\n' + \
                  "Институт: " + take_param(vk_id, "institute", db_path) + '\n' + \
                  "Курс: " + take_param(vk_id, "course", db_path) + '\n' + \
                  "Сколько раз был(а): " + take_param(vk_id, "count_was_here", db_path) + '\n' + \
                  "Причина записи: " + take_param(vk_id, "real_name", db_path)
    return info


def add_meeting_response(text):
    df = pd.read_csv(home_path + in_add_db_path, header=0, encoding='utf-8')
    if not df.empty:
        df = df.loc[df["add_user_step"] == 9]
        df.sort_values(["datetime_added"], inplace=True)
    if text.lower() == "список":
        set_stat("in_add_decision", 1, admin_stat_path)
        if df.empty:
            set_stat("in_add_decision", 0, admin_stat_path)
            send_message(vk_id_admin, "Список пуст")
        else:
            df.sort_values(["datetime_added"], inplace=True)
            add_user_vk_id = int(df.iloc[0]["vk_id"])
            user_info = take_user_info(add_user_vk_id, in_add_db_path)
            send_message(vk_id_admin, user_info + '\n\n Место встречи?')
    elif text.lower() == "нет" and int(take_stat_key("in_add_decision", admin_stat_path)) == 1:
        if not df.empty:
            add_user_vk_id = df.iloc[0]["vk_id"]
            df = df.loc[df["vk_id"] != add_user_vk_id]
            df.to_csv(home_path + in_add_db_path, index=False, encoding='utf-8')
            set_free_time_abs(add_user_vk_id)
            send_message(int(add_user_vk_id), "Тебя не могут принять в это время. Приносим свои извинения")
            if not df.empty:
                add_user_vk_id = df.iloc[0]["vk_id"]
                user_info = take_user_info(int(add_user_vk_id), in_add_db_path)
                send_message(vk_id_admin, user_info + '\n\n Место встречи?')
            else:
                set_stat("in_add_decision", 0, admin_stat_path)
                send_message(vk_id_admin, "Список пуст")
        else:
            send_message(vk_id_admin, "Список пуст")
    elif int(take_stat_key("in_add_decision", admin_stat_path)) == 1:
        if not df.empty:
            add_user_vk_id = df.iloc[0]["vk_id"]
            df_add_user = df.loc[df["vk_id"] == add_user_vk_id]
            df = df.loc[df["vk_id"] != add_user_vk_id]
            df.to_csv(home_path + in_add_db_path, index=False, encoding='utf-8')
            new_user_dict = df_add_user.to_dict('list')
            new_event_dict = {
                "vk_id": new_user_dict["vk_id"][0],
                "name": new_user_dict["name"][0],
                "surname": new_user_dict["surname"][0],
                "sex": new_user_dict["sex"][0],
                "real_name": new_user_dict["real_name"][0],
                "institute": new_user_dict["institute"][0],
                "course": new_user_dict["course"][0],
                "count_was_here": new_user_dict["count_was_here"][0],
                "subject": new_user_dict["subject"][0],
                "place": text,
                "datetime_added": new_user_dict["datetime_added"][0],
                "datetime_event": new_user_dict["datetime_event"][0]
            }
            df_event = pd.read_csv(home_path + events_db_path, header=0, encoding='utf-8')
            df_event = df_event.append(new_event_dict, ignore_index=True)
            df_event.to_csv(home_path + events_db_path, index=False, encoding='utf-8')
            send_message(int(add_user_vk_id), "Твоя заявка одобрена. Тебя ждут в " + text)
            if not df.empty:
                add_user_vk_id = df.iloc[0]["vk_id"]
                user_info = take_user_info(int(add_user_vk_id), in_add_db_path)
                send_message(vk_id_admin, user_info + '\n\n Место встречи?')
            else:
                set_stat("in_add_decision", 0, admin_stat_path)
                send_message(vk_id_admin, "Список пуст")
        else:
            set_stat("in_add_decision", 0, admin_stat_path)
            send_message(vk_id_admin, "Список пуст")
    elif text.lower() == "таблица":
        df = pd.read_csv(home_path + events_db_path, header=0, encoding='utf-8')
        df.to_excel(home_path + "overstudents.xlsx", index=False, encoding='utf-8')
        attachment = file_to_doc_attachment(vk_id_admin, "overstudents.xlsx")
        send_message(vk_id_admin, "", attachments=attachment)
    else:
        send_message(vk_id_admin, "Команда не найдена")

