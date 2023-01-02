from datetime import datetime, timezone

from rest_framework import serializers

from companies.models import Company
from countries.models import Country
from logs.models import Log, STATUS_STOP_TIMEZONE, STATUS_SUCCESSFUL
from logs.tasks import get_location_data
from users.models import Client, STATUS_USER_BAN, STATUS_DEVICE_BANNED, STATUS_NOT_HAVE_IN_DB, STATUS_RETRY_USER, \
    STATUS_VIRTUAL_DEVICE
from account.auth_backends import User


def update_status(validated_data, client, status):
    """
    Обновление статусо
    """

    validated_data['status'] = status
    if client.status != status:
        client.status = status
        client.save(update_fields=['status'])


def create_new_client(usser_id, company):
    """
    Создаем нового клиента с usser_id и domen из request и статусом 'NOT HAVE IN DB'
    """
    user, created = User.objects.get_or_create(
        username=usser_id,
        password=usser_id)
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

    now = datetime.now(timezone.utc)
    last_visit_time = last_log.created_at
    delta_time = (now - last_visit_time).total_seconds()
    if delta_time < 5 * 60:
        last_visit_less_5_min = True
    if last_log.ip != ip:
        ip_changed = True
    if last_log.getz_user != getz_user:
        time_zone_changed = True
    if last_log.getz_user != timezone_from_header:
        time_zone_from_header_changed = True
    if last_log.country.name != country_code_from_header:
        country_changed = True
    if last_visit_less_5_min or ip_changed or time_zone_changed or time_zone_from_header_changed or \
            country_changed:
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
        else:
            ip = self.context.get('request').META['REMOTE_ADDR']
            validated_data['ip'] = ip
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
        # company
        try:
            # Если есть компания с доменом - добавляем логу компанию
            company = Company.objects.get(domen=domen)
        except Company.DoesNotExist:
            # Если нет компании с доменом киента - ставим пропуск
            company = None
        validated_data['company'] = company

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
                                                     country_code_from_header):
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
                    country_time_zones = country.time_zones
                    country_user = country
                    сompany_countries = client.сompany.countries.all()
                    if check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries):
                        validated_data['filter_one_time_zone'] = STATUS_SUCCESSFUL
                        # Переход на фильтр 2
                    else:
                        # TimeZone НЕ совпадает с TimeZone страны и/или страна НЕ допустима для компании,
                        # изменяем статус клиента на 'USER BAN' и добавляем статус лога STOP TIME ZONE
                        validated_data['filter_one_time_zone'] = STATUS_STOP_TIMEZONE

        except Client.DoesNotExist:

            # Клиента нет в БД
            # Создаем клиента и присваиваем клиенту и логу статус 'NOT HAVE IN DB'
            client = create_new_client(usser_id, company)
            validated_data['client'] = client
            update_status(validated_data, client, status=STATUS_NOT_HAVE_IN_DB)
            # Go to filter one
            country_time_zones = country.time_zones
            country_user = country
            try:
                сompany_countries = client.сompany.countries.all()
                if check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries):
                    validated_data['filter_one_time_zone'] = STATUS_SUCCESSFUL
            except AttributeError:
                # У компании нет открытых стран
                pass

        return Log.objects.create(**validated_data)
