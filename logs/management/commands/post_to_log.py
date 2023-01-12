from django.core.management.base import BaseCommand
import requests
import bs4
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
        ip = '10.1.24.126'
        host = '90.324'
        # host = 'h83.onetel237.onetelecom.od.ua'
        new_id = 12345
        user_url = 'domen.com/?packageid=com.vexxhalkaskplay&usserid=ff4f9347625rebgshagfshfvdghf&getz=Europe/Kiev&getr=utm_source=google-play&utm_medium=organic'
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        url = f'https://shrouded-ravine-59969.herokuapp.com/index_test.php?{user_url}?&id={new_id}?country=UA'
        session = requests.Session()
        data = {
            'COUNTRY': 'UA'
        }
        response = session.get(
            url, headers={
                'Accept-Language': 'us',
                'REMOTE_ADDR': ip,
                'X-Country-Code': 'DE',
                # 'REMOTE_ADDR': 'UA',
                'Referer': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript',
                'Access-Control-Request-Headers': 'Vodafone',
                'User-Agent': user_agent,
                'URL': 'domen.com/?packageid=com.vexxhalkaskplay&usserid=661a1d49-6cff-43cb-9aa8-a52806e804ba&getz=Asia/Krasnoyarsk&getr=utm_source=google-play&utm_medium=organic'
            }, data=data, verify=False)
        # print(response.headers['Access-Control-Expose-Headers'])
        html = bs4.BeautifulSoup(response.text, features="lxml")
        res = ''.join(html.body.text.split())
        # print(res, '*******')

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

# https://damp-everglades-01529.herokuapp.com/logs/?domen=domen.com/%3Fpackageid=com.vexxhalkaskplay&usserid=ff4f9347625rebgshagfshfvdghf&getz=Europe/Kiev&getr=utm_source=google-play&utm_medium=organic
# 127.0.0.1:8000/logs/?domen=domen.com/%3Fpackageid=com.vexxhalkaskplay&usserid=661ad443c9aa8-a52806e804ba&getz=Europe/Kiev&getr=utm_source=google-play&utm_medium=organic