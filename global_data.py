import discord
import time
from datetime import datetime

CHARACTER_HITLIST_LIMIT = 50;

guild_ids = [discord.Object(id=916706804652732416)];
__server_data   = {};

class CoolDown:
    
    cached_time: int = 0;
    cool_down_time: int = 0;

    def is_on_cooldown(self) -> bool:
        if (time.time() - self.cached_time < self.cool_down_time):
            return True;
        return False;
    
    def get_remaining_time(self) -> int:
        return (self.cool_down_time - (time.time() - self.cached_time));
    
    def set_cooldown(self, cool_down_time: int):
        self.cached_time = time.time();
        self.cool_down_time = cool_down_time;
        return;
        
    def __init__(self, cool_down_time: int = 0):
        self.cached_time = time.time();
        self.cool_down_time = cool_down_time;
        return;

class UserData:
    
    member: discord.Member;
    
    __cool_downs = None;
    
    def is_on_cooldown(self, cool_down_name: str) -> bool:
        if (not cool_down_name in self.__cool_downs):
            return False;
        return self.__cool_downs[cool_down_name].is_on_cooldown();
    
    def set_cooldown(self, cool_down_name: str, cd_time: int):
        if (not cool_down_name in self.__cool_downs):
            self.__cool_downs[cool_down_name] = CoolDown(cd_time);
            return;
        self.__cool_downs[cool_down_name].set_cooldown(cd_time);
        return;
    
    def get_remaining_time(self, cool_down_name: str) -> int:
        if (not cool_down_name in self.__cool_downs):
            return 0;
        return self.__cool_downs[cool_down_name].get_remaining_time();
    
    def __init__(self, member: discord.Member):
        self.member = member;
        self.__cool_downs = {};
        return;

class ServerDataObject:
    
    server_id: str;
    
    __user_data = {};
    
    __loop_muted = {};
    
    __currently_pinged = [];
    
    __mudae_hitlist = [];
    
    def is_currently_pinged(self, member) -> bool:
        if (member.id in self.__currently_pinged):
            return True;
        return False;
    
    def set_currently_pinged(self, member, is_pinged: bool):
        if (is_pinged):
            self.__currently_pinged.append(member.id);
            return;
        self.__currently_pinged.remove(member.id);
    
    def get_user_data(self, member: discord.Member):
        if (not member.id in self.__user_data):
            self.__user_data[member.id] = UserData(member);
        return self.__user_data[member.id];
    
    def add_to_mudae_hitlist(self, str) -> bool:
        if (str in self.__mudae_hitlist or len(self.__mudae_hitlist) >= CHARACTER_HITLIST_LIMIT):
            return False;
        self.__mudae_hitlist.append(str);
        return True;
    
    def get_mudae_hitlist(self):
        return self.__mudae_hitlist;
    
    def remove_from_mudae_hitlist(self, str) -> bool:
        if (not str in self.__mudae_hitlist):
            str = self.search_mudae_hitlist(str);
            if (not str):
                return False;
        self.__mudae_hitlist.remove(str);
        return True;
    
    def search_mudae_hitlist(self, str: str):
        for character in self.__mudae_hitlist:
            if (str == character or character in str or str in character):
                return character;
    
    def clear_mudae_hitlist(self):
        self.__mudae_hitlist = [];
        return;
    
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

#Converts seconds to hours, minutes, seconds, returns a tuple of (hours, minutes, seconds)
def convert_to_time_format(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    return hour, min, sec

def print_report(message: str):
    print(get_current_date_time() + message);
    return;