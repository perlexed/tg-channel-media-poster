import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient
import os
from dotenv import load_dotenv
from typing import cast

load_dotenv()
api_id_env = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

if not api_id_env or not api_hash or not phone:
    raise RuntimeError('TELEGRAM_API_ID, TELEGRAM_API_HASH, and TELEGRAM_PHONE must all be set in the environment or .env file.')

api_id = int(api_id_env)
api_hash = cast(str, api_hash)
phone = cast(str, phone)

async def main():
    async with TelegramClient('schedule_test', api_id, str(api_hash)) as client:
        coroutine = client.start(phone=phone)
        await coroutine
        # Schedule message for 1 minute from now
        schedule_time = datetime.now() + timedelta(minutes=1)
        message = f"Test scheduled message at {schedule_time.strftime('%Y-%m-%d %H:%M:%S')}"
        channel_id = -1001617251413
        await client.send_message(
            channel_id,
            message,
            schedule=schedule_time
        )
        print(f"Scheduled message to '{channel_id}' for {schedule_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == '__main__':
    asyncio.run(main()) 