from dataclasses import field
from rest_framework import serializers

from temps.models import ServiceEquipment, Temps


class ServiceEquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceEquipment
        fields = '__all__'

class TempListSerializer(serializers.ModelSerializer):

    time = serializers.SerializerMethodField()

    def get_time(self, instance):
        return {'hour':instance.hour, 'minute': instance.minute}

    class Meta:
        model = Temps
        fields = ('id','created_at', 'value','time')
        depth = 1
