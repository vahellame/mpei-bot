# -*- coding: utf-8 -*-

import os
import sys
import linecache
import pandas as pd
import schedule
import time
import datetime

from threading import Thread

from consts import vk
from consts import vk_id_admin
from consts import week_days_num2en_dict
from consts import vk_key_admin
from consts import main_db_path
from consts import home_path
from consts import default_week_path
from consts import current_week_path
from consts import next_week_path

from vk_tools import send_message

from plugins.db_tools.db_tools import check_id
from plugins.db_tools.db_tools import set_param
from plugins.db_tools.db_tools import back_just_dialog
from plugins.db_tools.db_tools import check_just_dialog
from plugins.db_tools.db_tools import check_param

from plugins.add_meeting.add_meeting_request import add_meeting_request

from plugins.add_meeting.add_meeting_response import add_meeting_response

from plugins.keyboard.keyboards import kb_main

from plugins.calendar.calendar_tools import set_free_time


def daily_update():
    today = datetime.datetime.now().weekday()
    today = week_days_num2en_dict[today]
    set_free_time(today, "11:00", current_week_path, 1)
    set_free_time(today, "12:30", current_week_path, 1)
    set_free_time(today, "14:00", current_week_path, 1)
    set_free_time(today, "15:30", current_week_path, 1)
    set_free_time(today, "17:00", current_week_path, 1)


def daily_update_loop():
    schedule.every().day.at("00:00").do(daily_update)
    while True:
        schedule.run_pending()
        time.sleep(1)


def weekly_update():
    df_next_week = pd.read_csv(home_path + next_week_path, header=0, encoding='utf-8')
    df_next_week.to_csv(home_path + current_week_path, encoding='utf-8', index=False)
    df_default_week = pd.read_csv(home_path + default_week_path, header=0, encoding='utf-8')
    df_default_week.to_csv(home_path + next_week_path, encoding='utf-8', index=False)


def weekly_update_loop():
    schedule.every().monday.at("00:00").do(weekly_update)
    while True:
        schedule.run_pending()
        time.sleep(1)


def mpei_bot():
    i_feel_pain = True
    run_for_all = True
    run_for_admin = False
    while i_feel_pain:
        # try:
            while run_for_all:
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unanswered"})
                if messages["count"] > 0:
                    user_id = messages['items'][0]['last_message']['peer_id']
                    body = messages['items'][0]['last_message']['text']
                    check_id(user_id, main_db_path)
# JUST DIALOG ==========================================================================================================
                    if user_id != vk_id_admin and check_just_dialog(user_id, main_db_path):
                        if body.lower() == "привет":
                            send_message(user_id, "Добро пожаловать. Снова.")
                        elif body.lower() == "записаться на консультацию" or body.lower() == "вжух":
                            set_param(user_id, "in_add_meeting", 1, main_db_path)
                            response = add_meeting_request(user_id, body)
                            if response['exit']:
                                back_just_dialog(user_id, main_db_path)
                            send_message(user_id, response['message'],
                                         keyboard=response['keyboard'],
                                         attachments=response['keyboard'])
                        else:
                            send_message(user_id, "Что дальше?", keyboard=kb_main)
# IN ADD MEETING - REQUEST =============================================================================================
                    elif user_id != vk_id_admin and check_param(user_id, "in_add_meeting", main_db_path):
                        response = add_meeting_request(user_id, body)
                        if response['exit']:
                            back_just_dialog(user_id, main_db_path)
                        send_message(user_id, response['message'],
                                     keyboard=response['keyboard'],
                                     attachments=response['attachments'])
# IN ADD MEETING - RESPONSE ============================================================================================
                    elif user_id == vk_id_admin:
                        add_meeting_response(body)
# STOPPING BOT =========================================================================================================
                    elif user_id == vk_id_admin and body.lower() == vk_key_admin:
                        run_for_all = False
                        run_for_admin = True
                        send_message(vk_id_admin, "Бот остановлен")
# RUN ONLY FOR ADMIN ===================================================================================================
            while run_for_admin:
                messages = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unanswered"})
                if messages["count"] >= 1:
                    user_id = messages['items'][0]['last_message']['peer_id']
                    body = messages['items'][0]['last_message']['text']
                    if body.lower() == vk_key_admin and user_id == vk_id_admin:
                        run_for_all = True
                        run_for_admin = False
                        send_message(user_id, "Бот запущен", None)
        # except Exception as ex:
        #     exc_type, exc_obj, tb = sys.exc_info()
        #     print(tb)
        #     f = tb.tb_frame
        #     lineno = tb.tb_lineno
        #     filename = f.f_code.co_filename
        #     linecache.checkcache(filename)
        #     line = linecache.getline(filename, lineno, f.f_globals)
        #     log = 'Error in {}, line {} "{}": {}\n'.format(filename, lineno, line.strip(), ex)
        #     log_file = open(home_path + "logs.txt", "a")
        #     if run_for_admin:
        #         log = "WARNING. ERROR IN ADMIN MODE. " + log
        #     log_file.write(log)
        #     log_file.close()
        #     time.sleep(1)
        #     if os.stat('logs.txt').st_size > 309600:
        #         exit()
        #     try:
        #         vk._auth_token()
        #     except Exception as ex:
        #         del ex
        #         time.sleep(1)


thread1 = Thread(target=mpei_bot)
thread2 = Thread(target=weekly_update_loop)
thread3 = Thread(target=daily_update_loop)
thread1.start()
thread2.start()
thread3.start()
print("let it burn")
thread1.join()
thread2.join()
thread3.join()
