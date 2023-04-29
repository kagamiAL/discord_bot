import discord
import asyncio
from discord.ext import commands;
import os
from dotenv import load_dotenv

intents = discord.Intents.all()
bot     = commands.Bot(command_prefix='#', intents=intents);


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot));

@bot.event
async def on_message(message):
    if (message.author == bot.user):
        return;
    user_message: str = message.content;
    print(f'User {message.author} sent a message: {user_message}')
    await bot.process_commands(message)

load_dotenv(encoding='utf-16')
async def main():
    async with bot:
        for filename in os.listdir('cogs'):
            if (filename.find('.py') != -1):
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await bot.start(os.getenv('TOKEN'))

asyncio.run(main())