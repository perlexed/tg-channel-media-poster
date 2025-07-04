import os.path
import shutil
import os
import random

source_dir = 'E:/p/_images'
existing_files_dir = 'E:/p/_images/__channel'
target_sort_dir = 'E:/p/_images/__channel'
# target_dir = './test_data/test2_two_files_available'
# target_dir = './test_data/test1_all_files_taken'


def get_target_dir_files_list(target_dir_path: str) -> list:
    files_list = []
    for dirpath, dirnames, filenames in os.walk(target_dir_path):
        if filenames:
            for filename in filenames:
                files_list.append(filename)

    return files_list


def get_not_used_files(all_files: list, used_files: list) -> list:
    not_used_files = []

    for source_file in all_files:
        if source_file not in used_files:
            not_used_files.append(source_file)

    return not_used_files


def get_random_files_pack(files: list, max_pack_size: int) -> list:
    random.shuffle(files)

    if max_pack_size >= len(files):
        return files

    return files[0:max_pack_size]


if __name__ == '__main__':
    source_files = os.listdir(source_dir)
    used_files = get_target_dir_files_list(existing_files_dir)
    not_used_files = get_not_used_files(source_files, used_files)

    print(f'found {len(not_used_files)} unused files')

    random_files_pack = get_random_files_pack(not_used_files, 30)

    for file_to_copy in random_files_pack:
        shutil.copy2(os.path.join(source_dir, file_to_copy), target_sort_dir)

    print(f'copied {len(random_files_pack)} random files to {target_sort_dir}')
