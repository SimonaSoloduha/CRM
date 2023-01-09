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
