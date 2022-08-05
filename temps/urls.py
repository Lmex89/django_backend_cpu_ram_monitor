from django.urls import include, path
from temps.views import ServiceEquipmentList, TempList

urlpatterns = [
     path('service_equipment_list/',
         ServiceEquipmentList.as_view()),
    path('temp_list/',TempList.as_view()),
]