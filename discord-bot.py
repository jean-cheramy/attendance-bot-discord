import os
import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta, time

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

CHANNEL_NAME = "remote-attendance"
ROLE_NAME = "Bouman-9"
CATEGORY_NAME = "Bouman-9"

@bot.event
async def on_ready():
    """
    Called when the bot is ready. Starts the attendance scheduler.
    """
    print(f'Connected as {bot.user} (ID {bot.user.id})')
    bot.loop.create_task(attendance_scheduler())

def random_time_between(start_hour, start_minute, end_hour, end_minute, ref_date=None):
    """
    Return a datetime on ref_date (or today) with a random time between start and end.
    """
    if ref_date is None:
        ref_date = datetime.now().date()
    start = datetime.combine(ref_date, time(start_hour, start_minute))
    end = datetime.combine(ref_date, time(end_hour, end_minute))
    delta_seconds = int((end - start).total_seconds())
    random_seconds = random.randint(0, max(delta_seconds, 0))
    return start + timedelta(seconds=random_seconds)

async def send_attendance_message():
    """
    Send a message in the remote-attendance channel with counts
    of members in Bouman-9 voice channels.
    """
    if not bot.guilds:
        print("No guilds available.")
        return
    guild = bot.guilds[0]
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)
    if not role or not category or not channel:
        print("Role, category, or channel not found.")
        return

    voice_channels = [c for c in category.channels if isinstance(c, discord.VoiceChannel)]
    members_in_voice = set()
    for vc in voice_channels:
        for m in vc.members:
            members_in_voice.add(m.id)
    count = max(0, len(members_in_voice) - 1)
    await channel.send(f"- @jeanaicoach - Learners in Bouman-9 voice channels: {count}")

async def attendance_scheduler():
    """
    Scheduler that waits until morning random slot and afternoon random slot,
    sends the attendance messages, then stops (bot exits at the end).
    """
    today = datetime.now().date()
    morning_time = random_time_between(9, 30, 12, 30, ref_date=today)
    afternoon_time = random_time_between(14, 0, 16, 45, ref_date=today)

    for event_time in [morning_time, afternoon_time]:
        sleep_seconds = (event_time - datetime.now()).total_seconds()
        if sleep_seconds > 0:
            await asyncio.sleep(sleep_seconds)
            await send_attendance_message()
    await bot.close()

if __name__ == '__main__':
    token = os.getenv("DISCORD_TOKEN")
    bot.run(token)
