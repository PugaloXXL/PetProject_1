import json
import os.path
import youtube_dl
import requests
from auth_data import token_vk
import Functions
import telebot
from auth_data import token_bot

# 165200556
# -28905875
# -99099155



def get_post(user_id):
    # формируем запрос и забираем данные
    url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&count=10&access_token={token_vk}&v=5.131'
    req = requests.get(url)
    data = req.json()
    posts = data['response']['items']

    # если первый раз, то создается директория
    if os.path.exists(f'{user_id}'):
        print('Данная группа уже добавлен в базу')
    else:
        print('Впервые слышу про эту группу, щас гляну')
        os.mkdir(str(user_id))

    # сохраняем данные в json файле
    with open(f'{user_id}/{user_id}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # собираем айдишники постов
    new_posts = []                      # пойдет потом на выход из функции
    new_posts_id = []
    for posts_id in posts:
        id = str(posts_id['id'])
        new_posts_id.append(id)

    photo_types = ['w', 'z', 'y', 'x', 'r', 'q', 'p', 'o', 's']             # типы разрешений фотографий

    # 2 варианта: Если файла в директории нету, то это первый просмотр и он создается
    # если файл есть, то будем сравнивать данные с ним, и оставлять только новые посты (которых нет в файле)

    if not os.path.exists(f'{user_id}/posts_id_{user_id}.txt'):
        print('Первый просмотр')
        with open(f'{user_id}/posts_id_{user_id}.txt', 'w') as file:
            for i in new_posts_id:
                file.write(str(i) + '\n')
                new_posts.append(str(i))                            # это потом выйдет из функции
        # проходимся по каждому посту
        for p in posts:
            Functions.download_text(p['text'], p['id'], p['owner_id'])
            numeretor_item = 0
            try:

                # проходимся по каждому итему в посте (прикрепленные штуки)
                for post_item in p['attachments']:
                    post_id = p['id']

                    # если это фото, то прокручиваем цикл для нахождения максимально качественного расширения
                    if post_item['type'] == 'photo':
                        flag = False
                        numerator_types = 0
                        while not flag:
                            for size in post_item['photo']['sizes']:
                                if size['type'] == photo_types[numerator_types]:
                                    photo = size['url']
                                    post_id = str(post_id) + f'_{numeretor_item}'
                                    numeretor_item += 1
                                    print(size['type'] + '\n' + photo + '\n')
                                    Functions.download_photo(photo,  post_id, user_id)
                                    flag = True
                                    break
                            numerator_types += 1

                    # если видео, формируем запрос
                    elif post_item['type'] == 'video':
                        print('Видео')
                        access_key = post_item['video']['access_key']
                        video_id = post_item['video']['id']
                        owner_id = post_item['video']['owner_id']
                        video_url = f'https://api.vk.com/method/video.get?videos={owner_id}_{video_id}_{access_key}&access_token={token_vk}&v=5.131'
                        req = requests.get(video_url)
                        res = req.json()
                        video = res['response']['items'][0]['player']
                        post_id = str(post_id) + f'_{numeretor_item}'
                        Functions.download_video(video, post_id, user_id)
                        numeretor_item += 1
                        print(video)

                    else:
                        print('аудио, ссылка, без фото или др')

            except:
                print('что-то не то')
        print('Файл с постами создан')

    # мы тут, потому что ранее данная группа просматривалас и нам нужно проверить на новые посты и вывести их
    else:
        print('Файл есть, проверка на новые посты')

        with open(f'{user_id}/posts_id_{user_id}.txt', 'r') as file:
            file = [line.strip() for line in file]

            for id in new_posts_id:
                if str(id) not in file:
                    new_posts.append(id)

        if len(new_posts) == 0:
            print('Новых постов нет')

        else:
            print('Появились новые посты')
            for post in new_posts:
                for p in posts:
                    if str(p['id']) == post:
                        numeretor_item = 0
                        try:
                            # проходимся по каждому итему в посте (прикрепленные штуки)
                            for post_item in p['attachments']:
                                post_id = p['id']

                                # если это фото, то прокручиваем цикл для нахождения максимально качественного расширения
                                if post_item['type'] == 'photo':
                                    flag = False
                                    numerator_types = 0
                                    while not flag:
                                        for size in post_item['photo']['sizes']:
                                            if size['type'] == photo_types[numerator_types]:
                                                photo = size['url']
                                                post_id = str(post_id) + f'_{numeretor_item}'
                                                numeretor_item += 1
                                                print(size['type'] + '\n' + photo + '\n')
                                                Functions.download_photo(photo,  post_id, user_id)
                                                flag = True
                                                break
                                        numerator_types += 1

                                # если видео, формируем запрос
                                elif post_item['type'] == 'video':
                                    print('Видео')
                                    access_key = post_item['video']['access_key']
                                    video_id = post_item['video']['id']
                                    owner_id = post_item['video']['owner_id']
                                    video_url = f'https://api.vk.com/method/video.get?videos={owner_id}_{video_id}_{access_key}&access_token={token_vk}&v=5.131'
                                    req = requests.get(video_url)
                                    res = req.json()
                                    video = res['response']['items'][0]['player']
                                    post_id = str(post_id) + f'_{numeretor_item}'
                                    Functions.download_video(video, post_id, user_id)
                                    numeretor_item += 1
                                    print(video)

                                else:
                                    print('аудио, ссылка, без фото или др')

                        except:
                            print('что-то не то')
            # обновляем файл айдишников
            with open(f'{user_id}/posts_id_{user_id}.txt', 'a') as file:
                for i in new_posts:
                    file.write(str(i) + '\n')

    return new_posts

def main():
    user_id = input('введите id: ')
    get_post(user_id)

if __name__ == '__main__':
    main()


