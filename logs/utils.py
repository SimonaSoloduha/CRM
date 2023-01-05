from django.utils import timezone

from account.auth_backends import User

from logs.models import STATUS_SUCCESSFUL, STATUS_FILTER_OFF, STATUS_STOP_TIMEZONE, STATUS_STOP_MCHECKER
from logs.tasks import get_check_data
from users.models import Client, STATUS_NOT_HAVE_IN_DB, STATUS_USER_BAN, STATUS_DEVICE_BANNED, STATUS_RETRY_USER, \
    STATUS_VIRTUAL_DEVICE


def update_status(validated_data, client, status):
    """
    Обновление статусо
    """
    validated_data['status'] = status
    if client.status != status:
        client.status = status
        client.save(update_fields=['status'])


def create_new_client(usser_id, company, validated_data):
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
    update_status(validated_data, client, status=STATUS_NOT_HAVE_IN_DB)
    validated_data['client'] = client
    return client


def check_users_status_ban_and_divice_ban(client, validated_data):
    """
    Проверка статусов 'USER BAN' и 'DEVICE BANNED', если есть один из этих статусов - возвращаем False
    """
    if client.status == STATUS_USER_BAN:
        # Статус клиента 'USER BAN', меняем статус клиента и добавляем статус лога на 'DEVICE BANNED'
        update_status(validated_data, client, status=STATUS_USER_BAN)
        return False
    elif client.status == STATUS_DEVICE_BANNED:
        # Статус клиента 'DEVICE BANNED', добавляем статус лога 'DEVICE BANNED'
        update_status(validated_data, client, status=STATUS_DEVICE_BANNED)
        return False
    return True


def check_update_date_from_last_visit(client, last_log, ip, getz_user, timezone_from_header, country_code_from_header,
                                      validated_data):
    """
    Проверка измененияй данных с последнего визита:

    last_visit_less_5_min - клиент заходил меньше 5-ти минут назад
    ip_changed - был изменен параметр IP адрес,
    time_zone_changed - был изменен параметр автоустановка таймзона
    country_changed - был изменен параметр Страна
    time_zone_from_header_changed - был изменен параметр таймзона

    Если хотя бы 1 параметр клиента изменился - возвращаем True

    """
    now = timezone.now()
    last_visit_time = last_log.created_at
    delta_time = (now - last_visit_time).total_seconds()
    if delta_time < 5 * 60:
        update_status(validated_data, client, status=STATUS_USER_BAN)
        validated_data['detail_status'] += ' Заходил меньше 5 минут назад /'
        return False
    if last_log.ip != ip:
        update_status(validated_data, client, status=STATUS_USER_BAN)
        validated_data['detail_status'] += ' Изменен IP /'
        return False
    if last_log.getz_user != getz_user:
        update_status(validated_data, client, status=STATUS_USER_BAN)
        validated_data['detail_status'] += ' Изменена getz_user /'
        return False
    if last_log.getz_user != timezone_from_header:
        if timezone_from_header == 'Europe/Kyiv' and last_log.getz_user == 'Europe/Kiev':
            pass
        else:
            update_status(validated_data, client, status=STATUS_USER_BAN)
            validated_data[
                'detail_status'] += f' Не совпадает time_zone_from_header {timezone_from_header} с getz_user {last_log.getz_user} /'
            return False
    if last_log.country.name != country_code_from_header:
        update_status(validated_data, client, status=STATUS_USER_BAN)
        validated_data['detail_status'] += ' Изменен country_code_from_header /'
        return False
    update_status(validated_data, client, status=STATUS_RETRY_USER)
    return True


def check_update_user_agent(client, last_log, user_agent, validated_data):
    """
    Если user_agent клиента изменился - возвращаем False
    """
    if last_log.user_agent != user_agent:
        update_status(validated_data, client, status=STATUS_VIRTUAL_DEVICE)
        return False
    return True


def check_filter_one_time_zone(client, country, getz_user, validated_data):
    """
    Если TimeZone клиента совпадает с TimeZone страны и страна допустима для компании клиента - возвраем True
    """
    # Если фильтр 1 включен
    if client.сompany.active_filter_one_time_zone:
        country_time_zones = country.time_zones
        country_user = country
        try:
            сompany_countries = client.сompany.countries.all()
            if getz_user in country_time_zones:
                if country_user in сompany_countries:
                    validated_data['filter_one_time_zone'] = STATUS_SUCCESSFUL
                    # проверка пройдена
                    return True
                else:
                    # Страны пользователя нет в странах компании
                    validated_data['filter_one_time_zone'] = STATUS_STOP_TIMEZONE
                    validated_data['detail_status'] += ' Страны пользователя нет в странах компании /'
                    return False
            else:
                # getz_user пользователя нет в таймзонах страны
                validated_data['filter_one_time_zone'] = STATUS_STOP_TIMEZONE
                validated_data['detail_status'] += ' getz_user пользователя нет в таймзонах страны /'
                return False
        except AttributeError:
            # У компании нет открытых стран
            validated_data['detail_status'] += ' У компании нет открытых стран /'
            validated_data['filter_one_time_zone'] = STATUS_STOP_TIMEZONE
            return False
    else:
        # Если фильтр 1 отключен
        validated_data['filter_one_time_zone'] = STATUS_FILTER_OFF
        return True


def check_filter_two_cheker(url, user_agent, client, validated_data):
    """
    Проверка клиента по MagicChecker
    """
    if client.сompany.filter_two_cheker:
        # Фильтр 2 включен
        check_data = get_check_data(url, user_agent)
        if check_data:
            # фильтр 2 пройден
            validated_data['filter_two_cheker'] = STATUS_SUCCESSFUL
            return True
        else:
            # фильтр 2 не пройден
            validated_data['filter_two_cheker'] = STATUS_STOP_MCHECKER
            return False
    else:
        # Фильтр 2 отключен
        validated_data['filter_two_cheker'] = STATUS_FILTER_OFF
        return True
