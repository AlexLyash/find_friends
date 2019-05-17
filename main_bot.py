import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

from VkBot import VkBot

API_VERSION = '5.92'
APP_ID = 6973103


# 2FA обработчик
def auth_handler():
    key = input('Введите код двухфакторной аутентификации: ')
    remember_device = True
    return key, remember_device


# captcha обработчик
def captcha_handler(captcha):
    key = input(f"Введите капчу ({captcha.get_url()}): ").strip()
    return captcha.try_again(key)


# для регистрации пользователя через которого будет качать данные
def login_vk(token=None, login=None, password=None):
    try:
        if token:
            vk_session = vk_api.VkApi(token=token, app_id=APP_ID, auth_handler=auth_handler,
                                      api_version=API_VERSION)
        elif login and password:
            vk_session = vk_api.VkApi(login, password, captcha_handler=captcha_handler, app_id=APP_ID,
                                      api_version=API_VERSION, auth_handler=auth_handler)
            vk_session.auth(token_only=True, reauth=True)
        else:
            raise KeyError('Не введен токен или пара логин-пароль')

        return vk_session.get_api()
    except Exception as e:
        print(e)


# получение токена из файла
def get_token(file_path):
    with open(file_path) as file:
        token = file.read()
    return token


# метод для отправки сообщений
def write_msg(vk, user_id, message):
    random_id = random.randint(0, 10e20)
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': random_id})


# API-ключи
token_group = get_token("tokens/vk_bot_token.txt")
token_me = get_token("tokens/my_token.txt")

def listen():
    # авторизация
    vk = vk_api.VkApi(token=token_group)
    vk_me = login_vk(token=token_me)
    
    longpoll = VkLongPoll(vk)
    
    
    # основной цикл
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('New message:')
            print(f'For me by: {event.user_id}', end='')
    
            bot = VkBot(vk_me, vk, event.user_id, event.message_id)
    
            write_msg(vk, event.user_id, bot.new_message(event.text))
    
            print('Text: ', event.text)
