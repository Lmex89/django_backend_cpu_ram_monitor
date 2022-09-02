from datetime import datetime, timedelta
from multiprocessing import context
from rest_framework import generics
from temps.models import Cpuload, RamUsage, Temps, ServiceEquipment
from temps.serializers import (
    CpuLoadListSerializer,
    ServiceEquipmentSerializer,
    TempListSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
from django.db.models.functions import (
    ExtractHour,
    ExtractMinute,
)


class TempList(generics.ListAPIView):
    queryset = Temps.objects.all()
    serializer_class = TempListSerializer
    _ram_usage_query = None

    @property
    def ram_usage_query(self):
        ram_0 = ServiceEquipment.objects.filter(code="RAM_0").first()
        if self._ram_usage_query:
            return self._ram_usage_query
        queryset = RamUsage.objects.filter(service_equipment=ram_0)
        return queryset.annotate(
            hour=ExtractHour("created_at"), minute=ExtractMinute("created_at")
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
            .order_by("-created_at")
        )

    def list(self, request, *args, **kwargs):
        today = today = datetime.now().date()
        view, date, code, hour = self.filters()

        if view == "code" and not date:
            query = (
                self.get_queryset()
                .filter(service_equipment__code=code)
                .filter(created_at__gte=today, created_at__lt=today + timedelta(days=1))
            )
            if hour is None:
                hour = query.first().hour if query.exists() else None
            query = query.filter(hour=hour)
            ram_query = self.ram_usage_query.filter(hour=hour).values(
                "id",
                "value_used",
                "value_total",
                "value_available",
                "hour",
                "minute",
            )
        elif view == "code" and date:
            date_time_obj = datetime.strptime(date, "%Y-%m-%d")
            query = (
                self.get_queryset()
                .filter(
                    service_equipment__code=code,
                    created_at__range=[
                        date_time_obj,
                        date_time_obj + timedelta(days=1),
                    ],
                )
                .order_by()
                .distinct("minute")
            )
            ram_query = self.ram_usage_query.filter(
                created_at__range=[date_time_obj, date_time_obj + timedelta(days=1)]
            ).values(
                "id",
                "value_used",
                "value_total",
                "value_available",
                "hour",
                "minute",
            )

        serializer = self.get_serializer(
            query, many=True, context={"ram_usage": ram_query}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def filters(self):
        view = self.request.query_params.get("view")
        date = self.request.query_params.get("date")
        code = self.request.query_params.get("code")
        hour = self.request.query_params.get("hour")
        return view, date, code, hour


class ServiceEquipmentList(generics.ListAPIView):

    queryset = ServiceEquipment.objects.all()
    serializer_class = ServiceEquipmentSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class CpuLoadViewList(generics.ListAPIView):
    queryset = Cpuload.objects.all()
    serializer_class = CpuLoadListSerializer

    def get_queryset(self):
        today = today = datetime.now().date()
        code = self.request.query_params.get("code")
        filters = Q()
        queryset = super().get_queryset().annotate(
                    hour=ExtractHour("created_at"), minute=ExtractMinute("created_at")
                ).order_by("-created_at").filter(
                    created_at__range=[today, today + timedelta(days=1)]
                ).select_related('service_equipment')
        hour = queryset.first().hour if queryset.exists() else None

        if hour :
            filters &= Q(hour=hour)
        if code :
            filters &= Q(service_equipment__code=code)

        return queryset.filter(filters)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

        

