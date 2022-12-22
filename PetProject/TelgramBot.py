import json
import os.path
import youtube_dl
import requests

import Photo
from auth_data import token_vk
import telebot
from telebot import types

from auth_data import token_bot
import Posts
import Functions



bot = telebot.TeleBot(token_bot)
ID = []


@bot.message_handler(commands=['start', 'menu', 'help'])
def start(mess):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_post_content = types.KeyboardButton(text='Получить посты')
    item_album_content = types.KeyboardButton(text='Получить сохры')
    item_group = types.KeyboardButton(text='Новая группа')
    item_photo = types.KeyboardButton(text='Новый альбом')
    item_info = types.KeyboardButton(text='Подключенные ID')

    markup.add(item_group, item_photo, item_info, item_post_content, item_album_content)

    bot.send_message(mess.chat.id, 'Дарова другалек')
    bot.send_message(mess.chat.id, 'Хочешь следить за группой или сохраненками?', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def message(message):

    if message.text == 'Новый альбом':
        bot.send_message(message.chat.id, 'Введи айди странички')



    elif message.text == 'Новая группа':
        bot.send_message(message.chat.id, 'Введи айди группы')

    elif message.text == 'Подключенные ID':
        if len(ID) == 0:
            bot.send_message(message.chat.id, 'Список пуст')
        else:
            mes = ''
            for id in ID:
                mes += (id + '\n')
            bot.send_message(message.chat.id, mes)
    elif message.text == 'Получить сохры':
        if len(ID) == 0:
            bot.send_message(message.chat.id, 'Ваш список ID пуст, добавьте что-нибудь')
        else:
            test = 0
            for id in ID:
                if int(id) > 0:
                    test += 1
            if test == 0:
                bot.send_message(message.chat.id, 'В вашем списке нет сохраненных альбомов, добавьте хотя бы один')
            else:
                bot.send_message(message.chat.id, 'Проверяю')
                for id in ID:
                    if int(id) > 0:
                        id_of_new_photos = Photo.get_photo(id)
                        if len(id_of_new_photos) == 0:
                            bot.send_message(message.chat.id, f'В альбоме юзера с ID {id} нет новых фото')
                        else:
                            for i in id_of_new_photos:
                                mes = []
                                try:
                                    with open(f'{id}/photos/{i}.jpg', 'r') as photo_file:
                                        mes.append(f'{id}/photos/{i}.jpg')
                                    bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in mes])
                                except:
                                    bot.send_message(message.chat.id, 'Фото потерялось по дороге')

    elif message.text == 'Получить посты':

        if len(ID) == 0:
            bot.send_message(message.chat.id, 'Ваш список ID пуст, добавьте что-нибудь')

        else:
            test = 0
            for id in ID:
                if int(id) < 0:
                    test += 1
            if test == 0:
                bot.send_message(message.chat.id, 'В вашем списке нет групп, добавьте хотя бы одну')
            else:
                bot.send_message(message.chat.id, 'Проверяю')
                for id in ID:
                    if int(id) < 0:
                        id_of_new_posts = Posts.get_post(id)
                        if len(id_of_new_posts) == 0:
                            bot.send_message(message.chat.id, f'В группе с ID {id} нет новых постов')
                        else:
                            for i in id_of_new_posts:
                                flag = True
                                mes = []
                                num = 0
                                while flag:
                                    try:
                                        with open(f'{id}/post_photos/{i}_{num}.jpg', 'r') as photo_file:
                                            mes.append(f'{id}/post_photos/{i}_{num}.jpg')
                                        num += 1
                                    except:
                                        flag = False
                                try:

                                    with open(f'{id}/post_texts/{i}.txt', 'r', encoding="utf8") as text_file:
                                        a = text_file.read()
                                        bot.send_message(message.chat.id, a)

                                    bot.send_media_group(message.chat.id, [telebot.types.InputMediaPhoto(open(photo, 'rb')) for photo in mes])
                                    bot.send_message(message.chat.id, '.')
                                    bot.send_message(message.chat.id, '.')
                                    bot.send_message(message.chat.id, '.')
                                except:
                                    pass
                            bot.send_message(message.chat.id, 'Пока все')


    # Проверка на число (если целое число, то может быть ID)
    elif Functions.isint(message.text):
        # Пробный запрос
        if Functions.get_info_about_id(message.text):
            if message.text in ID:
                bot.send_message(message.chat.id, 'Уже есть такой ID, попробуй другой')
            else:
                # если число отрицательное, то это группа, выполняем функции для групп
                if int(message.text) < 0:
                    bot.send_message(message.chat.id, 'Нашел группу, добавляю в базу')
                    ID.append(message.text)
                    bot.send_message(message.chat.id, 'Добавил')



                # значит ссылка на страничку, работаем с сохраненками
                elif int(message.text) > 0:
                    try:
                        bot.send_message(message.chat.id, 'Нашел страничку, добавляю в базу')
                        ID.append(message.text)
                        bot.send_message(message.chat.id, 'Добавил')
                    except:
                        bot.send_message(message.chat.id, 'Не получилось добавить')

        else:
            bot.send_message(message.chat.id, 'Не корректно')

    else:
        bot.send_message(message.chat.id, 'Ниче не пон')


# @bot.callback_query_handler(func=lambda call: True)
# def send_text(call):
#     if call.data == 'posts':
#         bot.send_message(call.chat.id, 'Давай сюда айди')
#     else:
#         bot.send_message(call.chat.id, 'Не пойму тебя, дорогой')

bot.polling()


# if __name__ == '__main__':
    # Posts.main()





