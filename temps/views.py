from datetime import datetime, timedelta, date
from rest_framework import generics
from temps.models import Cpuload, RamUsage, Server, Temps, ServiceEquipment
from temps.serializers import (
    CpuLoadListSerializer,
    ServerSerializer,
    ServiceEquipmentSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q, Prefetch
from django.db.models.functions import (
    ExtractHour,
    ExtractMinute,
)

from temps.utils import send_email_alert
import threading
import time

ALIAS_SERVER = "laptop_lmex89"

class HealtCheckAPIView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        return Response(data=dict(status="ok"), status=status.HTTP_200_OK)


class SendEmailView(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        args_ = "brigadagubernamental394@gmail.com"
        for i in range(0, 100):
            t1 = threading.Thread(target=send_email_alert, args=(args_,))
            t1.start()
            time.sleep(1)
            print(t1)
        return Response(data=dict(), status=status.HTTP_200_OK)


class TempList(generics.ListAPIView):
    queryset = Temps.objects.all()
    serializer_class = ServerSerializer
    _ram_usage_query = None

    def server(self, list_code: list, date_input: date, hour_input: int):
        ram = "RAM_0"
        list_code.append(ram)
        query_temp = (
            self.get_queryset()
            .filter(
                created_at__gte=date_input,
                created_at__lt=date_input + timedelta(days=1),
            )
            .filter(hour=hour_input)
        )
        query_ram = self.ram_usage_query.filter(
            created_at__gte=date_input,
            created_at__lt=date_input + timedelta(days=1),
        ).filter(hour=hour_input)

        server = Server.objects.filter(alias=ALIAS_SERVER)
        server = server.prefetch_related(
            Prefetch(
                "service_equipment_server",
                queryset=ServiceEquipment.objects.filter(
                    Q(code__in=list_code)
                ).prefetch_related(
                    Prefetch(
                        "service_equipment_temp", queryset=query_temp, to_attr="temps_x"
                    ),
                    Prefetch(
                        "service_equipment_ram",
                        queryset=query_ram,
                        to_attr="ram_x",
                    ),
                ),
                to_attr="service_x",
            )
        )
        return server.first()

    @property
    def ram_usage_query(self):

        ram_0 = ServiceEquipment.objects.filter(code="RAM_0").first()
        if self._ram_usage_query:
            return self._ram_usage_query
        queryset = RamUsage.objects.filter(service_equipment=ram_0)
        return (
            queryset.annotate(
                hour=ExtractHour("created_at"), minute=ExtractMinute("created_at")
            )
            .select_related("service_equipment")
            .order_by("created_at")
        )

    def get_queryset(self):
        core_0 = ServiceEquipment.objects.filter(code="core_0").first()
        core_1 = ServiceEquipment.objects.filter(code="core_1").first()
        return (
            super()
            .get_queryset()
            .filter(Q(service_equipment=core_0) | Q(service_equipment=core_1))
            .annotate(
                hour=ExtractHour("created_at"), minute=ExtractMinute("created_at")
            )
            .select_related("service_equipment")
            .order_by("created_at")
        )

    def filters(self):
        view = self.request.query_params.get("view")
        date = self.request.query_params.get("date")
        code = self.request.query_params.get("code")
        hour = self.request.query_params.get("hour")
        return view, date, code, hour

    def list(self, request, *args, **kwargs):
        today = datetime.now().date()
        view, date, code, hour = self.filters()
        query = self.get_queryset()
        ram_query = self.ram_usage_query

        if view is None:
            return Response(
                dict(error="Error neceista el param view=code to reponse"),
                status=status.HTTP_404_NOT_FOUND,
            )
        if hour is None:
            hour = query.last().hour if query.exists() else None

        if not date:
            today = datetime.now().date()
            queryset = self.server(list_code=[code], date_input=today, hour_input=hour)

        else:
            date_time_obj = datetime.strptime(date, "%Y-%m-%d")
            queryset = self.server(
                list_code=[code], date_input=date_time_obj, hour_input=hour
            )

        serializer = self.get_serializer(
            queryset,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceEquipmentList(generics.ListAPIView):

    queryset = ServiceEquipment.objects.all()
    serializer_class = ServiceEquipmentSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CpuLoadViewList(generics.ListAPIView):
    queryset = Cpuload.objects.all()
    serializer_class = CpuLoadListSerializer

    def filters(self):
        date = self.request.query_params.get("date")
        code = self.request.query_params.get("code")
        hour_input = self.request.query_params.get("hour")
        return date, code, hour_input

    def get_queryset(self):
        date_input, code, hour_input = self.filters()
        date_input = (
            datetime.now().date()
            if date_input is None
            else datetime.strptime(date_input, "%Y-%m-%d")
        )
        code = self.request.query_params.get("code")
        filters = Q()
        queryset = (
            super()
            .get_queryset()
            .annotate(
                hour=ExtractHour("created_at"), minute=ExtractMinute("created_at")
            )
            .filter(created_at__range=[date_input, date_input + timedelta(days=1)])
            .select_related("service_equipment")
            .order_by("created_at")
        )

        hour = queryset.last().hour if hour_input is None else hour_input

        if hour:
            filters &= Q(hour=hour)
        if code:
            filters &= Q(service_equipment__code=code)

        return queryset.filter(filters)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
