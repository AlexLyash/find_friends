from annoy import AnnoyIndex
import face_recognition
import cv2


VEC_SIZE_EMB = 128


def count_encodings_dict(data:dict):
    '''
    Функция находит лица на фото, кодирует их и добавляет в индекс
    :param data: словарь в котором ключи это id пользователя,
    а значения - байтовое представление фото, на которых будет учиться модель
    :return: словарь counter: id пользователя, индекс
    '''
    counter = 0
    user_id_face_enc_emb = AnnoyIndex(VEC_SIZE_EMB)
    map_counter_2_user_id = {}
    #files = glob.iglob(pth + '/*')

    for user_id, photo in data.items():

        if photo.ndim == 3:

            known_picture = cv2.resize(photo, (0, 0), fx=0.55, fy=0.55)
            known_picture_encoding = face_recognition.face_encodings(known_picture)

            if len(known_picture_encoding) == 1:  # обрабатываем аватарки только с одним лицом
                known_face_encoding = known_picture_encoding[0]
                user_id_face_enc_emb.add_item(counter, known_face_encoding)
                map_counter_2_user_id[counter] = user_id
                counter += 1
        else:
            print('strange photo, used_id =', user_id)
    return map_counter_2_user_id, user_id_face_enc_emb



def get_indexer(path_to_known_faces, num_trees=10):
    '''
    Функция строит деревья
    :param path_to_known_faces: путь до папки с пользователями, на которых будет учиться модель
    :param num_trees: число деревьев
    :return: словарь counter: id пользователя, индекс
    '''
    map_counter_2_user_id, user_id_face_enc_emb = count_encodings_dict(path_to_known_faces)
    user_id_face_enc_emb.build(num_trees)
    return map_counter_2_user_id, user_id_face_enc_emb
