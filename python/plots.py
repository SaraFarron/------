from matplotlib import pyplot as plt

t, y = [], []
with open('сборка/stdout.txt', 'r') as f:
    for l in f.readlines():
        h = float(l[8:18].replace(' ', ''))
        t.append(h)
        n = float(l[117:].replace(' ', ''))
        y.append(n)
        
plt.plot(y)
plt.xlabel('Время суток, ч')
plt.ylabel('STEC')
plt.grid()
plt.show()
