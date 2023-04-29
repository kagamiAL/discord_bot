import discord;
import random;
from discord import Embed;
from discord import app_commands;
from datetime import timedelta;
import asyncio;
from global_data import *;
from discord.ext import commands

#FUNCTIONS
async def send_message(ctx, message_content, is_private):
    try:
        await ctx.author.send(message_content) if is_private else await ctx.channel.send(message_content);
    except Exception as e:
        print(e);   

#--returns muted role, if it doesn't exist, create it
async def get_muted_role(ctx):
    server = ctx.guild
    role = discord.utils.get(server.roles, name="Muted")
    if (not role):
        role = await server.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
    return role

#--loops through arrays of roles and removes any that are bot-managed
def sort_role_array(role_arr):
    return [x for x in role_arr if not x.is_bot_managed()]


#--handles mute state
async def handle_mute_state(ctx, member, is_muted: bool, time_out_duration: int):
    server_data_object = get_server_data(ctx.guild.id);
    server_data_object.set_currently_muted(member, is_muted);
    if (is_muted):
        try:
            await member.timeout(timedelta(minutes=time_out_duration), reason="User was timed out by the bot")
        except Exception as e:
            print_report(f"Failed to timeout user: {e}");

random_gifs = ['https://media.tenor.com/APFvROVc6CwAAAAC/sad-sorry.gif', 'https://media.tenor.com/h8zc8kPJDYoAAAAC/drake-dake.gif', 'https://media.tenor.com/NQfq1liFH-8AAAAd/byuntear-sad.gif', 'https://media.tenor.com/-DY1sCSEXqUAAAAd/sad-cat.gif']
random_sayings = ['Go outside and enjoy the outdoors or something', "Look who isn't working on their assignments rn", 'Did you know? Focusing on your work is 10x more efficient than being here']

#--modifies embed according to mute state
async def send_embed_to_channel(ctx, member, is_muted):
    global main_msg;
    try:
        description_string = random.choice(random_sayings)
        main_embed = Embed(colour=discord.Colour(0x7289da), description=description_string, title=f'Loop mute: {member.name} has been {"un" if not is_muted else ""}muted');
        main_embed.set_thumbnail(url=random.choice(random_gifs));
    except Exception as e:
        print_report(f'Error creating Embed: {e}')
    try:
        await ctx.channel.send("@here")
    except Exception as e:
        print_report(f'Error sending @here: {e}')
    try:
        main_msg = await ctx.channel.send(embed=main_embed);
    except Exception as e:
        print_report(f'Error sending Embed: {e}')
    return {'msg': main_msg, 'embed': main_embed};

#--modifies embed so it countsdown
async def modify_embed_countdown(embed_data, time_left: int, is_muted: bool):
    try:
        main_embed = embed_data['embed'];
        main_msg = embed_data['msg'];
        main_embed.remove_field(index=0)
        main_embed.insert_field_at(
            index=0,
            name='Time left',
            value=str(time_left) + (' minutes' if time_left > 1 else ' minute') + (' until unmute' if is_muted else ' until mute'),
        )
    except Exception as e:
        print_report(f'Error modifying Embed: {e}')
    try:
        await main_msg.edit(embed=main_embed);
    except Exception as e:
        print_report(f'Error editing Embed: {e}')

#--starts mute loop
async def handle_mute_loop(ctx, member, interval_minutes: int, mute_duration: int, immediate_mute: str):
    print(immediate_mute)
    global embed_data;
    SLEEP_INTERVAL = 60;
    STARTING_MUTE_STATE = (True if immediate_mute.lower() == 'true' else False);
    running_loop = asyncio.get_running_loop();
    server_data_object = get_server_data(ctx.guild.id);
    time_passed: int    = 0;
    server_data_object.set_loop_muted(member, True);
    embed_data = await send_embed_to_channel(ctx, member, STARTING_MUTE_STATE);
    await modify_embed_countdown(embed_data, mute_duration, STARTING_MUTE_STATE);
    await handle_mute_state(ctx, member, is_muted=STARTING_MUTE_STATE, time_out_duration=(mute_duration if STARTING_MUTE_STATE else interval_minutes));
    print_report("Loop mute has started")
    while (server_data_object.is_loop_muted(member)):
            if (not server_data_object.is_currently_muted(member)):
                if (time_passed >= interval_minutes):
                    print_report("Currently muting...")
                    embed_data = await send_embed_to_channel(ctx, member, True);
                    await modify_embed_countdown(embed_data, mute_duration, True);
                    await handle_mute_state(ctx, member, is_muted=True, time_out_duration=mute_duration);
                    time_passed = 0;
                    print_report("Sucessfully muted")
            elif (time_passed >= mute_duration):
                print_report("Currently unmuting...")
                embed_data = await send_embed_to_channel(ctx, member, False);
                await modify_embed_countdown(embed_data, interval_minutes, False);
                await handle_mute_state(ctx, member, is_muted=False, time_out_duration=interval_minutes);
                time_passed = 0;
                print_report("Successfully unmuted")
            await asyncio.sleep(SLEEP_INTERVAL);
            time_passed += 1;
            print_report(f"Time passed: {time_passed} minutes")
            running_loop.create_task(modify_embed_countdown(embed_data, (mute_duration if server_data_object.is_currently_muted(member) else interval_minutes) - time_passed, server_data_object.is_currently_muted(member)));

class Moderation(commands.Cog):
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def loop_mute(self, ctx, member: discord.Member, interval_minutes: int, mute_duration: int, immediate_mute: str):
        if (not get_server_data(ctx.guild.id).is_loop_muted(member)):
            if (member.roles[-1] >= ctx.guild.get_member(self.bot.user.id).roles[-1]):
                return print_report("Attempt to mute a user with a higher role than the bot")
            return await handle_mute_loop(ctx, member, interval_minutes, mute_duration, immediate_mute);
        return

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def un_loop_mute(self, ctx, member: discord.Member):
        server_data_object = get_server_data(ctx.guild.id);
        if (server_data_object.is_loop_muted(member)):
            server_data_object.set_loop_muted(member, False);
    
    def __init__(self, bot):
        self.bot = bot;

async def setup(bot):
    await bot.add_cog(Moderation(bot));
    print("Moderation cog loaded")
