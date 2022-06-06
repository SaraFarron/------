from os import listdir, remove, system
from datetime import datetime
from math import sqrt, asin, pi

from utils import *
from xyz_to_blh import xyz_to_blh, xyz2blh_gost

RINEX = 'ftp_data/gnss/data/daily/2020/001/20l/ABPO00MDG_R_20200010000_01D_EN.rnx'
SP3 = 'PPPH/PPPH/Example/gbm19571.sp3'


def main():
    print('reading rnx')

    # Get ionospheric coefficients
    gal = read_file(RINEX, 2, 7, 41).split(' ')
    a0, a1, a2 = [float(x) for x in gal if x]

    # Get station coordinates
    station_cords = read_file(RINEX, 8, 2, 42).split(' ')
    station_cords = [float(x) for x in station_cords if x]
    x, y, z = xyz_to_blh(*station_cords)

    # Get date
    date = read_file(RINEX, 1, 41, 48)
    year, month, day = date[:4], date[4:6], date[6:]

    print('writing stdin.txt\n reading sp3')
    with open('stdin.txt', 'w') as input_data:
        with open(SP3, 'r') as sp3:
            with open('psat_data.txt', 'r') as psat:
                print('checking dates')

                for line in sp3.readlines():
                    match line[0]:

                        # Get UT
                        case '*':
                            ut = line[15:32].split(' ')
                            h, m, s = [float(x) for x in ut if x]
                            ut = h + m / 60 + s / 3600
                            date = line[3:14].split(' ')
                            s_year, s_month, s_day = [x for x in date if x]
                            assert year == s_year and month == s_month and day == s_day, \
                                'dates does not match'
                        
                        # Get position
                        case 'P':
                            # This retreives coordinates straight from sp3, which is incorrect
                            # sat_cords = line[5:46].split(' ')
                            # sat_cords = [float(x) for x in sat_cords if x]
                            sat_cords = psat.readline().split(' ')
                            b, l, h = xyz_to_blh(*sat_cords)
                            rang = sqrt(
                                (sat_cords[0] - station_cords[0]) * (sat_cords[0] - station_cords[0]) + \
                                (sat_cords[1] - station_cords[1]) * (sat_cords[1] - station_cords[1]) + \
                                (sat_cords[2] - station_cords[2]) * (sat_cords[2] - station_cords[2])
                                )
                            kx = (sat_cords[0] - station_cords[0]) / rang
                            ky = (sat_cords[1] - station_cords[1]) / rang
                            kz = (sat_cords[2] - station_cords[2]) / rang
                            um = asin(
                                (kx * station_cords[0] + ky * station_cords[1] + kz * station_cords[2]) / \
                                sqrt(
                                    station_cords[0] * station_cords[0] + \
                                    station_cords[1] * station_cords[1] + \
                                    station_cords[2] * station_cords[2]
                                    )
                                ) * 180.0 / pi
                            assert um > 0, 'um is negative'

                        case _:
                            continue
                    input_data.write(f'{month} {ut} {x} {y} {z} {b} {l} {h}\n')
        
    print('running nequick')
    command = f'./сборка/NeQuickG_JRC_CCIR_MODIP_constants_UT_D.exe -f {a0} {a1} {a2} stdin.txt stdout.txt'
    print(system(command))
    print('finished')


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


def find_rinex():
    rinex_dir = 'ftp_data/gnss/data/daily/'

    for year in listdir(rinex_dir):
        dir_with_year = rinex_dir + year + '/'

        for d in listdir(dir_with_year):
            folder = year[-2:] + 'l'
            dir_with_d = dir_with_year + d + '/' + folder + '/'

            for file in listdir(dir_with_d):
                path = dir_with_d + file
                is_gal = read_file(path, 2, 0, 3)
                cords_comment = read_file(path, 8, 60, 67)

                if is_gal == 'GAL' and cords_comment == 'COMMENT':
                    gal = read_file(path, 2, 7, 41)
                    cords = read_file(path, 8, 2, 42)
                    cords = cords.split(' ')
                    cords = [x for x in cords if x]

                    date = read_file(path, 1, 41, 48)
                    year, month, day = date[:4], date[4:6], date[6:]

                    if year == '2017' and month == '7' and day == '10':
                        print(path)
                        return

                    print(f'{file} does not match')

                else:
                    print(f'file {file} is wrong: gal: {gal} cords comment: {cords_comment}')


if __name__ == '__main__':
    start = datetime.now()
    # main()
    # find_rinex()
    end = datetime.now()
    time = end - start
    print(f'execution time {time.microseconds / 1000}ms')
