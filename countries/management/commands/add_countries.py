from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup

from countries.models import Country


class Command(BaseCommand):
    """
    Команда для добавления стран со списком тайм-зон
    Команда для загрузки: python manage.py add_countries
    """

    def handle(self, *args, **options):
        url = 'https://goodtoolscron.xyz/iso/'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        countries = soup.find_all('a')
        for country in countries:
            if '.txt' in country.text:
                country_name = country.text[:-4]
                url_time_zones = url + country.text
                response_time_zones = requests.get(url_time_zones)
                soup_time_zones = BeautifulSoup(response_time_zones.text, 'lxml')
                time_zones = soup_time_zones.find('p')
                time_zones = time_zones.text.split()
                Country.objects.create(
                    name=country_name,
                    time_zones=time_zones
                )
        count_time_zones = Country.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f'Successfully! Added {count_time_zones} countries'))
