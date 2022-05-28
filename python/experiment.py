from os import listdir, remove
from utils import read_file
from xyz_to_blh import xyz_to_blh, xyz2blh_gost


def parse_rinex():
    rinex_dir = 'ftp_data/gnss/data/daily/'
    file_name = 'rinex_data.txt'

    if file_name in listdir():
        remove(file_name)

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
    sp3_dir = 'ftp_data/gnss/products/'
    file_name = 'sp3_data.txt'

    if file_name in listdir():
        remove(file_name)

    for folder in listdir(sp3_dir):
        dir_of_files = sp3_dir + folder + '/'
        for file in listdir(dir_of_files):
            date_time = read_file(dir_of_files + file, 22, 3, 31)
            with open(file_name, 'a') as f:
                f.write(f'date time: {date_time}, file: {file}\n')
        
if __name__ == '__main__':
    main()
