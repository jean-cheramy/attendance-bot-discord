import logging
import sys, traceback
import os
import discord
from discord.ext import commands
from scheduler import attendance_scheduler
from health import start_health_server, heartbeat

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)
log.info("App is booting!")

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready() -> None:
    """Runs on bot connection; logs info and starts attendance, heartbeat, and health server tasks."""
    log.info(f"Connected as {bot.user} (ID {bot.user.id})")
    bot.loop.create_task(attendance_scheduler(bot))
    bot.loop.create_task(heartbeat())
    bot.loop.create_task(start_health_server())

if __name__ == "__main__":
    try:
        token = os.getenv("DISCORD_BOT_TOKEN")
        if not token:
            raise ValueError("DISCORD_BOT_TOKEN environment variable is missing")
        log.info("Running the bot...")
        bot.run(token)
    except Exception as e:
        log.error(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
