from datetime import datetime, timedelta
from rest_framework import generics
from temps.models import Temps, ServiceEquipment
from temps.serializers import ServiceEquipmentSerializer, TempListSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models.functions import (
         ExtractDay, ExtractHour, ExtractMinute,
)

class TempList(generics.ListAPIView):
    queryset = Temps.objects.all()
    serializer_class = TempListSerializer

    def get_queryset(self):
        return super().get_queryset().annotate(
            hour=ExtractHour('created_at'),
            minute=ExtractMinute('created_at')
        )

    def list(self, request, *args, **kwargs):
        today = today = datetime.now().date()
        view = self.request.query_params.get('view')
        if view == 'all': 
            return super().list(request, *args, **kwargs)
            
        elif view == 'code':
            code = self.request.query_params.get('code')
            hour = self.request.query_params.get('hour')
            query = self.get_queryset().filter(service_equipment__code=code).filter(created_at__gte=today - timedelta(days=1))
            if hour is None:
                hour = query.last().hour
                query = query.filter(hour=hour).order_by().distinct('minute')
            else :
                query = query.filter(hour=hour)
            serializer = self.get_serializer(query, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)

        return super().list(request,*args,**kwargs)


class ServiceEquipmentList(generics.ListAPIView):

    queryset = ServiceEquipment.objects.all()
    serializer_class = ServiceEquipmentSerializer

    def list(self,request, *args, **kwargs):
        return super().list(request, *args, **kwargs)