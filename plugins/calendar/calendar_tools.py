# -*- coding: utf-8 -*-

import pandas as pd
import datetime

from consts import home_path
from consts import in_add_db_path
from consts import current_week_path
from consts import next_week_path
from consts import week_days_en
from consts import week_days_en2ru_dict
from consts import week_days_en2num_dict

from plugins.db_tools.db_tools import take_param


def hhmm_to_m(hhmm):
    m = int(hhmm[0:2]) * 60 + int(hhmm[3:5])
    return str(m)


def m_to_hhmm(m):
    hh = str(int(int(m) / 60))
    if len(hh) == 1:
        hh = "0" + hh
    mm = str(int(m) % 60)
    if len(mm) == 1:
        mm = "0" + mm
    return hh + ":" + mm


def check_free_time(free_time_dict):
    i = 0
    for day in week_days_en:
        if len(free_time_dict[day]) == 0:
            i += 1
    if i == 7:
        return False
    return True


def find_free_time_week(week_path):
    free_time_dict = {day: [] for day in week_days_en}
    df = pd.read_csv(home_path + week_path, header=0, encoding='utf-8')
    week_dict = df.to_dict('list')
    for day in week_days_en:
        for i in range(45):
            if week_dict[day][i] == 0 and \
                    week_dict[day][i + 1] == 0 and \
                    week_dict[day][i + 2] == 0:
                free_time_dict[day].append(week_dict["hhmm"][i])
    return free_time_dict


def set_param(vk_id, param, k, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    df.loc[df["vk_id"] == vk_id, param] = k
    df.to_csv(home_path + db_path, index=False, encoding='utf-8')


def set_free_time(week_day, hhmm, week_path, k):
    df = pd.read_csv(home_path + week_path, header=0, encoding='utf-8')
    df.loc[df["hhmm"] == hhmm, week_day] = k
    hhmm = m_to_hhmm(int(hhmm_to_m(hhmm)) + 30)
    df.loc[df["hhmm"] == hhmm, week_day] = k
    hhmm = m_to_hhmm(int(hhmm_to_m(hhmm)) + 30)
    df.loc[df["hhmm"] == hhmm, week_day] = k
    df.to_csv(home_path + week_path, index=False, encoding='utf-8')


def free_time_dict_to_text(free_time_dict):
    text = " Есть свободное время в следующие дни:\n"
    for day in week_days_en:
        if len(free_time_dict[day]) != 0:
            text += "\n{}: ".format(week_days_en2ru_dict[day].title())
            for hhmm in free_time_dict[day]:
                text += hhmm
                if hhmm != free_time_dict[day][-1]:
                    text += ", "
            text += '\n'
    text += '\n'
    return text


def make_datetime_event(weekday, hhmm, count_week):
    count_week -= 1
    weekday_num_event = week_days_en2num_dict[weekday]
    now = datetime.datetime.now()
    weekday_num_now = now.weekday()
    year = now.year
    month = now.month
    day = now.day
    hours = int(hhmm[0:2])
    minutes = int(hhmm[3:5])
    days_until = weekday_num_event - weekday_num_now + count_week * 7
    datetime_event = datetime.datetime(year, month, day, hours, minutes, 0) + datetime.timedelta(days=days_until)
    return datetime_event


def set_free_time_abs(vk_id):
    week_day = take_param(vk_id, "weekday", in_add_db_path)
    meeting_time = take_param(vk_id, "meeting_time", in_add_db_path)
    if datetime.datetime.now().timestamp() - datetime.datetime(year_e, month_e, day_e).timestamp() > 0:
        pass
    elif datetime.datetime.now().isocalendar()[1] == datetime.datetime(year_e, month_e, day_e).isocalendar()[1]:
        set_free_time(week_day, meeting_time, current_week_path, 0)
    else:
        set_free_time(week_day, meeting_time, next_week_path, 0)
