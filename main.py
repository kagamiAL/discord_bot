import discord
import asyncio
from global_data import *
from discord.ext import commands;
import os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot     = commands.Bot(command_prefix='#', intents=intents);

#--global functions

async def delete_messages_if_muted(message: discord.Message):
    if (get_server_data(message.guild.id).is_currently_muted(message.author)):
        await message.delete()
    return;

async def filter_mudae_hitlist(message: discord.Message):
    try:
        if (message.author.name == "Mudae"):
            server_data_object  = get_server_data(message.guild.id);
            if (len(message.embeds) > 0):
                embed: discord.Embed   = message.embeds[0];
                if server_data_object.search_mudae_hitlist(embed.author.name.lower()):
                    return await message.delete();
    except Exception as e:
        print_report(f'Error filtering mudae hitlist: {e}')

#--bot events
@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot));

@bot.event
async def on_message(message):
    if (message.author == bot.user):
        return;
    await bot.process_commands(message)
    await delete_messages_if_muted(message)
    await filter_mudae_hitlist(message)

load_dotenv(encoding='utf-16')
async def main():
    async with bot:
        for filename in os.listdir('cogs'):
            if (filename.find('.py') != -1):
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())