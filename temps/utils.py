from __future__ import annotations
from codeop import CommandCompiler
import subprocess as sp
import re
from typing import Tuple, List
from enum import Enum

COMMAND_MEM_RAM = ['free', '-m'] 
NAME_FILE_TEMP = "tmp.txt"
COMMAND_TEMP_SENSORS = ['sensors']
NAME_FILE_TEMP_CPU = "tmp_cpu.txt"

class CommandsTypeEnum(Enum):
    USED = 'used'
    TOTAL = 'total'
    AVAILABLE = 'available'

class SpCommand:

    def __init__(self, command_list:List[str],tmp_file:str) ->None:
        self.command_list = command_list
        self.tmp_file = tmp_file
        self.file_lines = self.call_command()

    def call_command(self,) -> List[str]:
        file = open(self.tmp_file, 'w')
        sp.call(self.command_list,stdout=file)
        file = open(self.tmp_file, 'r')
        lines = file.readlines()
        file.close
        return lines
 

class Scrapper:

    def __init__(self, sp_command:SpCommand) -> None:

        self.core_0 = None
        self.core_1 = None
        self.sp_command = sp_command

    def get_core_temps(self) -> Tuple[str,str]:
        core_0 = re.findall('Core 0:\s*\+\d{2,4}',''.join(self.sp_command.file_lines))
        core_1 = re.findall('Core 1:\s*\+\d{2,4}',''.join(self.sp_command.file_lines))
        
        if core_0 and len(core_0[0])> 2:
            self.core_0 = core_0[0][-2:]
        if core_1 and len(core_1[0]) > 2:
            self.core_1 = core_1[0][-2:]
        
        return self.core_0, self.core_1


class MemGrepper:
    
    def __init__(self, sp_command_obj:SpCommand, enum_const:CommandsTypeEnum) -> None:
        self.enum_const = enum_const
        self.sp_command = sp_command_obj
        self.memory = self.grep_memory_str()
        

    def get_index(self, string:str, list_lines : List[str]) -> int:
        return list_lines.index(string)

    def split_lines_list(self, lines):
        lines = [line.split() for line in lines ]
        return lines

    def grep_memory_str(self) -> Tuple:

        lines = self.sp_command.file_lines
        lines, index_used, index_total, index_aval = self.get_all_indexs_(lines)
        lines[1].pop(0)
        mem_used = lines[1][index_used]
        mem_total = lines[1][index_total]
        mem_available = lines[1][index_aval]
        return  mem_total, mem_used, mem_available,

    def get_all_indexs_(self, lines):
        lines = self.split_lines_list(lines) 

        index_used = self.get_index_string_in_line(lines, string_look=self.enum_const.USED.value)
        index_total = self.get_index_string_in_line(lines, string_look=self.enum_const.TOTAL.value)
        index_aval = self.get_index_string_in_line(lines, string_look=self.enum_const.AVAILABLE.value)

        return lines, index_used, index_total, index_aval 

    def get_index_string_in_line(self, lines, string_look:str):
        index_used = self.get_index(string=string_look, list_lines=lines[0])
        return index_used

