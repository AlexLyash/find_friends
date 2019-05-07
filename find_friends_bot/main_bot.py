import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

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

def get_token(file_path):
    with open(file_path) as file:
        token = file.read()
    return token


def write_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


# API-ключ
token = get_token("vk_bot_token.txt")
# token = '82ae80bf32f3ed5e1b363a287516063a4440ef2cbd14de516314b3c590dc3ea75ffe2574ee9e90ea5eecf'
# Авторизуемся как сообщество
vk_session = vk_api.VkApi(token=token, app_id=APP_ID)

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

for event in longpoll.listen():

    if event.type == VkEventType.MESSAGE_NEW:

        if event.to_me:

            print('New message:')
            print(f'For me by: {event.user_id}', end=' ')

            # bot = VkBot(event.user_id, vk)

            friends = vk.users.get(user_id=event.user_id, fields='photo_200')
            response = str(friends[0]['photo_200'])
            write_msg(event.user_id, response)
            print(response)
            print()
            # friends = friends['items']
            #
            # friends_temp = [d['id'] for d in friends if 'id' in d]
            # bot.new_message(event.text)
            # write_msg(event.user_id, str(friends_temp))

            print('Text: ', event.text)


