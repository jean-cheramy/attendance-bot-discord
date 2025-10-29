import os
from discord.utils import get
from datetime import datetime
import logging

log = logging.getLogger(__name__)

async def send_attendance_message(bot) -> None:
    """Send a message in the configured channel with counts of members in the configured category."""
    CHANNEL_NAME = os.getenv("CHANNEL_NAME")
    ROLE_NAME = os.getenv("ROLE_NAME")
    CATEGORY_NAME = os.getenv("CATEGORY_NAME")
    USER_ID = int(os.getenv("USER_ID"))

    try:
        if not bot.guilds:
            log.warning("No guilds available.")
            return
        guild = bot.guilds[0]
        role = get(guild.roles, name=ROLE_NAME)
        category = get(guild.categories, name=CATEGORY_NAME)
        channel = get(guild.text_channels, name=CHANNEL_NAME)
        if not role or not category or not channel:
            log.warning("Role, category, or channel not found.")
            return

        members_in_voice = {m.id for c in category.channels if isinstance(c, guild.voice_channels[0].__class__) for m in c.members}
        count = max(0, len(members_in_voice) - 1)

        mention = f"<@{USER_ID}>"
        await channel.send(f"- {mention} - Learners in {CATEGORY_NAME} voice channels: {count}")
        log.info(f"Attendance message sent at {datetime.now()}")
    except Exception as e:
        log.error(f"Error sending attendance message: {e}")
