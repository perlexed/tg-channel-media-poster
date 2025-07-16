import os
import random
import shutil
from typing import List

class FileUtils:
    @staticmethod
    def get_image_files(source_folder: str) -> List[str]:
        """
        Get all image files from the source folder (non-recursive).
        """
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        files = []
        for filename in os.listdir(source_folder):
            if os.path.isfile(os.path.join(source_folder, filename)):
                if os.path.splitext(filename)[1].lower() in image_extensions:
                    files.append(os.path.join(source_folder, filename))
        return files

    @staticmethod
    def shuffle_and_split(files: List[str], batch_size: int) -> List[List[str]]:
        """
        Shuffle files and split into batches of specified size.
        """
        random.shuffle(files)
        
        batches = []
        num_batches = len(files) // batch_size
        
        for i in range(num_batches):
            start = i * batch_size
            end = start + batch_size
            batch = files[start:end]
            batches.append(batch)
        
        return batches

    @staticmethod
    def move_files_to_folder(files: List[str], target_folder: str):
        """
        Move files to the target folder.
        """
        for file in files:
            shutil.move(
                file,
                os.path.join(target_folder, os.path.basename(file)),
            ) 