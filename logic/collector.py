import logging
from config.settings import Settings, ConfigError
from fs.folder_utils import FolderUtils
from fs.file_utils import FileUtils
from utils.date_utils import folder_to_date, date_to_folder, get_next_day
import os

class AppException(Exception):
    """Custom exception for business logic errors."""
    pass

class Collector:
    def __init__(self, settings: Settings, dry_run: bool = False):
        self.settings = settings
        self.dry_run = dry_run


    async def collect_images(self):
        start_message = ('DRY RUN: Starting distribution process simulation'
            if self.dry_run
            else 'Starting distribution process')

        logging.info(start_message)
        
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
        return list(zip(days_to_fill, images_batches))
