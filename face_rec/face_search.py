from multiprocessing import Process, Manager, Pool
import face_recognition
import functools
import cv2
import os


ALLOWED_FORMATS = {'.jpg', '.jpeg', '.png'}

res_dict = Manager().dict()


def count_distance(filename, pth, unknown_face):

    fileformat = os.path.splitext(filename)[1]

    if fileformat in ALLOWED_FORMATS:
        known_picture = face_recognition.load_image_file(pth + '/' + filename)
        known_picture = cv2.resize(known_picture, (0, 0), fx=0.55, fy=0.55)
        known_picture_encoding = face_recognition.face_encodings(known_picture)

        if len(known_picture_encoding) == 1: #  обрабатываем аватарки только с одним лицом
            known_face_encoding = known_picture_encoding[0]
            res_dict[filename] = face_recognition.face_distance([known_face_encoding], unknown_face)[0]

def get_distances(path_to_dir, unknown_face_enc):
    p = Pool(15)
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
