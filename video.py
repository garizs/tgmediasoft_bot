import re
import requests


# Метод получения названия видео
def vid_info(url):
    response = requests.get(url).text
    result = {
        'title': re.findall(r'"title":"[^>]*",', response)[0].split(',')[0][9:-1],
    }
    return result
