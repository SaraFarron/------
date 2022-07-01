import enum
import os
from os import system
from datetime import datetime
from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from scipy import stats
from random import random

from utils import *
from xyz_to_blh import xyz_to_blh

matplotlib.rcParams.update({'font.size': 17})
RINEX = 'ftp_data/gnss/data/daily/2020/001/20l/CHPI00BRA_R_20200010000_01D_EN.rnx'
SP3 = 'ftp_data/gnss/products/2086/gfz20864.sp3'
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

    np_csv = os.path.normpath(csv_file).split(os.sep)[-1][:-4]
    csv_out_file = f'db/out_{np_csv}.txt'

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

    sats = listdir('result/')

    if not file_exitsts(csv_out_file):
        run_nequick(sp3, csv_file, np_csv, [a0, a1, a2], station_cords, month, x, y, z)

    
    if f'{satellite}-csv{csv}.png' not in sats:
        # print(satellite + ' already calculated')
        print(f'skipping {satellite}-csv{csv}')
        return

    print('sattelite ' + satellite + ' csv ' + csv)

    nq_time, nq_delay_adj = calc_nq_delay(csv_out_file)
    real_time, real_delay = calc_real_delay(obs, satellite, dpl1)

    nq_time, nq_delay_adj = nq_time[nq_slice[0]:nq_slice[1]], nq_delay_adj[nq_slice[0]:nq_slice[1]]
    real_time, real_delay = real_time[r2l_slice[0]:r2l_slice[1]], real_delay[r2l_slice[0]:r2l_slice[1]]

    make_plot(nq_time, nq_delay_adj, real_time, real_delay, satellite, csv, average_length)


def calc_diff(nq_time, real_time, nq_delay_adj, real_delay):
    print('calculating diff')
    with open('dif_data.txt', 'a') as f:
        n, r = 0, 0
        while True:
            try:
                t_dif = nq_time[n] * 86400 / 24 - real_time[r] * 86400 / 24
            except IndexError:
                break
            if t_dif >= 1:
                r += 1
                continue
            elif t_dif <= -1:
                n += 1
                continue
            dif = nq_delay_adj[n] - real_delay[r]
            f.write(f'{dif}\n')
            if t_dif > 0:
                r += 1
            else:
                n += 1


def run_nequick(sp3, csv_file, np_csv, a: list[str, str, str], station_cords, month, x, y, z):
    print('writing stdin.txt\n reading sp3')
    with open('сборка/stdin.txt', 'w') as input_data:
        with open(csv_file, 'r') as psat:
            for i, line in enumerate(psat.readlines()):
                sat_cords = line.split(' ')
                sat_cords = [sat_cords[1], sat_cords[2], sat_cords[3]]
                sat_cords = list(map(float, sat_cords))

                print('checking um')
                um = calc_um(sat_cords, station_cords)
                if um <= 0:
                    print(f'skipping - um is negative ({um})')
                    continue

                b, l, h = xyz_to_blh(*sat_cords)

                ut = i / 86400 * 24

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

                next_l = next_l.split(' ')
                next_l = [x for x in next_l if x]
                pL1 = next_l[1]
                pL2 = next_l[2]
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
            nq_delay.append(n)  # d(n)

    return nq_time, nq_delay


def parse_PPPH():
    with open('PPPH/ppph_output.txt', 'r') as f:
        xl, yl, zl = [], [], []
        lines = f.readlines()[1:]
        for l in lines:
            args = l.split(' ')
            args = [x for x in args if x]
            x, y, z = list(map(float, [args[3], args[4], args[5]]))
            xl.append(x)
            yl.append(y)
            zl.append(z)
    plt.plot(xl)
    plt.plot(yl)
    plt.plot(zl)
    plt.grid()
    plt.show()


def make_plot(nq_time, nq_delay_adj, real_time, real_delay, satellite, csv, average_length):
    print('creating plots')
    average_delay, average_time = [], []

    for i in range(2, len(real_delay), average_length):
        average_delay.append(
            sum([x for x in real_delay[i - average_length + 1:i]]) / average_length
        )
        average_time.append(real_time[i])

    average_delay[0] = real_delay[0]
    plt.plot(nq_time, nq_delay_adj, 'o', label='NeQuick', markersize=1)
    plt.plot(real_time, real_delay, 'o', label='Спутник', markersize=1)
    plt.plot(average_time, average_delay, label='Усреднение')
    plt.xlabel('Местное время, ч')
    plt.ylabel('Ионосферная задержка, м')
    plt.grid()
    plt.legend()
    plt.show()
    # plt.savefig(f'result/{satellite}-csv{csv}.png')
    plt.clf()


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), stats.sem(a)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h


