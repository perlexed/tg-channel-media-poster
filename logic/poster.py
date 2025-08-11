import asyncio
import logging
import os
import random
from typing import List

from fs.file_utils import FileUtils
from fs.folder_utils import FolderUtils
from tg_local.tg_poster import TelegramPoster


class Poster(object):
    def __init__(self, telegram_chat_id: str, tg_poster: TelegramPoster):
        self.tg_poster = tg_poster
        self.telegram_chat_id = telegram_chat_id

    async def process_day(self, date, folder, batch):
        FileUtils.move_files_to_folder(batch, folder)
        await self.tg_poster.send_scheduled_images(
            self.telegram_chat_id,
            [os.path.join(folder, os.path.basename(f)) for f in batch],
            date
        )
        FolderUtils.mark_day_folder_closed(folder)
        logging.info(f'Processed and scheduled images for {date.strftime("%Y-%m-%d")}')

    async def process_batch(self, images_batch: List[str]):
        telegram_connected = False
        try:
            await self.tg_poster.connect()
            telegram_connected = True

            should_delay_posts = len(images_batch) > 1

            for (date, folder), batch in images_batch:
                await self.process_day(date, folder, batch)

                if not should_delay_posts:
                    continue

                delay = random.uniform(4, 8)
                print(f"Waiting {delay:.2f} seconds before next post...")
                await asyncio.sleep(delay)

        finally:
            if telegram_connected:
                await self.tg_poster.disconnect()



