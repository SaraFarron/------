from matplotlib import pyplot as plt

t, y = [], []
with open('сборка/stdout.txt', 'r') as f:
    for l in f.readlines():
        h = float(l[8:18].replace(' ', ''))
        t.append(h)
        n = float(l[120:].replace(' ', ''))
        y.append(n)

# length = 30
# average = []
# for i in range(2, len(y), length):
#     average.append(
#         sum([x for x in y[i-length+1:i]]) / length
#     )

plt.plot(t, y)
plt.xlabel('Время суток, ч')
plt.ylabel('STEC')
plt.grid()
plt.show()
