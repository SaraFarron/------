from matplotlib import pyplot as plt

from utils import read_file

fL1, fL2 = 1575.42e6, 1227.6e6
file = 'pseudo.txt'

I = lambda pL1, pL2: fL2 ** 2 / (fL1 ** 2 - fL2 ** 2) * (pL2 - pL1)
t, delay = [], []

line = 188
while line < 80000:
    try:
        l = read_file(file, line, 0, 3)
        y = read_file(file, line + 1, 0, 3)
    except Exception as e:
        print(e)
        break
    if l == '> 2' and y == 'C10':
        ut = read_file(file, line, 13, 29).split(' ')
        h, m, s = [float(x) for x in ut if x] 
        ut = h + m / 60 + s / 3600
        t.append(ut)

        pL1 = read_file(file, line + 1, 5, 17)
        pL2 = read_file(file, line + 1, 21, 33)
        d = I(float(pL1), float(pL2))
        delay.append(d)
    line += 1

plt.plot(t, delay, 'o')
plt.grid()
plt.show()