def diff_plots():
    m = []
    with open('dif_data.txt', 'r') as f:
        for l in f.readlines():
            m.append(float(l))
    n = []
    for x in m:
        if x < -5:
            x += 4
        n.append(x)
    m = n
    exp_val = round(sum(m) / len(m), 2)
    variance = (sum([(x - exp_val) ** 2 for x in m]) / len(m)) ** 0.5
    plt.hist(m, 48, density=True, rwidth=0.75)
    plt.title(
        f'Мат. ожидание = {round(exp_val, 2)} Среднеквадр. отклонение = {round(variance, 2)}'
        )
    plt.grid()
    plt.ylabel('Вероятность')
    plt.xlabel('dI, м')
    plt.show()
    plt.clf()


def tec_plot(sat):
    print('reading rnx')
    # Get ionospheric coefficients
    gal = read_file(RINEX, 2, 7, 41).replace('D', 'e').split(' ')
    a = [float(x) for x in gal if x]

    # Get station coordinates
    station_cords = read_file(RINEX, 8, 2, 42).split(' ')
    station_cords = [float(x) for x in station_cords if x]
    x, y, z = xyz_to_blh(*station_cords)

    # Get date
    date = read_file(RINEX, 1, 40, 48)
    year, month, day = map(int, [date[:4], date[4:6], date[6:]])

    nq_time, nq_stec = [], []
    j = False

    print('writing stdin.txt\n reading sp3')
    with open('сборка/stdin.txt', 'w') as input_data:
        with open(SP3, 'r') as sp3:
            for i, line in enumerate(sp3.readlines()):
                if line[:4] == sat:
                    print('checking ' + sat)
                    l = [x for x in line.split(' ') if x]
                    sat_cords = list(map(float, [l[1], l[2], l[3]]))
                    # um = calc_um(sat_cords, station_cords)
                    # if um < 0:
                    #     print('um is ' + str(um))
                    #     continue
                    print('+1')
                    j = True
                    b, l, h = xyz_to_blh(*sat_cords)
                    ut = i * 15 / 96

                    input_data.write(f'{month} {ut} {y} {x} {z} {l} {b} {h}\n')

    if not j:
        return

    print('running nequick')

    path_prefix = "C:/Универ/диплом/"
    nq_path = path_prefix + "сборка/NeQuickG_JRC_CCIR_MODIP_constants_UT_D.exe"
    stdin_path = path_prefix + 'сборка/stdin.txt'
    stdout_path = path_prefix + 'db/' + 'out_' + 'sp3' + '.txt'
    command = f'{nq_path} -f {a[0]} {a[1]} {a[2]} {stdin_path} {stdout_path}'
    print(system(command))

    with open('db/out_sp3.txt', 'r') as f:
        for i, line in enumerate(f.readlines()):
            l = [x for x in line.split(' ') if x]
            time = l[1]
            tec = l[-1]
            nq_time.append(float(time))
            nq_stec.append(float(tec))

    print('nequick finished')
    plt.plot(nq_time, nq_stec)
    plt.grid()
    plt.ylabel('STEC, TECU')
    plt.xlabel('Время суток')
    plt.savefig(f'pres pics/{sat}.png')
    plt.clf()


if __name__ == '__main__':
    start = datetime.now()
    average_length = 10
    dpl1 = -2.928
    # main('C09', '02', RINEX, SP3, OBS_RINEX, dpl1, average_length, nq_slice=[1700, -1], r2l_slice=[35, -1])
    # diff_plots()
    sats = [f'PG0{x}' for x in range(1, 10)] + [f'PG{x}' for x in range(10, 20)]
    for sat in sats:
        tec_plot(sat)
    # nq_time, nq_stec = [], []
    # with open('сборка/stdout.txt', 'r') as f:
    #     for i, line in enumerate(f.readlines()):
    #         l = [x for x in line.split(' ') if x]
    #         time = l[1]
    #         tec = l[-1]
    #         nq_time.append(float(time))
    #         nq_stec.append(float(tec))

    # for i in range(1):
    #     nq_stec.append(nq_stec[0])
    #     nq_stec.pop(0)

    # plt.plot(nq_time, nq_stec)
    # plt.grid()
    # plt.ylabel('STEC, TECU')
    # plt.xlabel('Время суток')
    # plt.show()
    end = datetime.now()
    time = end - start
    print(f'execution time {time.microseconds / 1000}ms')
