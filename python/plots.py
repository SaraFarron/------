from matplotlib import pyplot as plt
from utils import read_file


t, y = [], []
with open('сборка/out.txt', 'r') as f:
    for l in f.readlines():
        h = float(l[8:17].replace(' ', ''))
        t.append(h)
        n = float(l[117:-1].replace(' ', ''))
        y.append(n)
        
plt.plot(t, y)
plt.xlabel('Время суток, ч')
plt.ylabel('STEC')
plt.grid()
plt.show()
