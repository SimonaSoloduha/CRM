from django.db import transaction
from rest_framework import serializers

from logs.models import Log, STATUS_SUCCESSFUL
from logs.tasks import get_location_data
from logs.utils import check_update_date_from_last_visit, check_update_user_agent, \
    check_filter_one_time_zone, create_new_client, check_filter_two_cheker_off, check_users_status_ban_and_divice_ban, \
    get_detail_status, get_url, get_ip, get_country_code_from_header, get_country, get_timezone_from_headers, \
    get_getz_user, get_user_agent, get_usser_id, get_domen, get_company, get_filters_status
from users.models import Client


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['domen', 'packege_id', 'usser_id', 'getz_user', 'getr_user', 'utm_medium', 'url', 'filter_two_cheker']

    @transaction.atomic
    def update(self, instance, validated_data):
        instance.filter_two_cheker = validated_data.get('filter_two_cheker')
        if instance.filter_two_cheker == STATUS_SUCCESSFUL:
            instance.final = True
        instance.save()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        # detail_status
        get_detail_status(validated_data)
        # url
        get_url(validated_data)
        # ip
        context = self.context
        ip = get_ip(context, validated_data)
        # location
        location = get_location_data(ip)
        # country_code_from_header
        country_code_from_header = get_country_code_from_header(location)
        # country
        country = get_country(country_code_from_header, validated_data)
        # timezone from headers
        timezone_from_header = get_timezone_from_headers(location, validated_data)
        # getz_user
        getz_user = get_getz_user(validated_data)
        # headers / user_agent
        user_agent = get_user_agent(context, validated_data)
        # usser_id
        usser_id = get_usser_id(validated_data)
        # domen
        domen = get_domen(validated_data)
        # company
        company = get_company(domen, validated_data)
        # filters
        get_filters_status(company, validated_data)
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
                            if check_filter_two_cheker_off(client, validated_data):
                                # фильтр 2 отключен
                                validated_data['final'] = True

        except Client.DoesNotExist:
            # Клиента нет в БД
            client = create_new_client(usser_id, company, validated_data)
            # Go to filter 1
            if check_filter_one_time_zone(client, country, getz_user, validated_data):
                # Go to filter 2
                if check_filter_two_cheker_off(client, validated_data):
                    # фильтр 2 отключен
                    validated_data['final'] = True

        return Log.objects.create(**validated_data)
