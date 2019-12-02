# -*- coding: utf-8 -*-


from plugins.keyboard.kb_tools import get_button
from plugins.keyboard.kb_tools import prepare_keyboard


# ======================================================================================================================
# Отмена (красный)
# ======================================================================================================================

kb_otm = {
    "one_time": True,
    "buttons": [
        [get_button(label="Отмена", color="negative")]
    ]
}
kb_otm = prepare_keyboard(kb_otm)

# ======================================================================================================================
# Выход (красный)
# ======================================================================================================================

kb_vyh = {
    "one_time": True,
    "buttons": [
        [get_button(label="Выход", color="negative")]
    ]
}
kb_vyh = prepare_keyboard(kb_vyh)

# ======================================================================================================================
# Отмена (красный)
# Выход (красный)
# ======================================================================================================================

kb_otm_vyh = {
    "one_time": True,
    "buttons": [
        [get_button(label="Отмена", color="negative")],
        [get_button(label="Выход", color="negative")]
    ]
}
kb_otm_vyh = prepare_keyboard(kb_otm_vyh)

# ======================================================================================================================
# Записаться на консультацию (синий)
# ======================================================================================================================

kb_main = {
    "one_time": True,
    "buttons": [
        [get_button(label="Записаться на консультацию", color="primary")]
    ]
}
kb_main = prepare_keyboard(kb_main)

# ======================================================================================================================
# Да (белый)
# Нет (белый)
# Выход (красный)
# ======================================================================================================================

kb_yes_no_vyh = {
    "one_time": True,
    "buttons": [
        [get_button(label="Да", color="default")],
        [get_button(label="Нет", color="default")],
        [get_button(label="Выход", color="negative")]
    ]
}
kb_yes_no_vyh = prepare_keyboard(kb_yes_no_vyh)

# ======================================================================================================================
# ЭнМИ (белый)  | ИРЭ (белый)
# ИТАЭ (белый)  | ГПИ (белый)
# ИПЭЭф (белый) | ИнЭИ (белый)
# ИЭТ (белый)   | ИДДО (белый)
# ИЭЭ (белый)   | ВИИ (белый)
# АВТИ (белый)  | ИГВИЭ (белый)
#         Выход (красный)
# ======================================================================================================================

kb_institutes = {
    "one_time": True,
    "buttons": [
        [get_button(label="ЭнМИ", color="default"), get_button(label="ИРЭ", color="default")],
        [get_button(label="ИТАЭ", color="default"), get_button(label="ГПИ", color="default")],
        [get_button(label="ИПЭЭф", color="default"), get_button(label="ИнЭИ", color="default")],
        [get_button(label="ИЭТ", color="default"), get_button(label="ИДДО", color="default")],
        [get_button(label="ИЭЭ", color="default"), get_button(label="ВИИ", color="default")],
        [get_button(label="АВТИ", color="default"), get_button(label="ИГВИЭ", color="default")],
        [get_button(label="Выход", color="negative")]
    ]
}
kb_institutes = prepare_keyboard(kb_institutes)

# ======================================================================================================================
# 1 (белый)  | 2 (белый)
# 3 (белый)  | 4 (белый)
#  Магистратура (белый)
#    Выход (красный)

# ======================================================================================================================

kb_courses = {
    "one_time": True,
    "buttons": [
        [get_button(label="1", color="default"), get_button(label="2", color="default")],
        [get_button(label="3", color="default"), get_button(label="4", color="default")],
        [get_button(label="Магистратура", color="default")],
        [get_button(label="Выход", color="negative")]
    ]
}
kb_courses = prepare_keyboard(kb_courses)
