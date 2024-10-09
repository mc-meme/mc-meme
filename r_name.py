import os
import glob

import random


def rename_files_in_folder(folder_path):

    files = glob.glob(os.path.join(folder_path, '*'))


    files = [os.path.basename(f) for f in files]


    files.sort()
    random.shuffle(files)


    for index, file_name in enumerate(files):

        ext = os.path.splitext(file_name)[1]
        new_name = f"{index + 1}{ext}"


        old_file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(folder_path, new_name)


        os.rename(old_file_path, new_file_path)
        print(f'Renamed: {old_file_path} to {new_file_path}')



folder_path = 'zh_cn'
rename_files_in_folder(folder_path)
