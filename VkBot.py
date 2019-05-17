import vk_api
import urllib
import requests
import os
from face_rec import search, train_model

from save_friends_photos import get_friends, get_friends_of_friends, save_photos


def get_upload_server():
    r = requests.get('')


def save_unknown_photo(photo_url, photo_dir):
    if not os.path.exists(photo_dir):
        os.makedirs(photo_dir)

    photo_name = photo_dir + "/unknown_photo.jpg"
    photo = requests.get(photo_url).content
    with open(photo_name, 'wb') as handler:
        handler.write(photo)



class VkBot:

    def __init__(self, vk_user, bot_vk, user_id, message_id):
        self.bot_vk = bot_vk
        self.vk_user = vk_user
        self.user_id = user_id
        self.message_id = message_id
        self.commands = ["HELLO", "PHOTO", "TAKE FRIENDS", "TAKE FRIENDS OF FRIENDS", "FIND PERSON", "GOODBYE"]

    def take_photo(self):
        msg = self.bot_vk.method('messages.getById', {'message_ids': self.message_id})
        photo_url = msg['items'][0]['attachments'][0]['photo']['sizes'][2]['url']
        photo_dir = "unknown_photos"
        save_unknown_photo(photo_url, photo_dir)

    def get_friends(self):
        friends = get_friends(self.vk_user, self.user_id)
        save_photos(friends, self.user_id)

    def get_friends_of_friends(self):
        friends = get_friends_of_friends(self.vk_user, self.user_id)
        save_photos(friends, self.user_id)

    def new_message(self, message):
        # Привет
        if message.upper() == self.commands[0]:
            return f"Здарова!"

        # Взять фотографию у пользователя
        elif message.upper() == self.commands[1]:
            self.take_photo()
            return "ваше фото сохранено"

        # Сохранить друзей в файл
        elif message.upper() == self.commands[2]:
            self.get_friends()
            return f"Друзья Сохранены в Папку: " + "friends_photos" + str(self.user_id)

        # Сохранить друзей и друзей друзей в файл
        elif message.upper() == self.commands[3]:
            self.get_friends_of_friends()
            return f"Друзья Друзей Сохранены в Папку: " + "friends_photos" + str(self.user_id)

        # Пока

        elif message.upper() == self.commands[4]:
            if ("friends_photos" + str(self.user_id)) in os.listdir() and 'unknown_photos' in os.listdir():
                face_folder='friends_photos' + str(self.user_id)
                mapper, indexer = train_model.get_indexer(path_to_known_faces=face_folder)
                ans = search.find_person(path_to_unknown_face='unknown_photos/unknown_photo.jpg', indexer=indexer,
                                                                                              mapper=mapper)
                print(ans)
                try:
                    return 'vk.com/id' + str(list(ans.keys())[0])
                except:
                    return f'Совпадений не найдено'
            else:
                return "Сначала нужно загрузить фото(команда 2) и указать список для поиска(команды 3 или 4)"

        elif message.upper() == self.commands[5]:
            return f"Бывай!"

        else:
            return "Не понял!,\n Вот список команд:\n 1.{}\n2.{}\n3.{}\n4.{}\n5.{}\n6.{}\n".format(
                self.commands[0], self.commands[1], self.commands[2], self.commands[3],
                self.commands[4], self.commands[5]
            )
