from rest_framework import serializers

from temps.models import Cpuload, RamUsage, ServiceEquipment, Temps


class ServiceEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceEquipment
        fields = "__all__"


class TempListSerializer(serializers.ModelSerializer):

    time = serializers.SerializerMethodField()
    temp = serializers.SerializerMethodField()
    ram = serializers.SerializerMethodField()

    def get_time(self, instance):
        return {"hour": instance.hour, "minute": instance.minute}

    def get_temp(self, instance):

        return {
            "id": instance.id,
            "value": instance.value,
        }

    def get_ram(self, instance):
        ram = self.context.get("ram_usage")
        if not ram:
            return None
        ram = ram.filter(hour=instance.hour, minute=instance.minute).first()
        data = {
            "id": ram.get("id"),
            "value_used": ram.get("value_used"),
            "value_total": ram.get("value_total"),
            "value_available": ram.get("value_available"),
        }
        return data

    class Meta:
        model = Temps
        fields = ("temp", "ram", "time", "service_equipment", "created_at")


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
