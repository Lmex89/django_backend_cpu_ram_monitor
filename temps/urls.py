from django.urls import include, path
from temps.views import CpuLoadViewList, ServiceEquipmentList, TempList

urlpatterns = [
    path("service_equipment_list/", ServiceEquipmentList.as_view()),
    path("temp_list/", TempList.as_view()),
    path("cpu_load/", CpuLoadViewList.as_view()),
]
