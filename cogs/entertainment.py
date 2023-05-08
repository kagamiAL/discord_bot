import discord;
import random;
from discord import Embed;
from global_data import *;
from discord.ext import commands;
from discord import app_commands;

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
            character_name = character_name.lower();
            server_data_object = get_server_data(ctx.guild.id)
            if (server_data_object.remove_from_mudae_hitlist(character_name)):
                return await ctx.response.send_message(f'Removed ({character_name}) from the mudae hitlist', ephemeral=True)
            return await ctx.response.send_message(f'({character_name}) was not on the mudae hitlist', ephemeral=True)
        except Exception as e:
            print_report(f'Error removing from mudae hitlist: {e}')
    
    def __init__(self, bot):
        self.bot = bot
    
async def setup(bot):
    await bot.add_cog(Entertainment(bot));
    print("Entertainment cog loaded")