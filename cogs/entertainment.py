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

class Entertainment(commands.Cog):
    @app_commands.command(name='silly', description='Send a random silly gif')
    async def silly(self, interaction: discord.Interaction):
        try:
            print("Called")
            await interaction.channel.send(random.choice(random_silly_gifs));
            return await interaction.response.send_message('SILLY :33', ephemeral=True)
        except Exception as e:
            print_report(f'Error sending silly gif: {e}')
        
async def setup(bot):
    await bot.add_cog(Entertainment(bot));
    print("Entertainment cog loaded")