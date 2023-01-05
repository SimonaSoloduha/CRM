from django.db import transaction
from rest_framework import serializers

from companies.models import Company
from countries.models import Country
from logs.models import Log, STATUS_FILTER_OFF, STATUS_FILTER_NOT_STARTED
from logs.tasks import get_location_data
from logs.utils import check_update_date_from_last_visit, check_update_user_agent, \
    check_filter_one_time_zone, create_new_client, check_filter_two_cheker, check_users_status_ban_and_divice_ban
from users.models import Client


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ['domen', 'packege_id', 'usser_id', 'getz_user', 'getr_user', 'utm_medium', ]

    def get_ip(self, validated_data):
        """
        Извление ip
        """
        if 'HTTP_X_FORWARDED_FOR' in self.context.get('request').META:
            ip_adds = self.context.get('request').META['HTTP_X_FORWARDED_FOR'].split(",")
            ip = ip_adds[0]
            validated_data['ip'] = ip
            validated_data['detail_status'] += self.context.get('request').META
        else:
            ip = self.context.get('request').META['REMOTE_ADDR']
            validated_data['ip'] = ip
            validated_data['detail_status'] += self.context.get('request').META
        if not ip:
            validated_data['detail_status'] = 'Не удалось извлечь IP '
        # ip = '80.90.237.83'
        # validated_data['ip'] = ip
        return ip

    def get_country(self, country_code_from_header, validated_data):
        """
        Извление country
        """
        country = Country.objects.get(name=country_code_from_header)
        validated_data['country'] = country
        return country

    def get_country_code_from_header(self, location):
        """
        Извление country_code_from_header
        """
        country_code_from_header = location['country_code']
        return country_code_from_header

    def get_timezone_from_headers(self, location, validated_data):
        """
        Извление timezone_from_header
        """
        timezone_from_header = location['timezone']
        validated_data['timezone_from_header'] = timezone_from_header
        return timezone_from_header

    def get_getz_user(self, validated_data):
        """
        Извление getz_user
        """
        getz_user = validated_data.get('getz_user')
        return getz_user

    def get_user_agent(self, validated_data):
        """
        Извление USER_AGENT
        """
        user_agent = self.context.get('request').META.get("HTTP_USER_AGENT")
        validated_data['user_agent'] = user_agent
        return user_agent

    def get_usser_id(self, validated_data):
        """
        Извление usser_id
        """
        usser_id = validated_data.get('usser_id')
        return usser_id

    def get_domen(self, validated_data):
        """
        Извление domen
        """
        domen = validated_data.get('domen')
        return domen

    def get_detail_status(self, validated_data):
        """
        Создание пустого detail_status
        """
        validated_data['detail_status'] = ''

    def get_company(self, domen, validated_data):
        """
        Поиск компании по домену
        """
        try:
            # Если есть компания с доменом - добавляем логу компанию
            company = Company.objects.get(domen=domen)
        except Company.DoesNotExist:
            # Если нет компании с доменом киента - ставим пропуск
            company = None
            validated_data['detail_status'] += ' Не удалось извлечь IP /'
        validated_data['company'] = company
        return company

    def get_filters_status(self, company, validated_data):
        """
        Статус фильтров (включены или отключены)
        """
        if company:
            if company.active_filter_one_time_zone:
                validated_data['filter_one_time_zone'] = STATUS_FILTER_NOT_STARTED
            else:
                validated_data['filter_one_time_zone'] = STATUS_FILTER_OFF
            if company.filter_two_cheker:
                validated_data['filter_two_cheker'] = STATUS_FILTER_NOT_STARTED
            else:
                validated_data['filter_two_cheker'] = STATUS_FILTER_OFF

    @transaction.atomic
    def create(self, validated_data):
        # detail_status
        self.get_detail_status(validated_data)
        # ip
        ip = self.get_ip(validated_data)
        # location
        location = get_location_data(ip)
        # country_code_from_header
        country_code_from_header = self.get_country_code_from_header(location)
        # country
        country = self.get_country(country_code_from_header, validated_data)
        # timezone from headers
        timezone_from_header = self.get_timezone_from_headers(location, validated_data)
        # getz_user
        getz_user = self.get_getz_user(validated_data)
        # headers / user_agent
        user_agent = self.get_user_agent(validated_data)
        # usser_id
        usser_id = self.get_usser_id(validated_data)
        # domen
        domen = self.get_domen(validated_data)
        # # detail_status
        # self.get_detail_status(validated_data)
        # company
        company = self.get_company(domen, validated_data)
        # filters
        self.get_filters_status(company, validated_data)
        # url
        url = f'{domen}/?packageid={validated_data.get("packageid")}&usserid={usser_id}&getz={getz_user}&getr={validated_data.get("getr")}&utm_medium={validated_data.get("utm_medium")}'
        try:
            # Клиент есть в БД
            client = Client.objects.get(usser_id=usser_id)
            validated_data['client'] = client
            # Проверка статусов 'USER BAN' и 'DEVICE BANNED'
            if check_users_status_ban_and_divice_ban(client, validated_data):
                last_log = Log.objects.filter(client=client).latest('created_at')
                if check_update_date_from_last_visit(client, last_log, ip, getz_user, timezone_from_header,
                                                     country_code_from_header, validated_data):
                    # ПРОВЕРКА НА ВИРТУАЛЬНОЕ УСТРОЙСТВО ( СРАВНИВАЕМ USER-AGENT)
                    if check_update_user_agent(client, last_log, user_agent, validated_data):
                        # Go to filter 1
                        if check_filter_one_time_zone(client, country, getz_user, validated_data):
                            # Go to filter 2
                            if check_filter_two_cheker(url, user_agent, client, validated_data):
                                # фильтр 2 пройден или отключен
                                validated_data['final'] = True

        except Client.DoesNotExist:
            # Клиента нет в БД
            client = create_new_client(usser_id, company, validated_data)
            # Go to filter 1
            if check_filter_one_time_zone(client, country, getz_user, validated_data):
                # Go to filter 2
                if check_filter_two_cheker(url, user_agent, client, validated_data):
                    validated_data['final'] = True

        return Log.objects.create(**validated_data)
