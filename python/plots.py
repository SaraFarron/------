from matplotlib import pyplot as plt


def create_tec_plot():
    t, nq = [], []
    x, y = [], []
    d = lambda tec: tec * 10e6 * 40.3 / 1227e6 ** 2
    with open('сборка/stdout.txt', 'r') as f:
        lines = f.readlines()
        if not lines:
            print('no data')
            return
            
        for l in lines:
            h = float(l[8:18].replace(' ', ''))
            h -= 7
            # if h < 0:
            #     h = 24 - h
            t.append(h)
            n = float(l[120:].replace(' ', ''))
            nq.append(d(n))

    with open('far.txt', 'r') as f:
        lines = f.readlines()
        for l in lines:
            a, b = l.split(' ')
            x.append(a)
            y.append(b)

    fig, ax = plt.subplots(1, 2)
    ax[0].plot(t, nq, label='NeQuick')
    ax[1].plot(x, y, 'o', label='satellite', markersize=1)
    ax[0].set_xlabel('время')
    ax[0].set_ylabel('задержка')
    ax[1].set_xlabel('время')
    ax[1].set_ylabel('задержка')
    ax[0].legend()
    ax[1].legend()
    # plt.grid()
    plt.show()