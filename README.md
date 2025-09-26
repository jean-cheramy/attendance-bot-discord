# BeCode Attendance Bot

## About

I’m a coach at [**BeCode**](https://becode.org/fr/), and I need to make sure my learners are actively participating in the online Discord class. To simplify this process, I built this bot.

The bot **randomly checks the number of learners connected to the voice channels** in a specific class category on Discord. This allows me to monitor attendance without manually checking each session.

## Features

- Counts learners in the **“Bouman-9”** category and its voice channels.  
- Sends the count to a **“remote-attendance”** text channel.  
- Sends messages **twice a day**: once in the morning and once in the afternoon at random times.  
- **Does not run on weekends** to avoid unnecessary activity.  
- Fully logs actions for debugging and tracking.
- Deployed as a free app on [Railway](https://railway.com)

## Usage

1. **Set up the bot on Discord** and invite it with permissions to read channels, view voice channels, and send messages.  
2. **Set the environment variable** `DISCORD_TOKEN` with your bot’s token.  
3. Run the bot:

```bash
python discord-bot.py
```

The bot will automatically send attendance messages at random times during the day (morning and afternoon) on weekdays.

## Notes

- Ensure the bot has access to the **“Bouman-9”** category and the **“remote-attendance”** text channel.  
- All scheduling uses **Brussels time (UTC+1/UTC+2 with DST)**.  
- The bot automatically **skips weekends (Saturday and Sunday)**.  
- The bot only counts learners in voice channels; it does not track text activity.  
- All actions are logged to the console for monitoring and debugging.
