from celery.utils.log import get_task_logger
from WatchServer import settings
from WatchServer.celery import app
from temps.utils import (
    NAME_FILE_TEMP_CPU, Scrapper, MemGrepper, SpCommand, COMMAND_MEM_RAM, NAME_FILE_TEMP,
    CommandsTypeEnum,COMMAND_TEMP_SENSORS, NAME_FILE_TEMP_CPU)
from temps.models import Temps, ServiceEquipment, RamUsage

logger = get_task_logger(__name__)

@app.task
def create_data_temps_cpu():

    sp_command_ram = SpCommand(
        command_list=COMMAND_MEM_RAM,
        tmp_file=NAME_FILE_TEMP
    )
    grepper = MemGrepper(sp_command_obj=sp_command_ram, enum_const=CommandsTypeEnum)
    mem_total, mem_used, mem_available, = grepper.grep_memory_str()

    sp_command_temp_cpu = SpCommand(
        command_list=COMMAND_TEMP_SENSORS,
        tmp_file=NAME_FILE_TEMP_CPU
    )
    scp = Scrapper(
        sp_command=sp_command_temp_cpu
    )
    core0_temp, core1_temp = scp.get_core_temps()
    all_services_equips = ServiceEquipment.objects.all()
    
    core_0 = all_services_equips.filter(code='core_0').first()
    core_1 = all_services_equips.filter(code='core_1').first()
    ram_0 = all_services_equips.filter(code='RAM_0').first()


    if core1_temp and core0_temp:

        Temps.objects.create(
            value=int(core0_temp),
            service_equipment=core_0)

        Temps.objects.create(
            value=int(core1_temp),
            service_equipment=core_1)

    if ram_0 :

        RamUsage.objects.create(
            value_used=int(mem_used),
            value_total=int(mem_total),
            value_available=int(mem_available),
            service_equipment=ram_0
        )
        

    