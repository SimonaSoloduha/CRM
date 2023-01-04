import json

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
    Получение кода старны country_code и таймзоны timezone по ip
    """
    req_test_url = 'https://shrouded-ravine-59969.herokuapp.com/index_test.php'
    response = requests.get(req_test_url)
    # print(response.content)
    # res = json.loads(response.content.decode('utf-8'))
    # response = HttpResponseRedirect(redirect_to=req_test_url)
    # print(response)
    # validated_data['detail_status'] += str(response)
    return response.content

