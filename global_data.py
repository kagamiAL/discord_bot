import discord
from datetime import datetime

guild_ids = [discord.Object(id=916706804652732416)];
__server_data   = {};

class ServerDataObject:
    
    server_id: str;
    
    __loop_muted = {};
    
    def set_loop_muted(self, member, is_muted: bool):
        if (is_muted):
            self.__loop_muted[member.id] = {
                    'currently_muted': False,
                    'roles': member.roles[1:],
                    'time_remaining': 0,
                };
            return self.__loop_muted[member.id];
        del self.__loop_muted[member.id];
    
    def is_loop_muted(self, member, table_data=None) -> bool:
        if (member.id in self.__loop_muted):
            if (table_data and table_data != self.__loop_muted[member.id]):
                return False;
            return True
        return False
    
    def set_time_remaining(self, member, time_remaining) -> int:
        if (member.id in self.__loop_muted):
            self.__loop_muted[member.id]['time_remaining'] = time_remaining;
            return time_remaining;
    
    def get_time_remaining(self, member) -> int:
        if (member.id in self.__loop_muted):
            return self.__loop_muted[member.id]['time_remaining'];  
    
    def is_currently_muted(self, member) -> bool:
        if (member.id in self.__loop_muted):
            return self.__loop_muted[member.id]['currently_muted'];
    
    def set_currently_muted(self, member, is_muted: bool):
        if (member.id in self.__loop_muted):
            self.__loop_muted[member.id]['currently_muted'] = is_muted;
    
    def __init__(self, server_id: str):
        self.server_id = server_id;
        return;
    
def get_server_data(server_id):
    global __server_data;
    if (not server_id in __server_data):
        __server_data[server_id] = ServerDataObject(server_id);
    return __server_data[server_id];

def get_current_date_time() -> str:
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ': ';

def print_report(message: str):
    print(get_current_date_time() + message);
    return;