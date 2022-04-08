from os import system


NEQUICK_PATH = r'C:\NeQuickJRC\NeQuickJRC\bin\msvc\NeQuickG_JRC.exe '
NEQUICK_MODIP_ARG = r'C:\NeQuickJRC\NeQuickJRC\modip\modip2001_wrapped.asc '
NEQUICK_CCIR_ARG = r'C:\NeQuickJRC\NeQuickJRC\ccir\ '

a0, a1, a2 = 2.4500E+01, 3.2422E-01, 4.3640E-03
time = '02 18:24:27'
station_cords = [-15.425538589403404, 28.311014636811894, 1324.9196041869]
sattelite_cords = [-111.18083374029375, 137.59726265257754, -6401946.81655583]


gal_args = ' '.join(map(str, [a0, a1, a2])) + ' '
time_args = time + ' '
station_args = ' '.join(map(str, station_cords)) + ' '
sattelite_args = ' '.join(map(str, sattelite_cords))

command = NEQUICK_PATH + NEQUICK_MODIP_ARG + NEQUICK_CCIR_ARG + '-c ' + gal_args + time_args + station_args + sattelite_args

print(system(command))
