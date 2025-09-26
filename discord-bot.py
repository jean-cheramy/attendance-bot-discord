import os
import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

BRUSSELS = ZoneInfo("Europe/Brussels")

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
    Return a datetime on ref_date (or today) with a random time between start and end in Brussels time.
    """
    if ref_date is None:
        ref_date = datetime.now(BRUSSELS).date()
    start = datetime.combine(ref_date, time(start_hour, start_minute, tzinfo=BRUSSELS))
    end = datetime.combine(ref_date, time(end_hour, end_minute, tzinfo=BRUSSELS))
    delta_seconds = int((end - start).total_seconds())
    random_seconds = random.randint(0, max(delta_seconds, 0))
    return start + timedelta(seconds=random_seconds)

async def send_attendance_message():
    """
    Send a message in the remote-attendance channel with counts
    of members in Bouman-9 voice channels.
    """
    try:
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

        member = guild.get_member(1283510701763068018)
        if member:
            await channel.send(f"- {member.mention} - Learners in Bouman-9 voice channels: {count}")
        else:
            await channel.send(f"- Learners in Bouman-9 voice channels: {count}")

        print(f"Attendance message sent at {datetime.now(BRUSSELS)}")
    except discord.Forbidden:
        print("Bot does not have permission to send messages in the channel.")
    except Exception as e:
        print(f"Error sending attendance message: {e}")

async def attendance_scheduler():
    """
    Scheduler that waits until morning random slot and afternoon random slot,
    sends the attendance messages, then stops (bot exits at the end).
    """
    try:
        now = datetime.now(BRUSSELS)
        weekday = now.weekday()  # 0 = Monday, 6 = Sunday
        if weekday >= 5:
            print("Today is Saturday or Sunday. Exiting without sending messages.")
            return

        today = now.date()
        morning_time = random_time_between(9, 30, 12, 30, ref_date=today)
        afternoon_time = random_time_between(14, 0, 16, 45, ref_date=today)

        for event_time in [morning_time, afternoon_time]:
            sleep_seconds = (event_time - datetime.now(BRUSSELS)).total_seconds()
            if sleep_seconds > 0:
                print(f"Sleeping until {event_time}")
                await asyncio.sleep(sleep_seconds)
                await send_attendance_message()
    except Exception as e:
        print(f"Scheduler error: {e}")
    finally:
        await bot.close()
        print("Bot has exited after sending attendance messages.")

if __name__ == '__main__':
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("DISCORD_TOKEN environment variable not set.")
    bot.run(token)
