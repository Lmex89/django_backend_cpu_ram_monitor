from rest_framework import serializers

from temps.models import Cpuload, ServiceEquipment, Temps


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
        ram = (
            self.context.get("ram_usage")
            .filter(hour=instance.hour, minute=instance.minute)
            .first()
        )
        if ram:
            data = {
                "id": ram.get("id"),
                "value_used": ram.get("value_used"),
                "value_total": ram.get("value_total"),
                "value_available": ram.get("value_available"),
            }
            return data
        return None

    class Meta:
        model = Temps
        fields = ("temp", "ram", "time", "service_equipment", "created_at")


class CpuLoadListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cpuload
        fields = '__all__'