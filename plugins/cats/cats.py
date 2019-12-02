# -*- coding: utf-8 -*-

from consts import home_path

from vk_tools import file_to_doc_attachment
from vk_tools import send_message


def make_cats(vk_id):
    cats_list = []
    for i in range(1, 13):
        attachment = file_to_doc_attachment(vk_id, home_path + "plugins/cats/cat" + str(i) + ".gif")
        send_message(vk_id, "", attachments=attachment)
        cats_list.append(attachment)
    return cats_list
