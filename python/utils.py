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


def unpack_z_file(filename: str) -> str:
    """
        Unarchives .Z file, returns new file name
    """
    if not filename.endswith('.Z'):
        print('wrong file format, not Z')
        return

    new_name = filename[:-2]
    if path.exists(new_name):
        print(f'{new_name} already exists')
        remove(filename)
        return new_name

    uncompressed_data = unlzw3.unlzw(Path(filename)).decode()
    with open(new_name, 'w') as f:
        f.write(uncompressed_data)

    remove(filename)
    print(f'{filename} unpacked')
    return new_name


def unpack_gz_file(filename: str) -> str:
    """
        Unarchives .gz file, returns new file name
    """
    if not filename.endswith('.gz'):
        print('wrong file format, not gz')
        return
    
    new_name = filename[:-3]
    if path.exists(new_name):
        print(f'{new_name} already exists')
        remove(filename)
        return new_name

    with gzip.open(filename, 'rb') as f_in:
        with open(new_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    remove(filename)
    print(f'{filename} unpacked')
    return new_name


def download_file_ftp(dir: str, filename: str, 
                      target_dir: str | None = None, 
                      ftps: FTP_TLS | None = None) -> None:
    """
        Connects to dir, downloads filename, puts in target_dir
    """
    if target_dir[-1] != '/':
        target_dir += '/'

    if filename in listdir(getcwd() + '/' + target_dir):
        print(f'{filename} already present')
        return

    if not ftps:
        ftps = FTP_TLS(host=HOST)
        ftps.login(user=USER, passwd=PASSWORD)
        ftps.prot_p()
    ftps.cwd(dir)
    ftps.retrbinary("RETR " + filename, open(target_dir + filename, 'wb').write)

    print(f'{filename} downloaded')


def ftp_login() -> FTP_TLS:
    ftps = FTP_TLS(host=HOST)
    ftps.login(user=USER, passwd=PASSWORD)
    ftps.prot_p()
    return ftps


def ftp_cwd(dir: str, ftps: FTP_TLS | None = None) -> FTP_TLS:
    if not ftps:
        ftps = ftp_login()
        ftps.prot_p()
    ftps.cwd(dir)
    return ftps


def get_directory_ftp(dir: str, ftps: FTP_TLS | None = None) -> list[str, ]: 
    """
        Returns a list of files from dir in ftp
    """
    if not ftps:
        ftps = ftp_cwd(dir)
        ftps.prot_p()
    ftps = ftp_cwd(dir, ftps)

    return ftps.nlst()


def get_dir_with_data(dir: str, ftps: FTP_TLS | None) -> list[str, ]:
    """
        Returns full infor about directory
    """
    if not ftps:
        ftps = ftp_cwd(dir)
        ftps.prot_p()
    ftps = ftp_cwd(dir, ftps)

    return ftps.retrlines('LIST')


def read_file(filename: str, line: int, start: int | None = 0, end: int | None = -1) -> str:
    """
        Reads a line from start to end character from file and returns line
    """
    with open(filename, 'r') as f:
        for l in range(line):
            f.readline()
            if l + 1 == line:
                result = f.readline()

    return result[start:end]


def filter_by_format(files: list[str, ], format: str): 
    return [file for file in files if file.endswith(format)]

