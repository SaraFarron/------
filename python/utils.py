from ftplib import FTP_TLS
from pathlib import Path
from os import remove, listdir, path, getcwd
import unlzw3
import json
import gzip
import shutil

HOST = 'gdc.cddis.eosdis.nasa.gov'
USER = 'anonymous'
PASSWORD = 'jiperscreepers@gmail.com'
EMAIL = PASSWORD


# def unarchive_z(filename: str):
#     uncompressed_data = unlzw3.unlzw(Path(filename)).decode()
#     with open('python_sp3_files/' + filename[:-2], 'w') as f:
#         f.write(uncompressed_data)
#     remove(filename)
#     print(f'{filename} successfully downloaded')


# def unarchive_gz(filename: str):
#     with gzip.open(filename, 'rb') as f_in:
#         with open('python_rinex_files/' + filename[:-3], 'wb') as f_out:
#             shutil.copyfileobj(f_in, f_out)
#     remove(filename)
#     print(f'{filename} successfully downloaded')


# def download_sp3_file(filename: str, ftp_dir: str) -> None:
#     """
#         Connects to ftp_dir, downloads filename, unarchives, puts in python_sp3_files,
#         works only with sp3.Z and sp3.gz
#     """
#     if filename[:-2] not in listdir(getcwd() + '/python_sp3_files/') and filename[:-3] not in listdir(getcwd() + '/python_rinex_files/'):
#         email = 'jiperscreepers@gmail.com'

#         if filename not in listdir(path.abspath(getcwd())):
#             ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
#             ftps.login(user='anonymous', passwd=email)
#             ftps.prot_p()
#             ftps.cwd(ftp_dir)
#             ftps.retrbinary("RETR " + filename, open(filename, 'wb').write)
#         else:
#             print('archive is already in directory')

#         match filename[-2:]:
#             case '.Z': unarchive_z(filename)
#             case 'gz': unarchive_gz(filename)
#             case _: raise f'Unknown format {filename[-2:]}'
        
#     else:
#         print('file is already in directory')
    

# def get_ftp_dir(dir: str) -> list[str, ]:
#     """
#         Returns a list of files from dir in ftp
#     """
#     email = 'jiperscreepers@gmail.com'
#     ftps = FTP_TLS(host=HOST)
#     ftps.login(user=USER, passwd=PASSWORD)
#     ftps.prot_p()
#     ftps.cwd(dir)
#     return ftps.nlst()


# def read_sp3_file_date(filename: str, dir: str | None = None) -> str:
#     """
#         Read an sp3 file and returns date of observation
#     """
#     if dir:
#         with open(dir + filename, 'r') as f:
#             sp3_date = f.readline(23)
#     else:
#         with open(filename, 'r') as f:
#             sp3_date = f.readline(23)
#     return sp3_date[3:15]


# def read_rinex_file_datetime(filename: str, dir: str | None = None) -> str:
#     if dir:
#         with open(dir + filename, 'r') as f:
#             rinex_date = f.readlines()[1][:-1]
#     else:
#         with open(filename, 'r') as f:
#             rinex_date = f.readlines()[1][:-1]
#     return rinex_date[40:56]


# def get_sp3_files():
#     products_dir_path = '/pub/gps/products/'
#     products_dir = []
#     with open('folders.txt', 'r') as fp:
#         for line in fp.readlines()[:-15:-1]:
#             products_dir.append(line[:-1])

#     for folder in products_dir[::-1]:
#         print(f'reading {folder}')
#         folder_path = products_dir_path + folder + '/'
#         folder_contents = get_ftp_dir(folder_path)
#         sp3_files = [x for x in folder_contents if x[-5:] == 'sp3.Z']
#         sp3_files_and_dates = {}

#         for sp3 in sp3_files:
#             print(f'downloading {sp3}')
#             download_sp3_file(sp3, folder_path)
#             print(f'reading {sp3}')
#             sp3_files_and_dates[sp3] = read_sp3_file_date(sp3[:-2], 'python_sp3_files/')
#             print('success')

