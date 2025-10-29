import asyncio
from datetime import datetime, timedelta, time
import random
from zoneinfo import ZoneInfo
import os
from messaging import send_attendance_message
import logging

log = logging.getLogger(__name__)
BRUSSELS = ZoneInfo("Europe/Brussels")

def random_time_between(start_hour, start_minute, end_hour, end_minute, ref_date=None):
    """Return a random datetime between start and end on ref_date in Brussels time."""
    if ref_date is None:
        ref_date = datetime.now(BRUSSELS).date()
    start = datetime.combine(ref_date, time(start_hour, start_minute, tzinfo=BRUSSELS))
    end = datetime.combine(ref_date, time(end_hour, end_minute, tzinfo=BRUSSELS))
    delta_seconds = int((end - start).total_seconds())
    random_seconds = random.randint(0, max(delta_seconds, 0))
    return start + timedelta(seconds=random_seconds)

async def attendance_scheduler(bot):
    log.info("Attendance scheduler started")
    while True:
        now = datetime.now(BRUSSELS)
        weekday = now.weekday()  # 0=Monday, 6=Sunday
        log.info(f"Weekday: {weekday}")

        if weekday in [1, 3, 4]:
            today = now.date()

            # Morning and afternoon
            while True:
                morning_time = random_time_between(9, 15, 12, 30, ref_date=today)
                if not (morning_time.hour == 11 and 0 <= morning_time.minute < 15):
                    break
            while True:
                afternoon_time = random_time_between(14, 0, 16, 45, ref_date=today)
                if not (afternoon_time.hour == 15 and 0 <= afternoon_time.minute < 15):
                    break

            log.info(f"Today's schedule: morning at {morning_time}, afternoon at {afternoon_time}")

            for event_time in [morning_time, afternoon_time]:
                sleep_seconds = (event_time - datetime.now(BRUSSELS)).total_seconds()
                if sleep_seconds > 0:
                    log.info(f"Sleeping until {event_time} ({sleep_seconds/3600:.2f}h)")
                    await asyncio.sleep(sleep_seconds)
                    await send_attendance_message(bot)
                else:
                    log.info(f"Skipping past time {event_time}")
        else:
            log.info(f"Skipping {now.strftime('%A')} - not a scheduled day.")

        # Sleep until next day 00:05 Brussels time
        tomorrow = (now + timedelta(days=1)).date()
        midnight = datetime.combine(tomorrow, time(0, 5, tzinfo=BRUSSELS))
        sleep_seconds = (midnight - datetime.now(BRUSSELS)).total_seconds()
        log.info(f"Sleeping until {midnight} ({sleep_seconds/3600:.2f}h)")
        await asyncio.sleep(sleep_seconds)
