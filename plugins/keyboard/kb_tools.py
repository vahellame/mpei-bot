# -*- coding: utf-8 -*-

import json


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


def prepare_keyboard(kb):
    kb = json.dumps(kb, ensure_ascii=False).encode('utf-8')
    kb = str(kb.decode('utf-8'))
    return kb


def list_to_keyboard(lst, vyh_button=True):
    buttons = []
    for wrd in lst:
        button = [get_button(label=wrd, color="default")]
        buttons.append(button)
    if vyh_button:
        vyh_button = [get_button(label="Выход", color="negative")]
        buttons.append(vyh_button)
    kb = {
        "one_time": True,
        "buttons": buttons
    }
    kb = prepare_keyboard(kb)
    return kb


def list_to_time_keyboard(time_list):
    buttons = []
    for i in range(len(time_list)):
        time_list[i] = time_list[i][0:2] + ' ' + time_list[i][3:5]
    while len(time_list) > 3:
        buttons_x = time_list[:3]
        buttons.append(buttons_x)
        time_list = time_list[3:]
    buttons.append(time_list)
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            buttons[i][j] = get_button(label=buttons[i][j], color="default")
    vyh_button = [get_button(label="Выход", color="negative")]
    buttons.append(vyh_button)
    kb = {
        "one_time": True,
        "buttons": buttons
    }
    kb = prepare_keyboard(kb)
    return kb
