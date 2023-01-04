from django.db import transaction

from rest_framework import serializers


from companies.models import Company
from countries.models import Country
from logs.models import Log, STATUS_STOP_TIMEZONE, STATUS_SUCCESSFUL, STATUS_FILTER_OFF, STATUS_FILTER_NOT_STARTED
from logs.tasks import get_location_data, get_check_data
from logs.utils import update_status, check_update_date_from_last_visit, check_update_user_agent, \
    check_filter_one_time_zone, create_new_client
from users.models import Client, STATUS_USER_BAN, STATUS_DEVICE_BANNED, STATUS_NOT_HAVE_IN_DB, STATUS_RETRY_USER, \
    STATUS_VIRTUAL_DEVICE


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ['domen', 'packege_id', 'usser_id', 'getz_user', 'getr_user', 'utm_medium', ]

    @transaction.atomic
    def create(self, validated_data):
        # ip
        if 'HTTP_X_FORWARDED_FOR' in self.context.get('request').META:
            ip_adds = self.context.get('request').META['HTTP_X_FORWARDED_FOR'].split(",")
            ip = ip_adds[0]
            validated_data['ip'] = ip
        else:
            ip = self.context.get('request').META['REMOTE_ADDR']
            validated_data['ip'] = ip
        if not ip:
            validated_data['detail_status'] = 'Не удалось извлечь IP '
        # ip = '80.90.237.83'
        # validated_data['ip'] = ip
        # country
        location = get_location_data(ip)
        country_code_from_header = location['country_code']
        country = Country.objects.get(name=country_code_from_header)
        validated_data['country'] = country
        # timezone from headers
        timezone_from_header = location['timezone']
        validated_data['timezone_from_header'] = timezone_from_header
        # getz_user
        getz_user = validated_data.get('getz_user')
        # headers / user_agent
        user_agent = self.context.get('request').META.get("HTTP_USER_AGENT")
        validated_data['user_agent'] = user_agent
        # usser_id
        usser_id = validated_data.get('usser_id')
        # domen
        domen = validated_data.get('domen')
        # detail_status
        validated_data['detail_status'] = ''

        check_data = get_check_data()
        validated_data['detail_status'] += str(check_data)
        # print(check_data)
        # company
        try:
            # Если есть компания с доменом - добавляем логу компанию
            company = Company.objects.get(domen=domen)
        except Company.DoesNotExist:
            # Если нет компании с доменом киента - ставим пропуск
            company = None
            validated_data['detail_status'] += ' Не удалось извлечь IP /'
        validated_data['company'] = company
        # filters
        if company:
            if company.active_filter_one_time_zone:
                # Если фильтр 1 включен
                validated_data['filter_one_time_zone'] = STATUS_FILTER_NOT_STARTED
            else:
                validated_data['filter_one_time_zone'] = STATUS_FILTER_OFF
            if company.filter_two_cheker:
                # Если фильтр 2 включен
                validated_data['filter_two_cheker'] = STATUS_FILTER_NOT_STARTED
            else:
                validated_data['filter_two_cheker'] = STATUS_FILTER_OFF
        try:
            # Клиент есть в БД, проверяем статусы 'USER BAN' и 'DEVICE BANNED'
            client = Client.objects.get(usser_id=usser_id)
            validated_data['client'] = client
            if client.status == STATUS_USER_BAN:
                # Статус клиента 'USER BAN', меняем статус клиента и добавляем статус лога на 'DEVICE BANNED'
                update_status(validated_data, client, status=STATUS_USER_BAN)
                # выход
            elif client.status == STATUS_DEVICE_BANNED:
                # Статус клиента 'DEVICE BANNED', добавляем статус лога 'DEVICE BANNED'
                update_status(validated_data, client, status=STATUS_DEVICE_BANNED)
                # выход
            else:
                # У клиента нет статусов 'USER BAN' и 'DEVICE BANNED'
                # Проверка изменений
                last_log = Log.objects.filter(client=client).latest('created_at')
                if check_update_date_from_last_visit(last_log, ip, getz_user, timezone_from_header,
                                                     country_code_from_header, validated_data):
                    # Проверка не пройдена, изменяем статус клиента на 'USER BAN' и добавляем статус лога 'USER BAN'
                    update_status(validated_data, client, status=STATUS_USER_BAN)

                else:
                    # Добавляем статус 'RETRY USER' клиенту и логу
                    update_status(validated_data, client, status=STATUS_RETRY_USER)

                    # ПРОВЕРКА НА ВИРТУАЛЬНОЕ УСТРОЙСТВО ( СРАВНИВАЕМ USER-AGENT)
                    if check_update_user_agent(last_log, user_agent):
                        # изменяем статус клиента на STATUS VIRTUAL DEVICE и добавляем статус лога STATUS VIRTUAL DEVICE
                        update_status(validated_data, client, status=STATUS_VIRTUAL_DEVICE)
                    # Go to filter one
                    # Если фильтр 1 включен
                    if client.сompany.active_filter_one_time_zone:
                        country_time_zones = country.time_zones
                        country_user = country
                        сompany_countries = client.сompany.countries.all()
                        if check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries, validated_data):
                            validated_data['filter_one_time_zone'] = STATUS_SUCCESSFUL
                            # Переход на фильтр 2
                        else:
                            # TimeZone НЕ совпадает с TimeZone страны и/или страна НЕ допустима для компании,
                            # изменяем статус клиента на 'USER BAN' и добавляем статус лога STOP TIME ZONE
                            validated_data['filter_one_time_zone'] = STATUS_STOP_TIMEZONE
                    else:
                        # Если фильтр 2 отключен
                        validated_data['filter_one_time_zone'] = STATUS_FILTER_OFF
                        # Переход на фильтр 2

        except Client.DoesNotExist:
            # Клиента нет в БД
            # Создаем клиента и присваиваем клиенту и логу статус 'NOT HAVE IN DB'
            client = create_new_client(usser_id, company)
            validated_data['client'] = client
            update_status(validated_data, client, status=STATUS_NOT_HAVE_IN_DB)
            # Go to filter one
            # Если фильтр 1 включен
            if client.сompany.active_filter_one_time_zone:
                country_time_zones = country.time_zones
                country_user = country
                try:
                    сompany_countries = client.сompany.countries.all()
                    if check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries, validated_data):
                        validated_data['filter_one_time_zone'] = STATUS_SUCCESSFUL
                    else:
                        validated_data['filter_one_time_zone'] = STATUS_STOP_TIMEZONE
                except AttributeError:
                    validated_data['detail_status'] += ' У компании нет открытых стран /'
                    # У компании нет открытых стран
                    pass
            else:
                # Если фильтр 2 отключен
                validated_data['filter_one_time_zone'] = STATUS_FILTER_OFF
                # Переход на фильтр 2
        return Log.objects.create(**validated_data)
