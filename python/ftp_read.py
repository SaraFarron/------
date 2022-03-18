from ftplib import FTP_TLS

# FTP params
EMAIL = 'jiperscreepers@gmail.com'
DIR = '/pub/gps/products/'
FILENAME = 'zim20010.21g.gz'

# FTP stuff
ftps = FTP_TLS(host = 'gdc.cddis.eosdis.nasa.gov')
ftps.login(user='anonymous', passwd=EMAIL)
ftps.prot_p()
ftps.cwd(DIR)
dir = ftps.nlst()

# file writing
with open('folders.txt', 'w') as f:
    for folder in dir:
        try:
            int(folder)
            f.write(folder + '\n')
        except ValueError:
            continue


def read_sp3_file(filename: str, dir: str | None = None) -> str:
    """
        Read an sp3 file and returns date of observation
    """
    if dir:
        with open(dir + filename, 'r') as f:
            sp3_date = f.readline(23)
    else:
        with open(filename, 'r') as f:
            sp3_date = f.readline(23)
    return sp3_date[3:15]
