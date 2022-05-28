from ftplib import FTP_TLS
from pathlib import Path
from os import remove, listdir, path, getcwd, makedirs
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
    print('login successful')
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
    result = ''
    with open(filename, 'r') as f:
        for l in range(line):
            try:
                f.readline()
            except UnicodeDecodeError:
                print(f'decode error in file {filename}')
                return
            if l + 1 == line:
                result = f.readline()

    return result[start:end]


def filter_by_format(files: list[str, ], format: str): 
    return [file for file in files if file.endswith(format)]


def coordinates_parser(string: str) -> list[float, float, float]:
    res = [x for x in string.split(' ') if x != '']
    res = [x.replace('D', 'E') for x in res]

    cords = []
    for x in res:
        try:
            cords.append(float(x))
        except ValueError:
            continue

    if len(cords) == 3:
        print('Cords parsed successfully')
        return cords

    print(f'error parse cords {cords}')
    return


def ionosphere_parser(string: str) -> list[float, float, float]:
    res = [x for x in string.split(' ') if x != '']
    res = [x.replace('D', 'E') for x in res]

    try:
        if res[0] != 'GAL':
            print('wrong data')
            return
    except IndexError:
        print('error parse i8e')
        return
    
    a_coefs = []
    for x in res[1:]:
        try:
            a_coefs.append(float(x))
        except ValueError:
            continue
    
    if len(a_coefs) == 4:
        print('Ionosphere coefs parsed successfully')
        return a_coefs[:-1]
    
    print(f'error parse coefs {a_coefs}')
    return


def get_files_from_ftp_dir(dir: str, 
                           target_root: str, 
                           ftp_root: str, 
                           format: str, 
                           archive: str | None = None, 
                           ftps: FTP_TLS | None = None) -> None:
    """
        Downloads all files from provided ftp directory, format example: '.rnx', archive example: '.gz'
    """
    if not ftps:
        ftps = ftp_login()

    current_dir = ftp_root + dir
    host_dir = target_root + dir
    ftps = ftp_cwd(current_dir, ftps)
    try:
        makedirs(host_dir)
    except FileExistsError:
        print(f'{dir} already exists')

    print(f'getting all {format} files from {dir}')

    files = get_directory_ftp(current_dir, ftps)
    files = [f for f in files if f.endswith(format + archive) and not path.exists(host_dir + f[:-len(archive)])]
    for file in files:
        download_file_ftp(current_dir, file, host_dir)
        filename = host_dir + file
        if archive == '.gz':
            filename = unpack_gz_file(filename)
        elif archive == '.Z':
            filename = unpack_z_file(filename)
        else:
            print('File is not archived of unknown archive format')

    print(f'{dir} downloaded successfully')
