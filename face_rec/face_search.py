from multiprocessing import Process, Manager, Pool
import face_recognition
import functools
import os


res_dict = Manager().dict()


def count_distance(filename, pth, unknown_face):

    if filename[-3:] == 'jpg':
        distances = []
        known_picture = face_recognition.load_image_file(pth + '/' + filename)
        known_picture_encoding = face_recognition.face_encodings(known_picture)

# cчитаем дистанции от неизвестного лица до каждого лица на картинках из профилей
        for known_face_encoding in known_picture_encoding:
            distances.append(face_recognition.face_distance([known_face_encoding], unknown_face))

# ставим в соответствие id пользователя минимальную из найденных дистанций
        if len(distances) > 0:
            res_dict[filename] = min(distances)[0]


def get_distances(path_to_dir, unknown_face_enc):
    p = Pool(8)
    list_of_images = os.listdir(path_to_dir)
    p.map(functools.partial(count_distance, pth=path_to_dir, unknown_face=unknown_face_enc), list_of_images)

    p.close()
    p.join()
    return res_dict


def find_person(path_to_unknown_face='unknown_faces/putin.jpg', dir_known_faces='faces'):

    unknown_picture = face_recognition.load_image_file(path_to_unknown_face)
    unknown_picture_encoding = face_recognition.face_encodings(unknown_picture)

    if len(unknown_picture_encoding) > 1:
        print('More than one face detected.')
    elif len(unknown_picture_encoding) == 0:
        print('No faces detected.')
    else:
        unknown_face_encoding = unknown_picture_encoding[0]

        users_dict = get_distances(path_to_dir=dir_known_faces, unknown_face_enc=unknown_face_encoding)
        return dict(sorted(users_dict.items(), key=lambda x: x[1]))
