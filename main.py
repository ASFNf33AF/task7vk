from random import randrange
from config import token_g

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from runner import *
from database import vkinder


token = token_g

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)




def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

def send_photo(user_id, message, attachment):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7), "attachment": ",".join(attachment)})



for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            inputData_user(event.user_id)
            if request == "начать":
                user_data = vkinder.out_data_user(event.user_id)
                user_city = user_data[3]
                user_age = user_data[4]
                user_sex = user_data[1]
                user_relation = user_data[2]
                while user_city == 0 or user_age == 0 or user_sex == 0 or user_relation == 0:   
                    if user_city == 0:
                        write_msg(event.user_id, "Укажите Ваш город (например: 'Балашиха')")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    request = event.text.lower()
                                    request_city = request
                                    user_city = search_city(event.user_id, request_city)
                                    if user_city == "add_region":
                                        user_city = 0
                                        while user_city == 0:
                                            write_msg(event.user_id, f"Укажите Ваш регион (например: 'Московская область')")
                                            for event in longpoll.listen():
                                                if event.type == VkEventType.MESSAGE_NEW:
                                                    if event.to_me:
                                                        request = event.text.lower()
                                                        user_city = search_cityWithRegion(event.user_id, request, request_city)
                                                        break
                                        break
                                    else:
                                        break
                    elif user_age == 0:
                        write_msg(event.user_id, "Укажите Ваш возраст (например: '20')")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    request = event.text.lower()
                                    user_age = new_age(event.user_id, request)
                                    break
                    elif user_sex == 0:
                        write_msg(event.user_id, "Укажите Ваш пол (Мужской/Женский)")
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    request = event.text.lower()
                                    user_sex = new_sex(event.user_id, request)
                                    break
                    elif user_relation == 0:
                        write_msg(event.user_id, '''"Укажите Ваше семейное положение        
                                                       (- не женат/не замужем,
                                                        - есть друг/есть подруга,
                                                        - помолвлен/помолвлена,
                                                        - женат/замужем,
                                                        - все сложно,
                                                        - в активном поиске,
                                                        - влюблен/влюблена,
                                                        - В гражданском браке)''')
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW:
                                if event.to_me:
                                    request = event.text.lower()
                                    user_relation = new_relation(event.user_id, request)
                                    break
                else:
                    data = vkinder.out_data_user(event.user_id)
                    random_profile_id = profile_toUser(event.user_id, data)
                    attachment = photo_profile(random_profile_id)
                    if data[4] >= 18:
                        send_photo(event.user_id, f"Вот кого нашел https://vk.com/id{random_profile_id}", attachment)
                    else:
                        write_msg(event.user_id,  f"Минимальный возраст для пользователей Vkinder — 18 лет.")
            else:
                write_msg(event.user_id, "Чтобы начать подбор напишите слово 'начать'")
