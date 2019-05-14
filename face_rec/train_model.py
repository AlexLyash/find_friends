from annoy import AnnoyIndex
import face_recognition
import cv2
import os
import glob


VEC_SIZE_EMB = 128


def count_encodings(pth):
    '''
    Функция находит лица на фото, кодирует их и добавляет в индекс
    :param pth: путь до папки с пользователями, на которых будет учиться модель
    :return: словарь counter: id пользователя, индекс
    '''
    ALLOWED_FORMATS = {'.jpg', '.jpeg', '.png'}

    counter = 0
    user_id_face_enc_emb = AnnoyIndex(VEC_SIZE_EMB)
    map_counter_2_user_id = {}
    files = glob.iglob(pth + '/*')

    for file_ in files:
        filename = os.path.basename(file_)
        user_id, fileformat = os.path.splitext(filename)

        if fileformat in ALLOWED_FORMATS:
            known_picture = face_recognition.load_image_file(pth + '/' + filename)
            known_picture = cv2.resize(known_picture, (0, 0), fx=0.55, fy=0.55)
            known_picture_encoding = face_recognition.face_encodings(known_picture)

            if len(known_picture_encoding) == 1:  # обрабатываем аватарки только с одним лицом
                known_face_encoding = known_picture_encoding[0]
                user_id_face_enc_emb.add_item(counter, known_face_encoding)
                map_counter_2_user_id[counter] = user_id
                counter += 1

    return map_counter_2_user_id, user_id_face_enc_emb


def get_indexer(path_to_known_faces, num_trees=10):
    '''
    Функция строит деревья
    :param path_to_known_faces: путь до папки с пользователями, на которых будет учиться модель
    :param num_trees: число деревьев
    :return: словарь counter: id пользователя, индекс
    '''
    map_counter_2_user_id, user_id_face_enc_emb = count_encodings(path_to_known_faces)
    user_id_face_enc_emb.build(num_trees)
    return map_counter_2_user_id, user_id_face_enc_emb
