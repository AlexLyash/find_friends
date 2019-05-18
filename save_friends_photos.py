import requests
import imageio
import time
import multiprocessing 
from itertools import product

manager = multiprocessing.Manager()
shared_dict = manager.dict()

# друзья могут повторяться
def delete_repeating(l):
    '''
    друзья могут повторяться
    :param массив:
    :return: массив без повторений
    '''
    n = []
    for i in l:
        if i not in n:
            n.append(i)
    return n


def download_photo(d, user_id: str, friend_id: str, url: str):
    photo_bytes = requests.get(url).content
    photo = imageio.imread(photo_bytes)
    d[friend_id] = photo
    
    
def save_photos(friends, user_id):
    '''
    сохранение фотографий в папку "friends_photos + user_id"
    вск файлы называются "photo + friend_id"
    :param: friends - словарь с друзьями
    :param user_id
    '''
    photo_dict = {}
#    photo_dict[str(user_id)] = {}
    i = 0
    start_time = time.time()
    print('Number of profiles =', len(friends))
    tasks = []
    for friend in friends:
        try:
            friend['photo_200']
        except KeyError:
            continue
        if friend['photo_200'] == "https://vk.com/images/camera_200.png?ava=1" or \
                friend['photo_200'] == "https://vk.com/images/deactivated_200.png" or \
                friend['photo_200'] is None:
            continue
        tasks.append((shared_dict, str(user_id), friend['id'], friend['photo_200']))
    with multiprocessing.Pool(70) as p:
        p.starmap(download_photo, tasks)
    photo_dict[str(user_id)] = shared_dict
    print('photos are downloaded')
    print(time.time()-start_time)    
    return photo_dict


def get_friends(vk, user_id):
    '''
    получить своих друзей
    :param vk: мой vk api для парсинга
    :return: лист словарей с друзьями
    '''
    try:
        friends = vk.friends.get(user_id=user_id, fields='photo_200')['items']
        return friends
    except:
        return [{'id': None,
                 'first_name': None,
                 'last_name': None,
                 'is_closed': None,
                 'can_access_closed': None,
                 'photo_200': None,
                 'online': None}]


def get_friends_of_friends(vk, user_id):
    '''
    получить друзей друзей
    :param vk: мой vk api для парсинга
    :return: лист словарей с друзьями и друзьями друзей
    '''
    friends = get_friends(vk, user_id)
    friends_id = [d['id'] for d in friends if 'id' in d]
    for friend in friends_id:
        friends.extend(get_friends(vk, friend))

    friends_non_repeating = delete_repeating(friends)

    return friends_non_repeating

