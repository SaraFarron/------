from os import makedirs, path

from utils import *

RINEX_FILES_DIRS = [
    'gnss/data/daily/2020/001/20q/',
    'gnss/data/daily/2020/001/20p/',
    'gnss/data/daily/2020/001/20n/',
    'gnss/data/daily/2020/001/20m/',
    'gnss/data/daily/2020/001/20l/',
    'gnss/data/daily/2020/001/20h/',
    'gnss/data/daily/2020/001/20g/',
    'gnss/data/daily/2020/001/20f/',
]

"""
TODO check for cords + ionospheric coefs
"""

def get_rinex_files():
    path_prefix, ftp_path_prefix = 'ftp_data/', '/pub/'
    ftps = ftp_login()

    for DIR in RINEX_FILES_DIRS:
        current_dir = ftp_path_prefix + DIR
        host_dir = path_prefix + DIR
        ftps = ftp_cwd(current_dir, ftps)
        try:
            makedirs(host_dir)
        except FileExistsError:
            print(f'{DIR} already exists')

        files = get_directory_ftp(current_dir, ftps)
        files = [f for f in files if f.endswith('.rnx.gz') and not path.exists(host_dir + f[:-3])]
        for file in files:
            download_file_ftp(current_dir, file, host_dir)
            filename = host_dir + file
            filename = unpack_gz_file(filename)

    ftps.quit()


def check_rinex_files(filename: str):
    ionosphere_data = read_file(filename, 3, 0, 80)
    cords_data = read_file(filename, 9, 0, 68)
    json_data = {filename: {'ionoshpere': ionosphere_data, 'cords': cords_data}}
    with open('rinex_data.json', 'a') as f:
        json.dump(json_data, f)

get_rinex_files()
