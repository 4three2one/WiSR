import os
import glob
import random
import re
import shutil


def copy_remaining_files(remaining_files, destination_dir):
    for file_path in remaining_files:
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(destination_dir, file_name)
        if not os.path.exists(destination_path):
            shutil.copy(file_path, destination_path)
        else:
            print("已经存在",destination_path)


def copy_random_files(remaining_files, destination_dir):
    for file_path in remaining_files:
        file_name = os.path.basename(file_path)
        match = re.search(r'user_(\d+)', file_name)
        if match:
            user_id = match.group(1)
        match = re.search(r'rep_(\d+)', file_name)
        if match:
            rep_id = match.group(1)

        file_name = re.sub(r'user_\d+', 'user_x', file_name)

        file_name = re.sub(r'rep_\d+', f'rep_{user_id}{rep_id}', file_name)
        destination_path = os.path.join(destination_dir, file_name)
        if not os.path.exists(destination_path):
            shutil.copy(file_path, destination_path)
        else:
            print("已经存在", destination_path)


def select_random_files(file_list, n):
    random_files = random.sample(file_list, n)
    return random_files


root_dir=r"E:\wifi\WiSR\Widar3\CSI"

output_dir=r"E:\wifi\WiSR\Widar3\CSI\matfile_man"


user_ids=['1','2','3']
ori_ids=['1','2','3','4','5']
loc_ids=['1','2','3','4','5']
rx_ids=['1','2','3','4','5','6']
ges_ids = ["Push&Pull", "Sweep", "Clap", "Slide", "Draw-Zigzag(Vertical)", "Draw-N(Vertical)"]


room='1'
i=0
for user in user_ids:
    for ori in ori_ids:
        for loc in loc_ids:
            for ges in ges_ids:
                for rx in rx_ids:
                    mat_file_name_pattern = 'room_' + room + '_user_' + user + '_ges_' + ges + '_loc_' + loc + '_ori_' + ori + '_rx_' + rx + '*_csi.mat'
                    mat_files = glob.glob(
                        os.path.join(root_dir, f"matfile_ours", mat_file_name_pattern))
                    print("处理",mat_file_name_pattern)
                    random_files=select_random_files(mat_files, 4)
                    remaining_files = [file for file in mat_files if file not in random_files]
                    copy_remaining_files(remaining_files,output_dir)
                    copy_random_files(random_files,output_dir)
                    pass
print(i)
