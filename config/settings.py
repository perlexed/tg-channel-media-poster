import os
from dotenv import load_dotenv
from dataclasses import dataclass

class ConfigError(Exception):
    pass

@dataclass
class TelegramSettings:
    api_id: str
    api_hash: str
    phone: str
    chat_id: str

@dataclass
class Settings:
    days_to_fill_count: int
    source_folder: str
    target_root_folder: str
    batch_size: int
    telegram: TelegramSettings

    @staticmethod
    def from_env(dry_run: bool = False) -> 'Settings':
        load_dotenv()
        raw = _load_env_raw()
        _validate_env_raw(raw, dry_run=dry_run)
        return Settings(
            days_to_fill_count=int(raw['days_to_fill_count']),
            source_folder=raw['source_folder'],
            target_root_folder=raw['target_root_folder'],
            batch_size=int(raw['batch_size']),
            telegram=TelegramSettings(
                api_id=raw['telegram_api_id'],
                api_hash=raw['telegram_api_hash'],
                phone=raw['telegram_phone'],
                chat_id=raw['telegram_chat_id']
            )
        )

def _load_env_raw() -> dict:
    return {
        'days_to_fill_count': os.getenv('daysToFillCount'),
        'batch_size': os.getenv('batchSize'),
        'source_folder': os.getenv('sourceFolder'),
        'target_root_folder': os.getenv('targetRootFolder'),
        'telegram_api_id': os.getenv('TELEGRAM_API_ID'),
        'telegram_api_hash': os.getenv('TELEGRAM_API_HASH'),
        'telegram_phone': os.getenv('TELEGRAM_PHONE'),
        'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID'),
    }

def _validate_telegram_settings(raw: dict):
    if not raw['telegram_api_id']:
        raise ConfigError('TELEGRAM_API_ID must be set')
    if not raw['telegram_api_hash']:
        raise ConfigError('TELEGRAM_API_HASH must be set')
    if not raw['telegram_phone']:
        raise ConfigError('TELEGRAM_PHONE must be set')
    if not raw['telegram_chat_id']:
        raise ConfigError('TELEGRAM_CHAT_ID must be set')

def _validate_env_raw(raw: dict, dry_run: bool = False):
    if raw['days_to_fill_count'] is None or not raw['days_to_fill_count'].isdigit() or int(raw['days_to_fill_count']) <= 0:
        raise ConfigError('daysToFillCount must be a positive integer')
    if raw['batch_size'] is None or not raw['batch_size'].isdigit() or int(raw['batch_size']) <= 0:
        raise ConfigError('batchSize must be a positive integer')
    if not raw['source_folder'] or not os.path.isdir(raw['source_folder']):
        raise ConfigError('sourceFolder must be a valid directory')
    if not raw['target_root_folder'] or not os.path.isdir(raw['target_root_folder']):
        raise ConfigError('targetRootFolder must be a valid directory')
    if not dry_run:
        _validate_telegram_settings(raw) 