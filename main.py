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

#--bot events
@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot));

@bot.event
async def on_message(message):
    if (message.author == bot.user):
        return;
    user_message: str = message.content;
    print_report(f'User {message.author} sent a message: {user_message}')
    await bot.process_commands(message)
    await delete_messages_if_muted(message)

load_dotenv(encoding='utf-16')
async def main():
    async with bot:
        for filename in os.listdir('cogs'):
            if (filename.find('.py') != -1):
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())