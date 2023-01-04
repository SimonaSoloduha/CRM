from django.core.management.base import BaseCommand
import requests
from django.shortcuts import redirect


class Command(BaseCommand):
    """
    тестовый запрос в API
    """

    def handle(self, *args, **options):
        data = {
            'domen': 'domen.com',
            'packege_id': 'packageName',
            'usser_id': 'XXXX523X3',
            # 'getz_user': 'America/Antigua',
            'getz_user': 'Europe/Kiev',
            'getr_user': 'utm_source=google-play',
            'utm_medium': 'organic',
        }
        # req = requests.post("https://shrouded-ravine-59969.herokuapp.com/index.php", data=data)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        req = requests.get('https://shrouded-ravine-59969.herokuapp.com/index.php')
        req_test = requests.get('https://shrouded-ravine-59969.herokuapp.com/index_test.php')
        req_test_url = 'https://shrouded-ravine-59969.herokuapp.com/index_test.php'
        resp = redirect(req_test_url)

        # req = requests.post("http://127.0.0.1:8000/logs/", data=data)
        # req = requests.get("http://127.0.0.1:8000/logs/")
        # print(HttpResponseRedirect(req_test))

        self.stdout.write(self.style.SUCCESS(f'Done!  {resp}' "\n"))


# #
# data = {
#     "domen": "domen.com",
#     "packege_id": "packageName",
#     "usser_id": "XXXXXXX",
#     "getz_user": "Europe/Kiev",
#     "getr_user": "utm_source=google-play",
#     "utm_medium": "organic"
# }
