import discord

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
                };
            return
        del self.__loop_muted[member.id];
    
    def is_loop_muted(self, member) -> bool:
        if (member.id in self.__loop_muted):
            return True
        return False
    
    def get_muted_original_roles(self, member):
        if (member.id in self.__loop_muted):
            return self.__loop_muted[member.id]['roles'];
    
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