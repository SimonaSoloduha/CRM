from datetime import datetime, timezone

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist

import users
from companies.models import Company
from countries.models import Country
from logs.models import Log
from logs.tasks import get_location_data
from users.models import Client, STATUS_USER_BAN, STATUS_DEVICE_BANNED, STATUS_NOT_HAVE_IN_DB, STATUS_RETRY_USER, \
    STATUS_STOP_TIME_ZONE, STATUS_VIRTUAL_DEVICE
from account.auth_backends import User


def update_status(validated_data, client, status):
    """
    Обновление статусо
    """
    validated_data['status'] = status
    if client.status != status:
        client.status = status
        client.save(update_fields=['status'])


def create_new_client(usser_id, domen):
    """
    Создаем нового клиента с usser_id и domen из request и статусом 'NOT HAVE IN DB'
    """
    user, created = User.objects.get_or_create(
        username=usser_id,
        password=usser_id)
    try:
        # Если есть компания с доменом киента - добавляем клиенту компанию
        company = Company.objects.get(domen=domen)
    except ObjectDoesNotExist:
        # Если нет компании с доменом киента - ставим пропуск
        company = None
    client = Client.objects.create(
        user=user,
        usser_id=usser_id,
        сompany=company,
        status=STATUS_NOT_HAVE_IN_DB,
    )
    return client


def check_update_date_from_last_visit(last_log, ip, getz_user, timezone_from_header, country_code_from_header):
    """
    Проверка измененияй данных с последнего визита:

    last_visit_less_5_min - клиент заходил меньше 5-ти минут назад
    ip_changed - был изменен параметр IP адрес,
    time_zone_changed - был изменен параметр автоустановка таймзона
    country_changed - был изменен параметр Страна
    time_zone_from_header_changed - был изменен параметр таймзона

    Если хотя бы 1 параметр клиента изменился - возвращаем True

    """
    last_visit_less_5_min = False
    ip_changed = False
    time_zone_changed = False
    time_zone_from_header_changed = False
    country_changed = False
    print('****', last_log, ip, getz_user, timezone_from_header, country_code_from_header)

    now = datetime.now(timezone.utc)
    last_visit_time = last_log.created_at
    delta_time = (now - last_visit_time).total_seconds()
    print(delta_time)

    if delta_time < 5 * 60:
        print('delta_time')

        last_visit_less_5_min = True
    if last_log.ip != ip:
        print('ip_changed')

        ip_changed = True
    if last_log.getz_user != getz_user:
        print('time_zone_changed')

        time_zone_changed = True
    if last_log.getz_user != timezone_from_header:
        print('time_zone_from_header_changed')

        time_zone_from_header_changed = True
    if last_log.country.name != country_code_from_header:
        print('country_changed')

        country_changed = True
    if last_visit_less_5_min or ip_changed or time_zone_changed or time_zone_from_header_changed or \
            country_changed:
        print('Не даем')
        return True


def check_update_user_agent(last_log, user_agent):
    """
    Если user_agent клиента изменился - возвращаем True
    """
    if last_log.user_agent != user_agent:
        return True


def check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries):
    """
    Если TimeZone клиента совпадает с TimeZone страны и страна допустима для компании клиента - возвраем True
    """
    if getz_user in country_time_zones and country_user in сompany_countries:
        return True


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ['domen', 'packege_id', 'usser_id', 'getz_user', 'getr_user', 'utm_medium', ]

    def create(self, validated_data):
        # ip
        if 'HTTP_X_FORWARDED_FOR' in self.context.get('request').META:
            ip_adds = self.context.get('request').META['HTTP_X_FORWARDED_FOR'].split(",")
            ip = ip_adds[0]
            validated_data['ip'] = ip
            print('*1*')
        else:
            ip = self.context.get('request').META['REMOTE_ADDR']
            validated_data['ip'] = ip
            print('*2*')
        # ip = '80.90.237.83'
        # validated_data['ip'] = ip
        # country
        location = get_location_data(ip)
        country_code_from_header = location['country_code']
        country = Country.objects.get(name=country_code_from_header)
        validated_data['country'] = country
        # timezone from headers
        timezone_from_header = location['timezone']
        # getz_user
        getz_user = validated_data.get('getz_user')
        # headers / user_agent
        user_agent = self.context.get('request').META.get("HTTP_USER_AGENT")
        validated_data['user_agent'] = user_agent
        # usser_id
        usser_id = validated_data.get('usser_id')
        # domen
        domen = validated_data.get('domen')
        print('step 1')
        try:
            print('step 2')
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
                print('step 3')

                last_log = Log.objects.filter(client=client).latest('created_at')
                print('step 3-1', last_log)

                if check_update_date_from_last_visit(last_log, ip, getz_user, timezone_from_header,
                                                     country_code_from_header):
                    # Проверка не пройдена, изменяем статус клиента на 'USER BAN' и добавляем статус лога 'USER BAN'
                    update_status(validated_data, client, status=STATUS_USER_BAN)
                    print('step 3-2')

                else:
                    print('step 4')

                    # Добавляем статус 'RETRY USER' клиенту и логу
                    update_status(validated_data, client, status=STATUS_RETRY_USER)

                    # ПРОВЕРКА НА ВИРТУАЛЬНОЕ УСТРОЙСТВО ( СРАВНИВАЕМ USER-AGENT)
                    if check_update_user_agent(last_log, user_agent):
                        # изменяем статус клиента на STATUS VIRTUAL DEVICE и добавляем статус лога STATUS VIRTUAL DEVICE
                        update_status(validated_data, client, status=STATUS_VIRTUAL_DEVICE)
                    # Go to filter one
                    country_time_zones = country.time_zones
                    country_user = country
                    сompany_countries = client.сompany.countries.all()
                    if check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries):
                        validated_data['filter_one_time_zone'] = True
                        # Переход на фильтр 2
                        print('step 5')

                    else:
                        # TimeZone НЕ совпадает с TimeZone страны и/или страна НЕ допустима для компании,
                        # изменяем статус клиента на 'USER BAN' и добавляем статус лога STOP TIME ZONE
                        validated_data['filter_one_time_zone'] = False
                        update_status(validated_data, client, status=STATUS_STOP_TIME_ZONE)
                        print('step 6')
            print('step 3-3')

        except users.models.Client.DoesNotExist:
            print('step 7')

            # Клиента нет в БД
            # Создаем клиента и присваиваем клиенту и логу статус 'NOT HAVE IN DB'
            client = create_new_client(usser_id, domen)
            validated_data['client'] = client
            update_status(validated_data, client, status=STATUS_NOT_HAVE_IN_DB)
            # Go to filter one
            country_time_zones = country.time_zones
            country_user = country
            try:
                сompany_countries = client.сompany.countries.all()
                if check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries):
                    validated_data['filter_one_time_zone'] = True
            except AttributeError:
                # Нет компании в БД
                pass
        print('step 8')

        return Log.objects.create(**validated_data)
