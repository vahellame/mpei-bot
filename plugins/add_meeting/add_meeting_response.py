# -*- coding: utf-8 -*-

import pandas as pd

from consts import home_path, week_days_en2ru_dict, month_strnum2ru_dict
from consts import admin_stat_path
from consts import vk_id_admin
from consts import in_add_db_path
from consts import events_db_path

from plugins.calendar.calendar_tools import set_free_time_abs

from plugins.db_tools.db_tools import take_param, take_user_info

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
            send_message(vk_id_admin, user_info + '\n\n Встреча будет в ...?')
    elif text.lower() == "нет" and int(take_stat_key("in_add_decision", admin_stat_path)) == 1:
        if not df.empty:
            add_user_vk_id = int(df.iloc[0]["vk_id"])
            set_free_time_abs(add_user_vk_id)
            df = df.loc[df["vk_id"] != add_user_vk_id]
            df.to_csv(home_path + in_add_db_path, index=False, encoding='utf-8')
            send_message(int(add_user_vk_id), "Тебя не могут принять в это время. Приносим свои извинения")
            if not df.empty:
                add_user_vk_id = int(df.iloc[0]["vk_id"])
                user_info = take_user_info(add_user_vk_id, in_add_db_path)
                send_message(vk_id_admin, user_info + '\n\n Встреча будет в ...?')
            else:
                set_stat("in_add_decision", 0, admin_stat_path)
                send_message(vk_id_admin, "Список пуст")
        else:
            send_message(vk_id_admin, "Список пуст")
    elif int(take_stat_key("in_add_decision", admin_stat_path)) == 1:
        if not df.empty:
            ru_date_event = df.iloc[0]["datetime_event"].split(" ")[0].split("-")[2]
            if ru_date_event[0] == "0":
                ru_date_event = ru_date_event[-1]
            ru_date_event = ru_date_event + " " + \
                            month_strnum2ru_dict[df.iloc[0]["datetime_event"].split(" ")[0].split("-")[1]] + ", "
            ru_weekday = week_days_en2ru_dict[df.iloc[0]["weekday"]]
            if ru_weekday == "вторник":
                ru_date_event += "во вторник"
            elif ru_weekday == "понедельник" or ru_weekday == "четверг" or ru_weekday == "воскресенье":
                ru_date_event = ru_date_event + "в " + ru_weekday
            else:
                ru_date_event = ru_date_event + "в " + ru_weekday[0:-1] + "у"
            add_user_vk_id = int(df.iloc[0]["vk_id"])
            new_event_dict = {
                "vk_id": int(df.iloc[0]["vk_id"]),
                "name": str(df.iloc[0]["name"]),
                "surname": str(df.iloc[0]["surname"]),
                "sex": int(df.iloc[0]["sex"]),
                "real_name": str(df.iloc[0]["real_name"]),
                "institute": str(df.iloc[0]["institute"]),
                "course": int(df.iloc[0]["course"]),
                "count_was_here": int(df.iloc[0]["count_was_here"]),
                "subject": str(df.iloc[0]["subject"]),
                "place": str(text),
                "datetime_added": str(df.iloc[0]["datetime_added"]),
                "datetime_event": str(df.iloc[0]["datetime_event"])
            }
            df = df.loc[df["vk_id"] != int(add_user_vk_id)]
            df.to_csv(home_path + in_add_db_path, index=False, encoding='utf-8')
            df_event = pd.read_csv(home_path + events_db_path, header=0, encoding='utf-8')
            df_event = df_event.append(new_event_dict, ignore_index=True)
            df_event.to_csv(home_path + events_db_path, index=False, encoding='utf-8')
            add_text = "в " + new_event_dict["datetime_event"].split(" ")[1][:5] + ", " + ru_date_event
            send_message(add_user_vk_id, "Твоя заявка одобрена. Тебя ждут в " + text + ", " + add_text)
            if not df.empty:
                add_user_vk_id = int(df.iloc[0]["vk_id"])
                user_info = take_user_info(add_user_vk_id, in_add_db_path)
                send_message(vk_id_admin, user_info + '\n\n Встреча будет в ...?')
            else:
                set_stat("in_add_decision", 0, admin_stat_path)
                send_message(vk_id_admin, "Список пуст")
        else:
            set_stat("in_add_decision", 0, admin_stat_path)
            send_message(vk_id_admin, "Список пуст")
    elif text.lower() == "таблица":
        df = pd.read_csv(home_path + events_db_path, header=0, encoding='utf-8')
        df.to_excel(home_path + "Студенты.xlsx", index=False, encoding='utf-8')
        attachment = file_to_doc_attachment(vk_id_admin, "Студенты.xlsx")
        send_message(vk_id_admin, "", attachments=attachment)
    else:
        send_message(vk_id_admin, "Команда не найдена")
