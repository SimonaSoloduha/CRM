from datetime import datetime, timezone

from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist


from companies.models import Company
from logs.models import Log
from users.models import Client, STATUS_USER_BAN, STATUS_DEVICE_BANNED, STATUS_NOT_HAVE_IN_DB
from account.auth_backends import User

BLOCK_STATUSES = ['NOT HAVE IN DB', 'USER BAN', 'DEVICE BANNED']


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ['domen', 'packege_id', 'usser_id', 'getz_user', 'getr_user', 'utm_medium', ]

    def create(self, validated_data):
        validated_data['user_agent'] = self.context.get('request').META.get("HTTP_USER_AGENT")
        validated_data['ip'] = self.context.get('request').META.get("REMOTE_ADDR")
        ip_client = self.context.get('request').META.get('X-Real-IP')
        # {'domen': 'domen.com', 'packege_id': 'packageName', 'usser_id': 'XXXXXXXXXXXX', 'getz_user': 'timeZone',
        #  'getr_user': 'utm_source=google-play', 'utm_medium': 'organic',
        #  'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        #  'ip': '127.0.0.1'}
        usser_id = validated_data.get('usser_id')
        domen = validated_data.get('domen')
        getz_user = validated_data.get('getz_user')
        try:
            client = Client.objects.get(usser_id=usser_id)
            validated_data['client'] = client
            print('Старенький')
            if client.status == STATUS_USER_BAN:
                print('STATUS_USER_BAN')
                validated_data['status'] = STATUS_DEVICE_BANNED
                client.status = STATUS_DEVICE_BANNED
                client.save(update_fields=['status'])
                # выход
            elif client.status == STATUS_DEVICE_BANNED:
                print('STATUS_DEVICE_BANNED')
                validated_data['status'] = STATUS_DEVICE_BANNED + '403'
                # выход
            else:
                last_log = Log.objects.filter(client=client).latest('created_at')
                print('*** last_log', last_log, last_log.id, last_log.created_at)
                last_visit_less_5_min = False
                ip_changed = False
                time_zone_changed = False
                country_changed = False

                now = datetime.now(timezone.utc)
                delta_time = (now - last_log.created_at).total_seconds()
                print(delta_time)
                # if delta_time < 60 * 5:
                if delta_time < 5:
                    print(' last_visit_less_5_min DONE ')
                    last_visit_less_5_min = True
                if last_log.ip != validated_data['ip']:
                    print(' last_log DONE ')
                    ip_changed = True
                if last_log.getz_user != getz_user:
                    print(' time_zone_changed DONE ')
                    time_zone_changed = True
                # if last_log.county != validated_data['getz_user']:
                if last_log.getz_user != validated_data['getz_user']:
                    print(' country_changed DONE ')
                    #TODO УТОЧНИТЬ ПО СТРАНЕ
                    country_changed = True

                if last_visit_less_5_min or ip_changed or time_zone_changed or country_changed:
                    validated_data['status'] = STATUS_USER_BAN + '403'
                else:
                    # Проверка: TimeZone совпадает с TimeZone стран компании
                    company_countries = client.сompany.countries.values_list('time_zones', flat=True).distinct()
                    # print(client.сompany.domen)
                    # print(getz_user)
                    for country in company_countries:
                        if getz_user in country:
                            # validated_data['country'] = country
                            print('Е С Т Ь', country, getz_user, type(country))

        except ObjectDoesNotExist:
            print('Новенький')
            user = User.objects.get_or_create(
                username=usser_id,
                password=usser_id)
            try:
                company = Company.objects.get(domen=domen)
            except ObjectDoesNotExist:
                company = None
            client = Client.objects.create(
                user=user,
                usser_id=usser_id,
                сompany=company,
                status=STATUS_NOT_HAVE_IN_DB,
            )
            validated_data['client'] = client
            validated_data['status'] = STATUS_NOT_HAVE_IN_DB
            # GO TO FILTER 1

        # try:
        #     client = Client.objects.get(usser_id=usser_id)
        #     print('C L I E N T ', client)
        #     if client.status == STATUS_USER_BAN:
        #         print('STATUS_USER_BAN')
        #
        #         validated_data['status'] = STATUS_DEVICE_BANNED
        #         client.status = STATUS_DEVICE_BANNED
        #         client.save(update_fields=['status'])
        #     elif client.status == STATUS_DEVICE_BANNED:
        #         print('STATUS_DEVICE_BANNED')
        #
        #         validated_data['status'] = STATUS_DEVICE_BANNED + '403'
        #     else:
        #         print('GET LOG')
        #         try:
        #             last_log = Log.objects.filter(usser_id=usser_id).latest('created_at')
        #             print('*** last_log', last_log, last_log.id, last_log.created_at)
        #
        #         except ObjectDoesNotExist:
        #             print('Н Е Т    Л О Г А ')
        #         # RESPONSE
        #     print('status', client.status)
        # except ObjectDoesNotExist:
        #     print('Нет такого')
        #     user = User.objects.get_or_create(
        #         username=usser_id,
        #         password=usser_id)
        #     try:
        #         company = Company.objects.get(domen=domen)
        #     except ObjectDoesNotExist:
        #         company = None
        #     Client.objects.create(
        #         user=user,
        #         usser_id=usser_id,
        #         сompany=company,
        #         status=STATUS_NOT_HAVE_IN_DB,
        #     )
        #     validated_data['status'] = STATUS_NOT_HAVE_IN_DB

        return Log.objects.create(**validated_data)

# DOMEN.COM/?
# packageid=packageName&
# usserid=XXXXXXXXXXXX&
# getz=timeZone&
# getr=utm_source=google-play& (???)
# utm_medium=organic
# user_agent