from rest_framework import serializers
from temps.models import Cpuload, RamUsage, Server, ServiceEquipment, Temps


class ServiceEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEquipment
        fields = (
            "code",
            "id",
        )


class TempListSerializer(serializers.ModelSerializer):

    time = serializers.SerializerMethodField()

    def get_time(self, instance):
        return {"hour": instance.hour, "minute": instance.minute}

    class Meta:
        model = Temps
        fields = ("id", "value", "time", "service_equipment")


class RamUsageSerializer(serializers.ModelSerializer):

    time = serializers.SerializerMethodField()

    def get_time(self, instance):
        return {"hour": instance.hour, "minute": instance.minute}

    class Meta:
        model = RamUsage
        fields = ("id", "value_used", "value_total", "value_available", "time", "service_equipment")


class ServerSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    alias = serializers.SerializerMethodField()
    temps = serializers.SerializerMethodField()
    ram = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.id

    def get_alias(self, instance):
        return instance.alias 
        
    def get_ram(self, instance):
        equipment = instance.service_x
        temp = [eq for eq in equipment if "RAM" in eq.code]
        temps = temp[0].ram_x
        return RamUsageSerializer(temps, many=True).data

    def get_temps(self, instance):
        equipment = instance.service_x
        temp = [eq for eq in equipment if "core" in eq.code]
        temps = temp[0].temps_x
        return TempListSerializer(temps, many=True).data

    class Meta:
        model = Server
        fields = ("id", "temps", "ram","alias")


class CpuLoadListSerializer(serializers.ModelSerializer):

    time = serializers.SerializerMethodField()
    core_code = serializers.SerializerMethodField()

    def get_time(self, instance):
        return {"hour": instance.hour, "minute": instance.minute}

    def get_core_code(self, instance):
        return instance.service_equipment.code

    class Meta:
        model = Cpuload
        fields = ("id", "created_at", "value", "service_equipment", "core_code", "time")
