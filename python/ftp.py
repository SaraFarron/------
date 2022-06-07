from os import makedirs, path
import json

from experiment import *
from utils import *

RINEX_FILES_DIRS = [
    'gnss/data/daily/2017/191/17l/',
    'gnss/data/daily/2017/192/17l/',
    'gnss/data/daily/2017/193/17l/',
    'gnss/data/daily/2017/194/17l/',
]
SP3_FILES_DIRS = [
    'gnss/products/2085/',
    'gnss/products/2086/',
    'gnss/products/2087/',
    'gnss/products/2088/',
    'gnss/products/2089/',
]
OBS_FILES_DIRS = [
    'gnss/data/daily/2020/001/20o/',
]


def get_rinex_files():
    path_prefix, ftp_path_prefix = 'ftp_data/', '/pub/'
    ftps = ftp_login()

    for DIR in RINEX_FILES_DIRS:
        get_files_from_ftp_dir(DIR, path_prefix, ftp_path_prefix, '.rnx', '.gz', ftps)

    ftps.quit()


def check_rinex_file(filename: str) -> None:
    file_no_path = filename[54:]
    i8e_data = read_file(filename, 3, 0, 3)
    cords_data = read_file(filename, 9, 60, 69)
    if i8e_data == 'GAL' and cords_data == 'COMMENT':
        print(f'{file_no_path} is valid')
        json_data = {file_no_path: {'i8e': i8e_data, 'cords': cords_data}}
        with open('rinex_data.json', 'a') as f:
            json.dump(json_data, f)
        return
    # print(f'{file_no_path} is invalid')
    print(f'GAL-{i8e_data}|COMMENT-{cords_data}')


def get_sp3_files():
    path_prefix, ftp_path_prefix = 'ftp_data/', '/pub/'
    ftps = ftp_login()

    for DIR in SP3_FILES_DIRS:
        get_files_from_ftp_dir(DIR, path_prefix, ftp_path_prefix, '.sp3', '.Z', ftps)

    ftps.quit()


def get_obs_files():
    path_prefix, ftp_path_prefix = 'ftp_data/', '/pub/'
    ftps = ftp_login()

    for DIR in OBS_FILES_DIRS:
        get_files_from_ftp_dir(DIR, path_prefix, ftp_path_prefix, '.20o', '.Z', ftps)

    ftps.quit()


def get_sp3_datetime():
    for file in listdir('python_sp3_files/'):
        datetime = read_file('python_sp3_files/' + file, 22, 3, 31)
        json_data = {file: datetime}
        with open('sp3_data.json', 'a') as f:
            json.dump(json_data, f)
        print(f'{file} has been parsed')


folders = ['191', '192', '193', '194', ]
for folder in folders:
    dir = getcwd() + '/ftp_data/' + 'gnss/data/daily/2017/' + folder + '/17l/'
    for file in listdir(dir):
        check_rinex_file(dir + file)

# get_rinex_files()

