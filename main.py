import logging
import asyncio
import argparse
from config.settings import Settings, ConfigError
from logic.distributor import Distributor, AppException
from tg_local.tg_poster import TelegramPoster

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
    try:
        settings = Settings.from_env(dry_run=args.dry_run)
    except ConfigError as ce:
        logging.error(f'Config error: {ce}')
        return
    
    if args.dry_run:
        logging.info('DRY RUN MODE ENABLED - No actual files will be moved or messages sent')
        tg_poster = None
    else:
        tg_poster = TelegramPoster(
            settings.telegram.api_id,
            settings.telegram.api_hash,
            settings.telegram.phone
        )
        # await tg_poster
    
    try:
        distributor = Distributor(settings, tg_poster, args.dry_run)
        await distributor.run()
    except AppException as ae:
        logging.error(f'App error: {ae}')
    except Exception as e:
        logging.exception(f'Unhandled error: {e}')

if __name__ == '__main__':
    asyncio.run(main()) 