import json
import os.path
import youtube_dl
import requests
from auth_data import token_vk
import telebot
from auth_data import token_bot



def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def get_info_about_id(user_id):
    url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&count=10&access_token={token_vk}&v=5.131'
    req = requests.get(url)
    data = req.json()
    if 'response' in data:
        return True
    else:
        return False



def download_photo_from_album(photo, user_id, photo_id):
    if not os.path.exists(f'{user_id}/photos'):
        os.makedirs(f'{user_id}/photos')
    res = requests.get(photo)
    with open(f'{user_id}/photos/{photo_id}.jpg', 'wb') as photo_file:
        photo_file.write(res.content)




# функция скачавания фотографий с поста
def download_photo(photo, post_id, user_id):
    if not os.path.exists(f'{user_id}/post_photos'):
        os.makedirs(f'{user_id}/post_photos')
    res = requests.get(photo)
    with open(f'{user_id}/post_photos/{post_id}.jpg', 'wb') as photo_file:
        photo_file.write(res.content)


    # функция для скачивания видео
def download_video(video, post_id, user_id):
    if not os.path.exists(f'{user_id}/post_videos/{post_id}'):
        os.makedirs(f'{user_id}/post_videos')
    try:
        ydl_opts = ({'outtmpl': f'{user_id}/post_videos/{post_id}.mp4'})
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Качаю видео')
            ydl.download([video])
    except:
        print('Не удалось скачать видео')

    # функция для текста поста
def download_text(text, post_id, user_id):
    if not os.path.exists(f'{user_id}/post_texts'):
        os.makedirs(f'{user_id}/post_texts')
    with open(f'{user_id}/post_texts/{post_id}.txt', 'w', encoding="utf-8") as text_file:
        a = f'Пост из группы {user_id}:' + '\n\n' + str(text)
        text_file.write(a)
