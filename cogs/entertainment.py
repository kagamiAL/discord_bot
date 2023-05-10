import asyncio
import discord;
import random;
from global_data import *;
import constants;
from discord.ext import commands;
from discord import app_commands;

REMOVE_ACTION_NAME: str = 'remove_from_hitlist'

COOL_DOWN_TIME_SECONDS: int = 172800

random_silly_gifs = [
    'https://media.tenor.com/v6j3qu9ZmMIAAAAd/funny-cat.gif', 
    'https://media.tenor.com/qRhkAc08-doAAAAd/my-true.gif', 
    'https://media.tenor.com/oR19o57bN_gAAAAd/funny-cat.gif',
    'https://media.tenor.com/sbosXbCkxm0AAAAM/this-cat-is-cat.gif',
    'https://media.tenor.com/kxj_Pcpp2wIAAAAM/cat-kitten.gif',
    'https://media.tenor.com/B32h0zF0G1gAAAAM/cat-funny.gif',
    'https://media.tenor.com/Zz9d8m9MSy0AAAAM/funny-animals-tweakin.gif',
    'https://media.tenor.com/_3pxkYZMNGYAAAAM/cat-facetime.gif',
    'https://media.tenor.com/KhEOlkmMEJ4AAAAM/t-cat-draker-cat.gif',
]

nerd_gifs = [
    'https://media.tenor.com/SRX8X6DNF6QAAAAd/nerd-nerd-emoji.gif',
    'https://media.tenor.com/DuThn51FjPcAAAAC/nerd-emoji-nerd.gif'
]

async def find_latest_message(user_id, channel):
    async for message in channel.history(limit=100):
        if message.author.id == user_id:
            return message
    return None

def get_cooldown_string(user_data, action_name: str) -> str:
    return "You are on cooldown for this command, time remaining: {0:.1f} hrs, {1:.1f} min, {2:.1f} sec".format(*convert_to_time_format(user_data.get_remaining_time(action_name)))
class Entertainment(commands.Cog):
    @app_commands.command(name='silly', description='Send a random silly gif')
    async def silly(self, interaction: discord.Interaction):
        try:
            await interaction.channel.send(random.choice(random_silly_gifs));
            return await interaction.response.send_message('SILLY :33', ephemeral=True)
        except Exception as e:
            print_report(f'Error sending silly gif: {e}')
        
    @app_commands.command(name='nerd_reply', description='Reply to with nerd')
    async def nerd_reply(self, interaction: discord.Interaction, member: discord.Member):
        try:
            latest_message: discord.Message  = await find_latest_message(member.id, interaction.channel)
            if (latest_message):
                await latest_message.reply(random.choice(nerd_gifs));
                await interaction.response.send_message('Replied to nerd', ephemeral=True)
        except Exception as e:
            print_report(f'Error sending nerd gif: {e}')
    
    @app_commands.command(name='speak', description='Speak as the bot')
    async def speak(self, ctx: discord.Interaction, message: str):
        try:
            application_info = await self.bot.application_info()
            owner = application_info.owner
            if (ctx.user.id != owner.id):
                return await ctx.response.send_message("You do not have the required permissions to use this command")
            await ctx.channel.send(message);
            await ctx.response.send_message("Spoke", ephemeral=True)
        except Exception as e:
            print_report(f'Error speaking: {e}')
            
    @app_commands.command(name='add_to_mudae_hitlist', description='Delete all instances of this character if it appears')
    async def add_to_mudae_hitlist(self, ctx: discord.Interaction, character_name: str):
        try: 
            character_name = character_name.lower();
            if (len(character_name) < 4):
                return await ctx.response.send_message("Character name must be at least 4 characters long", ephemeral=True);
            server_data_object = get_server_data(ctx.guild.id)
            if (server_data_object.add_to_mudae_hitlist(character_name)):
                return await ctx.response.send_message(f'Added ({character_name}) to the mudae hitlist', ephemeral=True)
            return await ctx.response.send_message(f'({character_name}) is already on the mudae hitlist', ephemeral=True)
        except Exception as e:
            print_report(f'Error adding to mudae hitlist: {e}')
    
    @app_commands.command(name='get_mudae_hitlist', description='Read all characters on the mudae hitlist')
    async def read_mudae_hitlist(self, ctx: discord.Interaction):
        server_data_object = get_server_data(ctx.guild.id)
        return await ctx.response.send_message('Current mudae hitlist:\n' + '\n'.join(server_data_object.get_mudae_hitlist()), ephemeral=True)
    
    @app_commands.command(name='remove_from_mudae_hitlist', description='Remove a character from the mudae hitlist')
    async def remove_from_mudae_hitlist(self, ctx: discord.Interaction, character_name: str):
        try:
            application_info = await self.bot.application_info()
            owner = application_info.owner
            server_data_object: ServerDataObject = get_server_data(ctx.guild.id)
            if (ctx.user.id != owner.id):
                return await ctx.response.send_message('You do not have the permissions to use this command', ephemeral=True);
            character_name = character_name.lower();
            if (server_data_object.remove_from_mudae_hitlist(character_name)):
                return await ctx.response.send_message(f'Removed ({character_name}) from the mudae hitlist', ephemeral=True)
            return await ctx.response.send_message(f'({character_name}) was not on the mudae hitlist', ephemeral=True)
        except Exception as e:
            print_report(f'Error removing from mudae hitlist: {e}')
    
    @app_commands.command(name="repeatedly_ping", description="Repeatedly ping a user/role")
    async def repeatedly_ping(self, ctx: discord.Interaction, pingable: discord.Member|discord.Role, amt_ping: int):
        MAX_PINGS = 75
        INTERVAL_TIME: int = 1
        ACTION_NAME: str    = 'spam_ping'
        try: 
            if (not ctx.user.guild_permissions.administrator):
                return await ctx.response.send_message("You do not have the required permissions to use this command", ephemeral=True);
            server_data_object: ServerDataObject = get_server_data(ctx.guild.id)
            user_data: UserData   = server_data_object.get_user_data(ctx.user)
            if (user_data.is_on_cooldown(ACTION_NAME)):
                return await ctx.response.send_message(get_cooldown_string(user_data, ACTION_NAME), ephemeral=True);
            if (server_data_object.is_currently_pinged(pingable)):
                return await ctx.response.send_message(f'({pingable}) is already being pinged', ephemeral=True)
            user_data.set_cooldown(ACTION_NAME, constants.get_constant('repeat_ping_cool_down'));
            server_data_object.set_currently_pinged(pingable, True);
            amt_ping = (amt_ping if amt_ping <= MAX_PINGS else MAX_PINGS)
            await ctx.response.send_message(f'Pinging ({pingable}) {amt_ping} times', ephemeral=True)
            for _ in range(amt_ping):
                await ctx.channel.send(pingable.mention)
                await asyncio.sleep(INTERVAL_TIME)
            server_data_object.set_currently_pinged(pingable, False);
        except Exception as e:
            print_report(f'Error repeatedly pinging: {e}')
    
    def __init__(self, bot):
        self.bot = bot
    
async def setup(bot):
    await bot.add_cog(Entertainment(bot));
    print("Entertainment cog loaded")