from cProfile import label
from os import listdir, system
from datetime import datetime
from math import sqrt, asin, pi
from matplotlib import pyplot as plt

from utils import *
from xyz_to_blh import xyz_to_blh, xyz2blh_gost

RINEX = 'ftp_data/gnss/data/daily/2020/001/20l/CHPI00BRA_R_20200010000_01D_EN.rnx'
SP3 = 'ftp_data/gnss/products/2086/igs20864.sp3'


def main():
    print('reading rnx')

    # Get ionospheric coefficients
    gal = read_file(RINEX, 2, 7, 41).replace('D', 'e').split(' ')
    a0, a1, a2 = [float(x) for x in gal if x]

    # Get station coordinates
    station_cords = read_file(RINEX, 8, 2, 42).split(' ')
    station_cords = [float(x) for x in station_cords if x]
    x, y, z = xyz_to_blh(*station_cords)

    # Get date
    date = read_file(RINEX, 1, 40, 48)
    year, month, day = map(int, [date[:4], date[4:6], date[6:]])

    print('writing stdin.txt\n reading sp3')
    with open('сборка/stdin.txt', 'w') as input_data:
        with open(SP3, 'r') as sp3:
            with open('major_data.txt', 'r') as psat:
                print('checking dates')

                for line in sp3.readlines():
                    match line[0]:

                        # Get UT
                        case '*':
                            ut = line[14:32].split(' ')
                            h, m, s = [float(x) for x in ut if x]
                            ut = h + m / 60 + s / 3600
                            date = line[3:14].split(' ')
                            s_year, s_month, s_day = [int(x) for x in date if x]
                            continue
                        
                        # Get position
                        case 'P':
                            print('checking um')
                            sat_cords = psat.readline().split(' ')
                            sat_cords = [float(x) for x in sat_cords if x]
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
                            if um <= 0:
                                print(f'skipping - um is negative ({um})')
                                continue

                        case _:
                            continue
                    input_data.write(f'{month} {ut} {y} {x} {z} {l} {b} {h}\n')
        
    print('running nequick')
    path_prefix = "C:\Универ\диплом\сборка/"
    nq_path = path_prefix + "NeQuickG_JRC_CCIR_MODIP_constants_UT_D.exe"
    stdin_path = path_prefix + 'stdin.txt'
    stdout_path = path_prefix + 'stdout.txt'
    command = f'{nq_path} -f {a0} {a1} {a2} {stdin_path} {stdout_path}'
    print(system(command))
    print('nequick finished')


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


def get_data_from_major():
    with open('NeQk/almanach/GLO_CRD_ALM_14_step001sec.csv', 'r') as f:
        with open('major_data.txt', 'w') as m:
            for line in f.readlines():
                data = line.split(' ')
                m.write(f'{data[1]} {data[2]} {data[3]}\n')
    print('finished extracting majors data')


def real_delay():
    satellite = 'G03'
    with open('PPPH/PPPH/Example/ISTA00TUR_R_20171910000_01D_30S_MO.00o', 'r') as f:
        with open('pseudo.txt', 'w') as o:
            for l in f.readlines():
                if l[:3] == '> 2' or l[:3] == satellite:
                    o.write(l)

    t, y = [], []
    fL1, fL2 = 1575.42e6, 1227.6e6
    I = lambda pL1, pL2: fL2 ** 2 / (fL1 ** 2 - fL2 ** 2) * (pL2 - pL1)

    with open('pseudo.txt', 'r') as f:
        lines = f.readlines()
        for i, l in enumerate(lines):
            try:
                next_l = lines[i+1]
            except IndexError:
                break

            if l[:3] == '> 2' and next_l[:3] == satellite:
                ut = l[13:29].split(' ')
                h, m, s = [float(x) for x in ut if x] 
                ut = h + m / 60 + s / 3600
                t.append(ut)

                pL1 = next_l[5:17]
                pL2 = next_l[21:33]
                d = I(float(pL1), float(pL2))
                y.append(d)
    
    return t, y


def create_tec_plot(x, y):
    l1, l2 = 1575e6, 1227e6
    t, nq = [], []
    d = lambda tec: tec * 1e16 * 40.3 / l1 ** 2
    with open('сборка/stdout.txt', 'r') as f:
        lines = f.readlines()
        if not lines:
            print('no data')
            return
            
        for l in lines:
            h = float(l[8:18].replace(' ', ''))
            t.append(h)
            n = float(l[120:].replace(' ', ''))
            nq.append(d(n))
        nqa = [*nq]
        for _ in range(int(len(nqa) * 24 / 7)):
            nqa.append(nqa[0])
            nqa.pop(0)

    t, nqa = t[2200:], nqa[2200:]
    x, y = x[60:], y[60:]

    length = 15
    average = []
    x_av = []
    for i in range(2, len(y), length):
        average.append(
            sum([x for x in y[i-length+1:i]]) / length
        )
        x_av.append(x[i])

    average[0] += 1.9

    plt.plot(t, nqa, label='NeQuick')
    plt.plot(x, y, 'o', label='Спутник', markersize=1)
    plt.plot(x_av, average, label='Экстраполяция')
    plt.xlabel('Местное время, ч')
    plt.ylabel('Ионосферная задержка, м')
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == '__main__':
    start = datetime.now()
    get_data_from_major()
    main()
    create_tec_plot(*real_delay())
    end = datetime.now()
    time = end - start
    print(f'execution time {time.microseconds / 1000}ms')