#         with open('files.json', 'a') as f:
#             json.dump(sp3_files_and_dates, f)


# def get_rinex_files(start: str, end: str):
#     """
#         start is starting day
#         end is ending day
#     """
#     rinex_folders_path = '/pub/gnss/data/daily/2017/' 
#     dirs = get_ftp_dir(rinex_folders_path)
#     if start and end:
#         start_index = dirs.index(start)
#         end_index = dirs.index(end)
#         dirs = dirs[start_index:end_index]
        
#     for folder in dirs:
#         print(f'reading {folder}')
#         folder_path = rinex_folders_path + folder + '/17l/'
#         folder_contents = get_ftp_dir(folder_path)
#         rinex_files = [x for x in folder_contents if x[-6:] == 'rnx.gz']
#         rinex_files_and_datetimes = {}

#         for rinex in rinex_files:
#             print(f'downloading {rinex}')
#             download_sp3_file(rinex, folder_path)
#             print(f'reading {rinex}')
#             rinex_files_and_datetimes[rinex] = read_rinex_file_datetime(rinex[:-3], 'python_rinex_files/')
#             print('success')
        
#         with open('rinex_files.json', 'a') as f:
#             json.dump(rinex_files_and_datetimes, f)


# if __name__ == '__main__':
    # get_sp3_files()
    # get_rinex_files('190', '195')
    # print(get_ftp_dir('/pub/gps/data/daily/2019/190/19l/'))


def unpack_z_file(filename: str) -> None:
    """
        Unarchives .Z file
    """
    uncompressed_data = unlzw3.unlzw(Path(filename)).decode()
    with open(filename[:-2], 'w') as f:
        f.write(uncompressed_data)

    remove(filename)
    print(f'{filename} unpacked')


def unpack_gz_file(filename: str) -> None:
    """
        Unarchives .gz file
    """
    with gzip.open(filename, 'rb') as f_in:
        with open(filename[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    remove(filename)
    print(f'{filename} unpacked')


def download_file_ftp(dir: str, filename: str, target_dir: str | None = None) -> None:
    """
        Connects to dir, downloads filename, puts in target_dir
    """
    if filename in listdir(getcwd() + dir):
        print(f'{filename} already present')
        return
    
    if target_dir[-1] != '/':
        target_dir += '/'

    ftps = FTP_TLS(host=HOST)
    ftps.login(user=USER, passwd=PASSWORD)
    ftps.prot_p()
    ftps.cwd(dir)
    ftps.retrbinary("RETR " + filename, open(target_dir + filename, 'wb').write)

    print(f'{filename} downloaded')


def ftp_login() -> FTP_TLS:
    ftps = FTP_TLS(host=HOST)
    ftps.login(user=USER, passwd=PASSWORD)
    return ftps


def ftp_cwd(ftps: FTP_TLS | None) -> FTP_TLS:
    if not ftps:
        ftps = ftp_login()
    ftps.prot_p()
    ftps.cwd(dir)
    return ftps


def get_directory_ftp(dir: str, ftps: FTP_TLS | None) -> list[str, ]: 
    """
        Returns a list of files from dir in ftp
    """
    if not ftps:
        ftps = ftp_cwd(dir)
    ftps = ftp_cwd(dir, ftps)

    return ftps.nlst()


def get_dir_with_data(dir: str, ftps: FTP_TLS | None) -> list[str, ]:
    """
        Returns full infor about directory
    """
    if not ftps:
        ftps = ftp_cwd(dir)
    ftps = ftp_cwd(dir, ftps)

    return ftps.retrlines('LIST')


def read_file(filename: str, line: int, start: int | None = 0, end: int | None = -1) -> str:
    """
        Reads a line from start to end character from file and returns line
    """
    with open(filename, 'r') as f:
        result = f.readline(line)

    return result[start:end]


def filter_by_format(files: list[str, ], format: str): 
    return [file for file in files if file.endswith(format)]
