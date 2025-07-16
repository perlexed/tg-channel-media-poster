import logging
from config.settings import Settings, ConfigError
from fs.folder_utils import FolderUtils
from fs.file_utils import FileUtils
from utils.date_utils import folder_to_date, date_to_folder, get_next_day
from tg_local.tg_poster import TelegramPoster
import os
from typing import Optional

class AppException(Exception):
    """Custom exception for business logic errors."""
    pass

class Distributor:
    def __init__(self, settings: Settings, tg_poster: Optional[TelegramPoster], dry_run: bool = False):
        self.settings = settings
        self.tg_poster = tg_poster
        self.dry_run = dry_run

    async def process_day(self, date, folder, batch, close_callback):
        if self.dry_run or self.tg_poster is None:
            logging.info(f'DRY RUN: Would move {len(batch)} files to folder: {folder}')
            logging.info(f'DRY RUN: Would send scheduled images for {date.strftime("%Y-%m-%d")}: {[os.path.basename(f) for f in batch]}')
            logging.info(f'DRY RUN: Would mark day folder as closed: {folder}')
        else:
            telegram_connected = False
            try:
                await self.tg_poster.connect()
                telegram_connected = True
                FileUtils.move_files_to_folder(batch, folder)
                await self.tg_poster.send_scheduled_images(
                    self.settings.telegram.chat_id,
                    [os.path.join(folder, os.path.basename(f)) for f in batch],
                    date
                )
                close_callback(folder)
                logging.info(f'Processed and scheduled images for {date.strftime("%Y-%m-%d")}')
            finally:
                if telegram_connected:
                    await self.tg_poster.disconnect()

    async def run(self):
        if self.dry_run:
            logging.info('DRY RUN: Starting distribution process simulation')
        else:
            logging.info('Starting distribution process')
        
        # First, do all file operations and validation
        last_closed_day = FolderUtils.find_last_closed_day(self.settings.target_root_folder)
        if not last_closed_day:
            raise AppException('No closed days found in targetRootFolder')

        # Prepare days to fill
        days_to_fill = []
        last_date = folder_to_date(*last_closed_day)
        current_date = get_next_day(last_date)
        for _ in range(self.settings.days_to_fill_count):
            year, month, day = date_to_folder(current_date)
            if self.dry_run:
                day_folder = os.path.join(self.settings.target_root_folder, year, month, day)
                logging.info(f'DRY RUN: Would create day folder: {day_folder}')
            else:
                day_folder = FolderUtils.create_day_folder(self.settings.target_root_folder, year, month, day)
            days_to_fill.append((current_date, day_folder))
            current_date = get_next_day(current_date)

        # Check source files
        images = FileUtils.get_image_files(self.settings.source_folder)
        expected_count = self.settings.days_to_fill_count * self.settings.batch_size
        if len(images) != expected_count:
            raise AppException(f'Expected {expected_count} images, found {len(images)}')

        # Shuffle and split
        images_batches = FileUtils.shuffle_and_split(images, self.settings.batch_size)
        images_by_folders = list(zip(days_to_fill, images_batches))

        # Distribute and publish
        for (date, folder), batch in images_by_folders:
            await self.process_day(date, folder, batch, FolderUtils.mark_day_folder_closed)
        
        if self.dry_run:
            logging.info('DRY RUN: Distribution process simulation completed')
        else:
            logging.info('Distribution process completed') 