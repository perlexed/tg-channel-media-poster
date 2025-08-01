import os
from typing import Optional, Tuple

FOLDER_CLOSE_SYMBOL = '_'

class FolderUtils:
    @staticmethod
    def find_last_closed_day(target_root_folder: str) -> Optional[Tuple[str, str, str]]:
        """
        Find the last closed day folder in the target root folder.
        Returns (year, month, day) as strings, or None if not found.
        """
        years = sorted([d for d in os.listdir(target_root_folder) if os.path.isdir(os.path.join(target_root_folder, d))])
        last = None
        for year in years:
            year_path = os.path.join(target_root_folder, year)
            months = sorted([m for m in os.listdir(year_path) if os.path.isdir(os.path.join(year_path, m))])
            for month in months:
                month_path = os.path.join(year_path, month)
                days = sorted([d for d in os.listdir(month_path) if os.path.isdir(os.path.join(month_path, d))])
                for day in days:
                    if day.endswith(FOLDER_CLOSE_SYMBOL):
                        last = (year, month, day)
        return last

    @staticmethod
    def create_day_folder(target_root_folder: str, year: str, month: str, day: str) -> str:
        """
        Create a folder for the given day if it does not exist.
        Returns the path to the created/existing folder.
        """
        path = os.path.join(target_root_folder, year, month, day)
        os.makedirs(path, exist_ok=True)
        return path

    @staticmethod
    def mark_day_folder_closed(day_folder_path: str):
        """
        Mark the day as closed by renaming the folder to end with FOLDER_CLOSE_SYMBOL.
        """
        base = os.path.basename(day_folder_path)
        if not base.endswith(FOLDER_CLOSE_SYMBOL):
            new_base = base + FOLDER_CLOSE_SYMBOL
            new_path = os.path.join(os.path.dirname(day_folder_path), new_base)
            os.rename(day_folder_path, new_path)
            return new_path
        return day_folder_path 