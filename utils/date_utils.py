from datetime import datetime, timedelta
from typing import Tuple

def folder_to_date(year: str, month: str, day: str) -> datetime:
    return datetime(int(year), int(month.lstrip('_')), int(day.lstrip('_')))

def date_to_folder(date: datetime) -> Tuple[str, str, str]:
    return str(date.year), f"{date.month:02d}", f"{date.day:02d}"

def get_next_day(date: datetime) -> datetime:
    return date + timedelta(days=1) 