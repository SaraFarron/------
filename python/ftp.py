from os import makedirs, path

from utils import *

RINEX_FILES_DIRS = [
    'gnss/data/daily/2017/191/20l/',
    'gnss/data/daily/2017/192/20l/',
    'gnss/data/daily/2017/193/20l/',
    'gnss/data/daily/2017/194/20l/',
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
    i8e_data = read_file(filename, 3, 0, 60)
    i8e_coefs = ionosphere_parser(i8e_data)
    cords_data = read_file(filename, 9, 0, 60)
    cords = coordinates_parser(cords_data)

    file_no_path = filename[54:]
    if i8e_coefs and cords:
        print(f'{file_no_path} has all data needed')
        json_data = {file_no_path: {'i8e': i8e_coefs, 'cords': cords}}
        with open('rinex_data.json', 'a') as f:
            json.dump(json_data, f)
        return

    print(f'{file_no_path} is bad')
    json_data = {file_no_path: {'ionoshpere': i8e_data, 'cords': cords_data}}
    with open('rinex_bad_data.json', 'a') as f:
        json.dump(json_data, f)


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


# dir = getcwd() + '/ftp_data/' + 'gnss/data/daily/2020/001/20l/'
# for file in listdir(dir):
#     check_rinex_file(dir + file)

get_rinex_files()
