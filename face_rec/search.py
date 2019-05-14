import face_recognition
import os


def find_person(path_to_unknown_face, indexer, mapper, threshold=0.7):
    '''
    Функция находит лицо на фото, кодирует его и ищет похожие лица
    :param path_to_unknown_face: путь до картинки с человеком, которого ищем
    :param indexer: объект annoy.Annoy, обученный на известных лицах
    :param mapper: словарь, который ставит в соответствие номеру вектора из indexer id пользователя
    :param threshold: порог, выше которого лица считаются похожими
    :return: словарь, в котором ключ - id найденных пользователей, значение - насколько найденные лица
        близки к искомому(чем больше значение, тем ближе); None, если нет похожих лиц
    '''
    ALLOWED_FORMATS = {'.jpg', '.jpeg', '.png'}

    fileformat = os.path.splitext(path_to_unknown_face)[1]

    if fileformat in ALLOWED_FORMATS:
        unknown_picture = face_recognition.load_image_file(path_to_unknown_face)
        unknown_picture_encoding = face_recognition.face_encodings(unknown_picture)

        if len(unknown_picture_encoding) > 1:
            print('More than one face detected.')
        elif len(unknown_picture_encoding) == 0:
            print('No faces detected.')
        else:
            users_dict = {}

            unknown_face_encoding = unknown_picture_encoding[0]
            most_similar = list(indexer.get_nns_by_vector(unknown_face_encoding, 5, include_distances=True))

            for (counter, distance) in zip(*most_similar):
                similarity = 1 - distance ** 2 / 2
                if similarity >= threshold:
                    user_id = mapper[counter]
                    users_dict[user_id] = similarity
                else:
                    continue

    # Если похожие лица не найдены, возвращаем None
    # в противном случае - словарь с ключами-user_id и значениями-similarity
            if len(users_dict.items()) == 0:
                return None
            else:
                return users_dict

    else:
        print(f"Wrong format. Only {ALLOWED_FORMATS} formats are allowed.")
