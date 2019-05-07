import vk_api


class VkBot:

    def __init__(self, user_id, vk):

        self.user_id = user_id
        self.vk = vk

        self.commands = ["ПРИВЕТ", "ДРУЗЬЯ", "ДРУЗЬЯ ДРУЗЕЙ", "ПОКА"]

    def get_friends(self):
        try:
            friends = self.vk.friends.get(user_id=self.user_id, fields='photo_200_orig')
            friends = friends['items']
        except:
            friends = [{'id': None,
                        'first_name': None,
                        'last_name': None,
                        'is_closed': None,
                        'can_access_closed': None,
                        'photo_200_orig': None,
                        'online': None}]

        friends_temp = [d['id'] for d in friends if 'id' in d]
        return friends_temp

    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    def new_message(self, message):

        # Привет
        if message.upper() == self.commands[0]:
            return f"Здарова!"

        # Погода
        elif message.upper() == self.commands[1]:
            return str(self.get_friends())

        # Время
        elif message.upper() == self.commands[2]:
            return self.commands

        # Пока
        elif message.upper() == self.commands[3]:
            return f"Бывай!"

        else:
            return "Не понял!"
