import logging
import asyncio
import argparse
import os

from config.settings import Settings, ConfigError
from logic.collector import Collector, AppException
from tg_local.tg_poster import TelegramPoster
from logic.poster import Poster

def parse_args():
    parser = argparse.ArgumentParser(description='Telegram Channel Media Poster')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Run in dry run mode (no actual file operations or Telegram posting)')
    return parser.parse_args()

async def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

    if args.dry_run:
        logging.info('DRY RUN MODE ENABLED - No actual files will be moved or messages sent')

    try:
        settings = Settings.from_env(dry_run=args.dry_run)
    except ConfigError as ce:
        logging.error(f'Config error: {ce}')
        return

    try:
        collector = Collector(settings, args.dry_run)
        images_batch = await collector.collect_images()

        if args.dry_run:
            for (date, folder), batch in images_batch:
                logging.info(f'DRY RUN: Would move {len(batch)} files to folder: {folder}')
                logging.info(
                    f'DRY RUN: Would send scheduled images for {date.strftime("%Y-%m-%d")}: {[os.path.basename(f) for f in batch]}')
                logging.info(f'DRY RUN: Would mark day folder as closed: {folder}')

            logging.info('DRY RUN: Distribution process simulation completed')
            return

        tg_poster = TelegramPoster(
            settings.telegram.api_id,
            settings.telegram.api_hash,
            settings.telegram.phone
        )

        poster = Poster(settings.telegram.chat_id, tg_poster)
        await poster.process_batch(images_batch)

        logging.info('Distribution process completed')

    except AppException as ae:
        logging.error(f'App error: {ae}')
    except Exception as e:
        logging.exception(f'Unhandled error: {e}')

if __name__ == '__main__':
    asyncio.run(main()) 