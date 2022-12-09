import requests
import operator
from config import token_u

from random import randrange
from database import *

token = token_u


def inputData_user(user_id, request):

    try:
        URL = "https://api.vk.com/method/users.get"
        params = {
            "user_id": f"{user_id}",
            "access_token": token,
            "v": "5.131",
            "fields": "bdate, city, relation, sex"
        }
        requests_users = requests.get(URL, params=params)
        user_data = requests_users.json()
        city = 0
        relation = 0
        bdate = 0
        sex = 0
        for key, value in user_data["response"][0].items():
            if key == "city":
                city = value["id"]
                break
        for key, value in user_data["response"][0].items():
            if key == "relation":
                relation = value
                break
        for key, value in user_data["response"][0].items():
            if key == "bdate":
                bdate =  value.split(".")[2]
                break
        for key, value in user_data["response"][0].items():
            if key == "sex":
                sex = value
                break
        vkinder.add_user(user_id)
        vkinder.add_data_user(user_id, sex, relation, city, bdate)
        r_error = request
    except:
        r_error = "error"

    return r_error



def search_city(user_id, city_title):

    try:
        URL = "https://api.vk.com/method/database.getCities"
        params = {
            "country_id": "1",
            "q": f"{city_title}",
            "access_token": token,
            "v": "5.131"
        }
        requests_city = requests.get(URL, params=params)
        city_data = requests_city.json()
        count_cities = city_data["response"]["count"]
        moscow = "москва"
        if count_cities == 1 or city_title == moscow:
            city_id = city_data["response"]["items"][0]["id"]
            vkinder.update_city(user_id, city_id)
        elif count_cities == 0:
            city_id = 0
        else:
            city_id = "add_region"
    except:
        city_id = "error"

    return city_id


def search_cityWithRegion(user_id, region_title, city_title):

    try:
        URL = "https://api.vk.com/method/database.getRegions"
        params = {
            "country_id": "1",
            "q": f"{region_title}",
            "access_token": token,
            "v": "5.131"
        }
        requests_regions = requests.get(URL, params=params)
        regions_data = requests_regions.json()
        region_id = regions_data["response"]["items"][0]["id"]
        count_regions = regions_data["response"]["count"]
        if count_regions == 0:
            city_id = 0
        else:
            URL = "https://api.vk.com/method/database.getCities"
            params = {
                "country_id": "1",
                "region_id": f"{region_id}",
                "q": f"{city_title}",
                "count": "1",
                "access_token": token,
                "v": "5.131"
            }
            requests_cities = requests.get(URL, params=params)
            cities_data = requests_cities.json()
            city_id = cities_data["response"]["items"][0]["id"]
            vkinder.update_city(user_id, city_id)
    except:
        city_id = "error"

    return city_id


def new_age(user_id, age):

    new_age = age.isnumeric()
    if new_age == True:
        age_int = int(age)
        if age_int >= 100:
            new_age = 0
        else:
            vkinder.update_age(user_id, age)
    else:
        new_age = 0

    return new_age


def new_sex(user_id, sex):

    if sex == "мужской":
        new_sex = 2
        vkinder.update_sex(user_id, new_sex)    
    elif sex == "женский":
        new_sex = 1
        vkinder.update_sex(user_id, new_sex) 
    else:
        new_sex = 0

    return  new_sex



def new_relation(user_id, relation_status):

    status_dict = {"не женат": 1, "не замужем": 1, 
    "есть друг": 2, "есть подруга": 2, 
    "помолвлен": 3, "помолвлена": 3, 
    "женат": 4, "замужем": 4, 
    "все сложно": 5, 
    "в активном поиске": 6, 
     "влюблен": 7, "влюблена": 7, 
     "в гражданском браке": 8}
    for key, value in status_dict.items():
        if relation_status == key:
            relation = value
            break
        else:
            relation = 0
    vkinder.update_relation(user_id, relation)

    return  relation



def profile_toUser(user_id, data):

    try:
        data_user = data
        sex = data_user[1]
        relation = data_user[2]
        city = data_user[3]
        bdate = 2022 - data_user[4]
        if sex == 1:
            sex = 2
        else:
            sex = 1
        status_one = [3,4,8]
        status_two = [1,6,2,7,5]
        if relation in status_one:
            status_two = status_two + status_one
        else:
            status_two = status_two
        profiles_list = []
        URL = "https://api.vk.com/method/users.search"
        for status in status_two: 
            params = {
                "offset": "10",
                "count": "1000",
                "access_token": token,
                "v": "5.131",
                "city_id": f"{city}",
                "sex": f"{sex}",
                "status": f"{status}",
                "birth_year": f"{bdate}"
            }
            requests_profiles = requests.get(URL, params=params)
            profiles_data = requests_profiles.json()
            for key in profiles_data.items():
                if key == "error":
                    continue
                else:
                    for close_profile in profiles_data["response"]["items"]:
                        if close_profile["is_closed"] == True:
                            continue
                        else:
                            profiles_list.append(close_profile["id"])
        lenght_profiles = len(profiles_list)
        add_profile = False
        random_profile = randrange(lenght_profiles)
        random_profile_id = 0
        while add_profile is False:
            random_profile_id = profiles_list[random_profile]
            add_profile = vkinder.add_profileToUser(user_id, random_profile_id)
    except:
        random_profile_id = "error"

    return random_profile_id


def photo_profile(random_profile_id):

    try:
        URL = "https://api.vk.com/method/photos.get"
        params = {
            "owner_id": f"{random_profile_id}",
            "album_id": "profile",
            "extended": "1",
            "access_token": token,
            "v": "5.131"
        }
        requests_photos = requests.get(URL, params=params)
        photos_data = requests_photos.json()
        dict_photos = {}
        for img in photos_data["response"]["items"]:
            photo = f"photo{img['owner_id']}_{img['id']}"  
            dict_photos[photo] = [img["likes"]["count"], img["comments"]["count"]]
        sortedDict = sorted(dict_photos.items(), key=operator.itemgetter(1), reverse=True)
        list_top_photos = []
        if len(sortedDict) >= 3: 
            count_photo = 0
            while count_photo <= 2:
                list_top_photos.append(sortedDict[count_photo][0])
                count_photo += 1 
        else:
            count_photo = 0
            while count_photo <= len(sortedDict)-1:
                list_top_photos.append(sortedDict[count_photo][0])
                count_photo += 1 
    except:
        list_top_photos = "error" 

    return list_top_photos