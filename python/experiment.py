from os import listdir
from utils import read_file
from xyz_to_blh import xyz_to_blh, xyz2blh_gost


def main():
    """
    1. Parse rinex, get date and time
    2. Parse all sp3s, get date and time and compare with rinex's - if it ~= - take data,
    if not - next one
    3. Create txt file with data needed for nequick, get a0, a1 and a2, transform xyz to blh
    3.1. (Optional) Check differenct in final results between gost blh and internet one
    4. Run nequick
    5. (Optional) After nequick finishes - create a plot
    """

    rinex_dir = 'ftp_data/gnss/data/daily/'
    sp3_dir = 'ftp_data/gnss/products/'

    for year in listdir(rinex_dir):
        for d in year:
            folder = year[-2:] + 'l'
            for file in folder:
                path = rinex_dir + year + '/' + d + '/' + file
                date_time = read_file(path, 2, 41, 56)
                date, time = date_time.split(' ')

if __name__ == '__main__':
    main()
