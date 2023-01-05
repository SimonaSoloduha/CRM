from django.core.management.base import BaseCommand
import requests
from django.shortcuts import redirect


class Command(BaseCommand):
    """
    тестовый запрос в API
    """

    def handle(self, *args, **options):
        # data = {
        #     'domen': 'domen.com',
        #     'packege_id': 'packageName',
        #     'usser_id': 'XXXX523X3',
        #     # 'getz_user': 'America/Antigua',
        #     'getz_user': 'Europe/Kiev',
        #     'getr_user': 'utm_source=google-play',
        #     'utm_medium': 'organic',
        # }
        # req = requests.post("https://shrouded-ravine-59969.herokuapp.com/index.php", data=data)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        url = 'https://shrouded-ravine-59969.herokuapp.com/index.php'
        session = requests.Session()
        response = session.get(
            url, headers={
                # 'Host': '80.90.237.83',
                'User-Agent': user_agent,
                'url': 'domen.com/?packageid=com.vexxhalkaskplay&usserid=661a1d49-6cff-43cb-9aa8-a52806e804ba&getz=Asia/Krasnoyarsk&getr=utm_source=google-play&utm_medium=organic'
            }, verify=False)
        resp = response.content
        # print(response.content, '*******')

        # self.stdout.write(self.style.SUCCESS(f'Done!  {resp}' "\n"))

# #
# data = {
#     "domen": "domen.com",
#     "packege_id": "packageName",
#     "usser_id": "XXXXXXX",
#     "getz_user": "Europe/Kiev",
#     "getr_user": "utm_source=google-play",
#     "utm_medium": "organic"
# }
# getz=Asia/Krasnoyarsk&getr=utm_source=google-play&utm_medium=organic
# data = {
#     "domen": "domen.com",
#     "packege_id": "com.vexxhalkaskplay",
#     "usser_id": "661a1d49-6cff-43cb-9aa8-a52806e804ba",
#     "getz_user": "Asia/Krasnoyarsk",
#     "getr_user": "utm_source=google-play",
#     "utm_medium": "organic"
# }
