import math
from matplotlib import pyplot as plt
from math import sin, exp
import numpy as np

t, y = [], []
# with open('сборка/stdout.txt', 'r') as f:
#     for l in f.readlines():
#         h = float(l[8:18].replace(' ', ''))
#         t.append(h)
#         n = float(l[120:].replace(' ', ''))
#         y.append(n)
t = [x for x in np.arange(0, 24, 0.01)]
for x in t:
    if x < 5:
        tec = exp(x * 4e-1)
    elif x > 19:
        tec = 1e5 * x ** -3 * exp(-x * 1e-5)
    else:
        tec = 25 * sin(x * .1 + 1.7)
    y.append(tec)

plt.plot(t, y)
plt.xlabel('Время суток, ч')
plt.ylabel('STEC')
plt.grid()
plt.show()
