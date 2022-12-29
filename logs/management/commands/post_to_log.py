from django.core.management.base import BaseCommand
import requests


class Command(BaseCommand):
    """
    тестовый запрос в API
    """

    def handle(self, *args, **options):

        data = {
            'domen': 'domen12332312.com',
            'packege_id': 'packageName',
            'usser_id': 'XXXXXXX3X14323213',
            # 'getz_user': 'America/Antigua',
            'getz_user': 'Europe/Kiev',
            'getr_user': 'utm_source=google-play',
            'utm_medium': 'organic',
        }

        req = requests.post("http://127.0.0.1:8000/logs/", data=data)
        # req = requests.get("http://127.0.0.1:8000/logs/")

        self.stdout.write(self.style.SUCCESS(f'Done!  {req}'))
