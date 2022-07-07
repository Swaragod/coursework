import requests
import time
import os.path
import yadisk
from pprint import pprint

with open('token.txt', 'r') as file_token:
    token = file_token.read().strip()
with open('yatoken.txt', 'r') as file_token:
    yatoken = file_token.read().strip()



def get_info(id, token, album='wall', quantity=5, v='5.131'):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': id,
        'album_id': album,
        'count': quantity,
        'extended': 1,
        'photo_sizes': '0',
        'access_token': token,
        'v': v
    }
    res = requests.get(URL, params=params).json()
    return res


all_info = get_info(221059951,token, 'wall', 18)

# def local_files_quantity():
#     files = os.listdir('fotos')
#     return len(files)

def download():
    info = all_info['response']['items']
    quantity = len(info)
    if not os.path.isdir('fotos'):
        os.mkdir('fotos')
    i = 0
    # pprint(info)
    print('Идет скачивание:')
    for foto in info:

        if foto['sizes'][-4]['type'] == 'w':
            foto_url = foto['sizes'][-4]['url']
        else:
            foto_url = foto['sizes'][-1]['url']

        foto_name = str(foto['likes']['count']) + '.jpg'

        path = 'fotos/' + foto_name
        if os.path.exists(path):
            foto_name = str(foto['likes']['count']) + '_' + str(foto['date']) + '.jpg'

        time.sleep(0.34)
        api = requests.get(foto_url)
        i += 1
        bar = round(i / quantity * 100, 1)
        print(foto_name )
        print('..............', ' выполнено ', bar, ' %')

        with open('fotos/%s' % foto_name, 'wb') as file:
            file.write(api.content)

    print('Скачивание завершено.')


def upload():
    ya = yadisk.YaDisk(token=yatoken)
    i = 0
    local_files_quantity = len(os.listdir('fotos'))

    if not ya.exists('coursework'):
        ya.mkdir('coursework')
    time_now = str(f'coursework/{time.strftime("%Y-%m-%d_%H-%M-%S")}/')
    ya.mkdir(time_now)
    print(f'\nНа Яндекс диске создана папка: {time_now}')
    print('Идет загрузка на Яндекс диск:')
    for jpg_file in os.listdir('fotos'):
        local_path = os.path.join('fotos', jpg_file)
        with open(local_path, "rb") as f:
            ya_path = os.path.join(time_now, jpg_file)
            ya.upload(f, ya_path)
        i += 1
        bar = round(i / local_files_quantity * 100, 1)
        print(jpg_file)
        print('..............', ' выполнено ', bar, ' %')
    print('Загрузка завершена.')


print(f"Количество фотографий пользователя {all_info['response']['count']}")

# local_files_quantity()
download()
upload()



