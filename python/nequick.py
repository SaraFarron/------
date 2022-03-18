from os import system
import argparse


NEQUICK_PATH = r'C:\NeQuickJRC\NeQuickJRC\bin\msvc\NeQuickG_JRC.exe '
NEQUICK_MODIP_ARG = r'C:\NeQuickJRC\NeQuickJRC\modip\modip2001_wrapped.asc '
NEQUICK_CCIR_ARG = r'C:\NeQuickJRC\NeQuickJRC\ccir\ '

parser = argparse.ArgumentParser(description='NeQuick launch script')
parser.add_argument("-a0", default='1', type=str, help="ionospheric 1st param")
parser.add_argument("-a1", default='1', type=str, help="ionospheric 2nd param")
parser.add_argument("-a2", default='1', type=str, help="ionospheric 3rd param")

parser.add_argument("-m", default='1', type=str, help="month")
parser.add_argument("-ut", default='1', type=str, help="UT")

parser.add_argument("-slo", default='1', type=str, help="station.longitude")
parser.add_argument("-sla", default='1', type=str, help="station.latitude")
parser.add_argument("-sh", default='1', type=str, help="station.height")

parser.add_argument("-sala", default='1', type=str, help="satellite.longitude")
parser.add_argument("-salo", default='1', type=str, help="satellite.latitude")
parser.add_argument("-sah", default='1', type=str, help="satellite.height")

args = parser.parse_args()

gal_args = ' '.join([args.a0, args.a1, args.a2]) + ' '
time_args = ' '.join([args.m, args.ut]) + ' '
station_args = ' '.join([args.slo, args.sla, args.sh]) + ' '
sattelite_args = ' '.join([args.sala, args.salo, args.sah])

command = NEQUICK_PATH + NEQUICK_MODIP_ARG + NEQUICK_CCIR_ARG + '-c ' + gal_args + time_args + station_args + sattelite_args

print(system(command))