import json
import os.path
import requests
import Functions
from auth_data import token_vk


# 165200556

def get_photo(user_id):
    url = f'https://api.vk.com/method/photos.get?owner_id={user_id}&album_id=saved&count=10&rev=1&access_token={token_vk}&v=5.131'
    req = requests.get(url)
    data = req.json()

    print(req)
    if os.path.exists(f'{user_id}'):
        print('Данный пользователь уже добавлен в базу')
    else:
        os.mkdir(user_id)

    with open(f'{user_id}/{user_id}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    photo_types = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 's']
    photos = data['response']['items']
    new_photos_id = []
    new_photos = []

    for photos_id in photos:
        id = photos_id['id']
        new_photos_id.append(id)

    if not os.path.exists(f'{user_id}/photos_id_{user_id}.txt'):
        print('Файсла с айди нету, щас сделаем')
        with open(f'{user_id}/photos_id_{user_id}.txt', 'w') as file:
            for i in new_photos_id:
                file.write(str(i) + '\n')
                new_photos.append(i)


        for ph in photos:
            try:
                flag = False
                for pt in photo_types:
                    for size in ph['sizes']:
                        if size['type'] == pt:
                            print(pt)
                            photo = size['url']
                            print(photo)
                            Functions.download_photo_from_album(photo, user_id, ph['id'])
                            flag = True
                            break
                    if flag:
                        break
            except:
                print('что-то не то')
    else:
        print('Файл есть, проверка на новые посты')

        with open(f'{user_id}/photos_id_{user_id}.txt', 'r') as file:
            file = [line.strip() for line in file]

            for id in new_photos_id:
                if str(id) not in file:
                    new_photos.append(id)

        if len(new_photos) == 0:
            print('Новых постов нет')

        else:
            print('Появились новые посты')
            for ph in new_photos:
                for p in photos:
                    if str(p['id']) == ph:
                        try:
                            flag = False
                            for pt in photo_types:
                                for size in ph['sizes']:
                                    if size['type'] == pt:
                                        print(pt)
                                        photo = size['url']
                                        print(photo)
                                        Functions.download_photo_from_album(photo, user_id, ph['id'])
                                        flag = True
                                        break
                                if flag:
                                    break
                        except:
                            print('что-то не то')

            # обновляем файл айдишников
            with open(f'{user_id}/photos_id.txt', 'a') as file:
                for i in new_photos:
                    file.write(str(i) + '\n')

    return new_photos




def main():
    user_id = input('введите id: ')
    get_photo(user_id)

if __name__ == '__main__':
    main()
