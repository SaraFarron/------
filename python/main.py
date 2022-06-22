import os
from os import system
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib

from utils import *
from xyz_to_blh import xyz_to_blh

matplotlib.rcParams.update({'font.size': 17})
RINEX = 'ftp_data/gnss/data/daily/2020/001/20l/CHPI00BRA_R_20200010000_01D_EN.rnx'
SP3 = 'ftp_data/gnss/products/2086/igs20864.sp3'
OBS_RINEX = 'PPPH/Example/ISTA00TUR_R_20171910000_01D_30S_MO.00o'


def main(
        satellite: str,
        csv: str,
        rnx: str,
        sp3: str,
        obs: str,
        dpl1: float,
        average_length: int,
        nq_slice: list[int, int] | None = [0, -1],
        r2l_slice: list[int, int] | None = [0, -1]
):
    csv_file = f'NeQk/almanach/GLO_CRD_ALM_{csv}_step001sec.csv'

    np_rnx = os.path.normpath(rnx).split(os.sep)[-1][:-4]
    np_sp3 = os.path.normpath(sp3).split(os.sep)[-1][:-4]
    np_obs = os.path.normpath(obs).split(os.sep)[-1][:-2]
    np_csv = os.path.normpath(csv_file).split(os.sep)[-1][:-4]
    csv_out_file = f'db/out_{np_csv}.txt'
    nequick_delay_output = 'db/' + '-'.join(
        [csv, np_sp3, np_rnx]
    ) + '.txt'
    real_delay_output = 'db/' + '-'.join(
        [np_obs, str(dpl1)]
    ) + '.txt'

    print('reading rnx')
    # Get ionospheric coefficients
    gal = read_file(rnx, 2, 7, 41).replace('D', 'e').split(' ')
    a0, a1, a2 = [float(x) for x in gal if x]

    # Get station coordinates
    station_cords = read_file(rnx, 8, 2, 42).split(' ')
    station_cords = [float(x) for x in station_cords if x]
    x, y, z = xyz_to_blh(*station_cords)

    # Get date
    date = read_file(rnx, 1, 40, 48)
    year, month, day = map(int, [date[:4], date[4:6], date[6:]])

    if not file_exitsts(csv_out_file):
        run_nequick(sp3, csv_file, np_csv, [a0, a1, a2], station_cords, month, x, y, z)

    nq_time, nq_delay_adj = calc_nq_delay(csv_out_file)

    real_time, real_delay = calc_real_delay(obs, satellite, dpl1)

    print('creating plots')

    nq_time, nq_delay_adj = nq_time[nq_slice[0]:nq_slice[1]], nq_delay_adj[nq_slice[0]:nq_slice[1]]
    real_time, real_delay = real_time[r2l_slice[0]:r2l_slice[1]], real_delay[r2l_slice[0]:r2l_slice[1]]
    average_delay, average_time = [], []

    for i in range(2, len(real_delay), average_length):
        average_delay.append(
            sum([x for x in real_delay[i - average_length + 1:i]]) / average_length
        )
        average_time.append(real_time[i])

    average_delay[0] = real_delay[0]

    plt.plot(nq_time, nq_delay_adj, label='NeQuick')
    plt.plot(real_time, real_delay, 'o', label='Спутник', markersize=1)
    plt.plot(average_time, average_delay, label='Усреднение')
    plt.xlabel('Местное время, ч')
    plt.ylabel('Ионосферная задержка, м')
    plt.grid()
    plt.legend()
    plt.show()


def run_nequick(sp3, csv_file, np_csv, a: list[str, str, str], station_cords, month, x, y, z):
    print('writing stdin.txt\n reading sp3')
    with open('сборка/stdin.txt', 'w') as input_data:
        with open(sp3, 'r') as sp3_file:
            with open(csv_file, 'r') as psat:
                for line in sp3_file.readlines():
                    match line[0]:

                        # Get UT
                        case '*':
                            ut = line[14:32].split(' ')
                            h, m, s = [float(x) for x in ut if x]
                            ut = h + m / 60 + s / 3600
                            date = line[3:14].split(' ')
                            continue

                        # Get position
                        case 'P':
                            sat_cords = psat.readline().split(' ')
                            sat_cords = [sat_cords[1], sat_cords[2], sat_cords[3]]
                            sat_cords = list(map(float, sat_cords))

                            print('checking um')
                            um = calc_um(sat_cords, station_cords)
                            if um <= 0:
                                print(f'skipping - um is negative ({um})')
                                continue
                            b, l, h = xyz_to_blh(*sat_cords)

                        case _:
                            continue
                    input_data.write(f'{month} {ut} {y} {x} {z} {l} {b} {h}\n')

    print('running nequick')

    path_prefix = "C:/Универ/диплом/"
    nq_path = path_prefix + "сборка/NeQuickG_JRC_CCIR_MODIP_constants_UT_D.exe"
    stdin_path = path_prefix + 'сборка/stdin.txt'
    stdout_path = path_prefix + 'db/' + 'out_' + np_csv + '.txt'
    command = f'{nq_path} -f {a[0]} {a[1]} {a[2]} {stdin_path} {stdout_path}'
    print(system(command))

    print('nequick finished')


def calc_real_delay(obs, satellite, dpl1) -> tuple[list[float,], list[float,]]:
    real_time, real_delay = [], []
    fL1, fL2 = 1575.42e6, 1227.6e6
    I = lambda pL1, pL2: fL2 ** 2 / (fL1 ** 2 - fL2 ** 2) * (pL2 - (pL1 + dpl1))

    print('getting real delay')

    with open(obs, 'r') as f:
        lines = f.readlines()
        switch = 'time'
        for i, l in enumerate(lines):
            if l[:3] == '> 2':
                if switch == 'time':
                    ut = l[13:29].split(' ')
                    h, m, s = [float(x) for x in ut if x]
                    ut = h + m / 60 + s / 3600
                    switch = 'satellite'
                else:
                    switch = 'time'
            elif l[:3] == satellite and switch == 'satellite':
                try:
                    next_l = lines[i + 1]
                except IndexError:
                    break
                real_time.append(ut)

                pL1 = next_l[5:17]
                pL2 = next_l[21:33]
                d = I(float(pL1), float(pL2))
                real_delay.append(d)
                switch = 'time'

    return real_time, real_delay


def calc_nq_delay(csv_out_file) -> tuple[list[float, ], list[float, ]]:
    l1, l2 = 1575e6, 1227e6
    print('getting nequick delay')

    nq_time, nq_delay = [], []
    d = lambda tec: tec * 1e16 * 40.3 / l1 ** 2

    with open(csv_out_file, 'r') as f:
        lines = f.readlines()
        if not lines:
            raise 'No data'

        for l in lines:
            h = float(l[8:18].replace(' ', ''))
            nq_time.append(h)
            n = float(l[120:].replace(' ', ''))
            nq_delay.append(d(n))

        nq_delay_adj = [*nq_delay]
        for _ in range(int(len(nq_delay_adj) * 24 / 7)):
            nq_delay_adj.append(nq_delay_adj[0])
            nq_delay_adj.pop(0)

    return nq_time, nq_delay_adj


if __name__ == '__main__':
    start = datetime.now()
    average_length = 10
    dpl1 = 2.928
    main('E01', '04', RINEX, SP3, OBS_RINEX, dpl1, average_length)
    end = datetime.now()
    time = end - start
    print(f'execution time {time.microseconds / 1000}ms')
