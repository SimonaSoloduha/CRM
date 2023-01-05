import json
import bs4

from crm.celery import app
from crm.settings import ABSTRACT_API_URL
import requests


@app.task
def get_location_data(ip_user):
    """
    Получение кода старны country_code и таймзоны timezone по ip
    """
    response = requests.get(ABSTRACT_API_URL + "&ip_address=" + ip_user + "&fields=country_code,timezone")

    res = json.loads(response.content.decode('utf-8'))
    data = {
        'country_code': res['country_code'],
        'timezone': res['timezone']['name'],
    }
    return data


@app.task
def get_check_data():
    """
    Проверка по Magic Checker
    Ответы:
    True - пройдена
    False - не пройдена
    """
    # req_test_url = 'https://shrouded-ravine-59969.herokuapp.com/index_test.php'
    req_test_url = 'https://shrouded-ravine-59969.herokuapp.com/index.php'
    response = requests.get(req_test_url)
    res = response.text
    # html = bs4.BeautifulSoup(response.text, features="lxml")
    # res = ''.join(html.body.text.split())
    if res == 'YES':
        return True
    elif res == 'MAIN':
        return False
    else:
        # Лог
        return False

