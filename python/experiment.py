from os import listdir, remove

from numpy import diff
from utils import read_file
from xyz_to_blh import xyz_to_blh, xyz2blh_gost


def file_exists(filename: str) -> bool:
    """
    Remove file if it already exists
    """
    if filename in listdir():
        remove(filename)
        return True
    return False


def parse_rinex():
    rinex_dir = 'ftp_data/gnss/data/daily/'
    file_name = 'rinex_data.txt'
    file_exists(file_name)

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
                    date_time = read_file(path, 1, 40, 55)
                    gal = read_file(path, 2, 7, 41)
                    cords = read_file(path, 8, 2, 42)
                    date, time = date_time.split(' ')
                    # x, y, z = cords.split(' ')
                    with open(file_name, 'a') as f:
                        f.write(f'date: {date} time: {time} GAL: {gal} x, y, z: {cords} file: {file}\n')
                else:
                    print(f'file {file} is wrong: gal: {gal} cords comment: {cords_comment}')


def parse_sp3():
    sp3_dir = 'ftp_data/gnss/products/'
    file_name = 'sp3_data.txt'
    file_exists(file_name)

    for folder in listdir(sp3_dir):
        dir_of_files = sp3_dir + folder + '/'
        for file in listdir(dir_of_files):
            date_time = read_file(dir_of_files + file, 22, 3, 31)
            with open(file_name, 'a') as f:
                f.write(f'date time: {date_time}, file: {file}\n')


def main():
    """
    1. Parse rinex, get date and time, get a0, a1 and a2
    2. Parse all sp3s, get date and time and compare with rinex's - if it ~= - take data,
    if not - next one
    3. Create txt file with data needed for nequick, transform xyz to blh
    3.1. (Optional) Check differenct in final results between gost blh and internet one
    4. Run nequick
    5. (Optional) After nequick finishes - create a plot
    """
    file_name = 'cords.txt'
    file_exists(file_name)

    with open('psat_data.txt', 'r') as f:
        counter, difference_counter = 0, 0
        for l in f.readlines():
            x, y, z = l[4:12], l[17:25], l[30:38]
            x, y, z = x.replace(' ', ''), y.replace(' ', ''), z.replace(' ', '')
            try:
                x, y, z = float(x), float(y), float(z)
            except ValueError:
                print('Value Error')
                return
            blh = xyz_to_blh(x, y, z)
            blh_gost = xyz2blh_gost(x, y, z)
            for n, g in zip(blh, blh_gost):
                if n != g:
                    difference_counter += 1
            with open(file_name, 'a') as c:
                c.write(f'b = {blh[0]}, l = {blh[1]}, h = {blh[2]}\n')
            counter += 1
    print(f'counter = {counter} difference counter = {difference_counter}')
        
if __name__ == '__main__':
    main()
