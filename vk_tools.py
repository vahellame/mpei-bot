# -*- coding: utf-8 -*-

import random
import requests

from consts import vk
from consts import home_path


def file_to_photo_attachment(vk_id, filename):
    photo = open(filename, 'rb')
    met_1 = vk.method("photos.getMessagesUploadServer", {"type": "doc", "peer_id": vk_id})
    req = requests.post(met_1['upload_url'], files={'photo': photo}).json()
    met_2 = vk.method('photos.saveMessagesPhoto',
                      {'photo': req['photo'], 'server': req['server'], 'hash': req['hash']})[0]
    photo_url = 'photo{}_{}'.format(met_2["owner_id"], met_2["id"])
    photo.close()
    return photo_url


def file_to_doc_attachment(vk_id, filename):
    doc = open(filename, "rb")
    met_1 = vk.method("docs.getMessagesUploadServer", {"type": "doc", "peer_id": vk_id})
    req = requests.post(met_1["upload_url"], files={"file": doc}).json()
    met_2 = vk.method("docs.save", {"file": req["file"], "title": filename})
    doc_url = "doc{}_{}".format(met_2["doc"]["owner_id"], met_2["doc"]["id"])
    doc.close()
    return doc_url


def send_message(vk_id, message, keyboard=None, attachments=None):
    if type(attachments) == str:
        attachments = [attachments]
    elif attachments is None:
        attachments = []
    vk.method("messages.send",
              {"peer_id": vk_id,
               "message": message,
               "keyboard": keyboard,
               "attachment": ','.join(attachment for attachment in attachments),
               "random_id": random.randint(1, 2147483647)})
