# -*- coding: utf-8 -*-

import pandas as pd

from consts import vk
from consts import home_path


def check_param(vk_id, param, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    res = df[df["vk_id"] == vk_id]
    return res[param].any()


def take_param(vk_id, param, db_path):
    res = ""
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    if not df.empty:
        res = df[df["vk_id"] == vk_id][param].iloc[0]
        res = str(res)
    return res


def check_admin(vk_id, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    res = df[df["vk_id"] == vk_id]
    if res["Admin"].iloc[0] == 2:
        return True
    else:
        return False


def check_just_dialog(vk_id, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    for param in list(df)[4:]:
        if check_param(vk_id, param, db_path):
            return False
    return True


def back_just_dialog(vk_id, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    for col in list(df)[4:]:
        set_param(vk_id, col, 0, db_path)


def set_param(vk_id, param, k, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    df.loc[df["vk_id"] == vk_id, param] = k
    df.to_csv(home_path + db_path, index=False, encoding='utf-8')


def create_clear_str(vk_id, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    user_info = vk.method("users.get",
                          {"user_ids": vk_id, "fields": "first_name", "fields": "last_name", "fields": "sex"})
    new_user_list = list(df)
    new_user = {item: 0 for item in new_user_list}
    new_user["vk_id"] = vk_id
    new_user["name"] = user_info[0]["first_name"]
    new_user["surname"] = user_info[0]["last_name"]
    new_user["sex"] = user_info[0]["sex"]
    df = df.append(new_user, ignore_index=True)
    df.to_csv(home_path + db_path, encoding='utf-8', index=False)


def check_id(vk_id, db_path):
    df = pd.read_csv(home_path + db_path, header=0, encoding='utf-8')
    result = df[df["vk_id"] == vk_id]
    if len(result) == 0:
        create_clear_str(vk_id, db_path)
        return None
    return result

