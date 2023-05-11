import discord
import time
import constants;
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
    
    member = None;
    
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
    
    __pingable_roles = [];
    
    __blacklisted_categories = [];
    
    __mudae_hitlist = {};
    
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
    
    #Checks if the role is pingable
    def is_pingable_role(self, role: discord.Role) -> bool:
        return (role.id in self.__pingable_roles)
    
    #Adds a role to pingable roles
    def add_pingable_role(self, role: discord.Role) -> bool:
        if (role.id in self.__pingable_roles):
            return False;
        self.__pingable_roles.append(role.id);
        return True;
    
    #Returns if category is blacklisted
    def is_blacklisted_category(self, category: discord.CategoryChannel) -> bool:
        return (category.id in self.__blacklisted_categories);
    
    #Adds a blacklisted category
    def blacklist_category(self, category: discord.CategoryChannel) -> bool:
        if (category.id in self.__blacklisted_categories):
            return False;
        self.__blacklisted_categories.append(category.id);
        return True;
    
    #Checks if the character in the hitlist is past the duration, removes them if so, (RETURNS TRUE IF REMOVED)
    def check_mudae_hitlist_status(self, char_name: str) -> bool:
        if (char_name in self.__mudae_hitlist):
            if (time.time() - self.__mudae_hitlist[char_name] >= constants.get_constant('hitlist_duration')):
                del self.__mudae_hitlist[char_name];
                return True;
        return False;
    
    #Checks entire hitlist for expired characters
    def check_entire_mudae_hitlist(self):
        for char_name in list(self.__mudae_hitlist.keys()):
            self.check_mudae_hitlist_status(char_name);
        return;
    
    def add_to_mudae_hitlist(self, str) -> bool:
        if (str in self.__mudae_hitlist or len(self.__mudae_hitlist) >= CHARACTER_HITLIST_LIMIT):
            return False;
        self.__mudae_hitlist[str]   = time.time();
        return True;
    
    def get_mudae_hitlist(self):
        return self.__mudae_hitlist;
    
    def remove_from_mudae_hitlist(self, str) -> bool:
        if (not str in self.__mudae_hitlist):
            return False;
        del self.__mudae_hitlist[str];
        return True;
    
    def search_mudae_hitlist(self, str: str):
        if (str and str in self.__mudae_hitlist):
            return str;
    
    def clear_mudae_hitlist(self):
        self.__mudae_hitlist = {};
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