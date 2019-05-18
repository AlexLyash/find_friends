import face_recognition
import cv2

def find_person_dict(unk_photo, indexer, mapper, threshold=0.7):
    '''
    Функция находит лицо на фото, кодирует его и ищет похожие лица
    :param unk_photo: векторное представление картинки с человеком которого ищем
    :param indexer: объект annoy.Annoy, обученный на известных лицах
    :param mapper: словарь, который ставит в соответствие номеру вектора из indexer id пользователя
    :param threshold: порог, выше которого лица считаются похожими
    :return: словарь, в котором ключ - id найденных пользователей, значение - насколько найденные лица
        близки к искомому(чем больше значение, тем ближе); None, если нет похожих лиц
    '''
    if unk_photo.ndim == 2:
        unk_photo = cv2.cvtColor(unk_photo,cv2.COLOR_GRAY2RGB)
    if unk_photo.ndim == 3:
        unknown_picture_encoding = face_recognition.face_encodings(unk_photo)
    
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