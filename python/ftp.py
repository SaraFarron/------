from os import makedirs, path

from utils import *

RINEX_FILES_DIRS = [
    'gnss/data/daily/2020/001/20l/',
    'gnss/data/daily/2020/001/20h/',
    'gnss/data/daily/2020/001/20g/',
    'gnss/data/daily/2020/001/20f/',
]


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


# dir = getcwd() + '/ftp_data/' + 'gnss/data/daily/2020/001/20l/'
# for file in listdir(dir):
#     check_rinex_file(dir + file)

# get_rinex_files()


def get_sp3_datetime():
    for file in listdir('python_sp3_files/'):
        datetime = read_file('python_sp3_files/' + file, 22, 3, 31)
        json_data = {file: datetime}
        with open('sp3_data.json', 'a') as f:
            json.dump(json_data, f)
        print(f'{file} has been parsed')


get_sp3_datetime()
