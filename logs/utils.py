from django.utils import timezone

from account.auth_backends import User
from users.models import Client, STATUS_NOT_HAVE_IN_DB


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


def check_update_date_from_last_visit(last_log, ip, getz_user, timezone_from_header, country_code_from_header, validated_data):
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

    now = timezone.now()
    last_visit_time = last_log.created_at
    delta_time = (now - last_visit_time).total_seconds()
    if delta_time < 5 * 60:
        last_visit_less_5_min = True
        validated_data['detail_status'] += ' Заходил меньше 5 минут назад /'
    if last_log.ip != ip:
        ip_changed = True
        validated_data['detail_status'] += ' Изменен IP /'
    if last_log.getz_user != getz_user:
        time_zone_changed = True
        validated_data['detail_status'] += ' Изменена getz_user /'
    if last_log.getz_user != timezone_from_header:
        if timezone_from_header == 'Europe/Kyiv' and last_log.getz_user == 'Europe/Kiev':
            return False
        else:
            time_zone_from_header_changed = True
            validated_data['detail_status'] += f' Не совпадает time_zone_from_header {timezone_from_header} с getz_user {last_log.getz_user} /'
    if last_log.country.name != country_code_from_header:
        country_changed = True
        validated_data['detail_status'] += ' Изменен country_code_from_header /'
    if last_visit_less_5_min or ip_changed or time_zone_changed or time_zone_from_header_changed or \
            country_changed:
        return True


def check_update_user_agent(last_log, user_agent):
    """
    Если user_agent клиента изменился - возвращаем True
    """
    if last_log.user_agent != user_agent:
        return True


def check_filter_one_time_zone(getz_user, country_time_zones, country_user, сompany_countries, validated_data):
    """
    Если TimeZone клиента совпадает с TimeZone страны и страна допустима для компании клиента - возвраем True
    """
    if getz_user in country_time_zones:
        if country_user in сompany_countries:
            return True
        else:
            validated_data['detail_status'] += ' Страны пользователя нет в странах компании /'
    else:
        validated_data['detail_status'] += ' getz_user пользователя нет в таймзонах страны /'
