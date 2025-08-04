import logging
from telethon import TelegramClient
from datetime import datetime, timezone, timedelta
from typing import List

class TelegramPoster:
    def __init__(self, api_id: str, api_hash: str, phone: str):
        print('DEBUG: api_id', api_id)
        self.api_id = int(api_id)  # Convert to int
        self.api_hash = api_hash
        self.phone = phone
        self.client = None

    async def connect(self):
        """Connect to Telegram and authenticate"""
        self.client = TelegramClient('session_name', self.api_id, self.api_hash)

        tg_start_coroutine = self.client.start(phone=self.phone)
        await tg_start_coroutine
        logging.info("Connected to Telegram as user")

    async def disconnect(self):
        """Disconnect from Telegram"""
        if self.client and self.client.is_connected():
            self.client.disconnect()

    async def send_scheduled_images(self, chat_id: str, image_paths: List[str], scheduled_date: datetime):
        """
        Send images as a single album (bulk) scheduled message to the chat at 23:00 KRAT (UTC+7) on the given date.
        """
        if not self.client:
            raise Exception("Not connected to Telegram. Call connect() first.")
        
        # Set time to 23:00 KRAT (UTC+7)
        send_time = scheduled_date.replace(hour=23, minute=0, second=0, microsecond=0)
        
        # Convert to UTC timestamp for Telegram
        send_time_utc = send_time - timedelta(hours=7)
        schedule_time = send_time_utc.replace(tzinfo=timezone.utc)
        
        try:
            # Send all images as a single album
            await self.client.send_file(
                int(chat_id),
                image_paths,
                schedule=schedule_time
            )
            logging.info(f"Scheduled album of {len(image_paths)} images for {scheduled_date.strftime('%Y-%m-%d %H:%M')}")
        except Exception as e:
            logging.error(f"Failed to send scheduled images: {e}")
            raise 