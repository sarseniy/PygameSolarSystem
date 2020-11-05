import matplotlib.pyplot as plt
import numpy as np


class Graph:
    def __init__(self):
        self.t = []
        self.v = []
        self.r = []

    def gain_data(self, objs, time):
        for obj in objs:
            if obj.type == 'Planet':
                self.v.append((obj.Vx**2 + obj.Vy**2)**0.5)
                self.t.append(time)
                self.r.append((obj.x**2 + obj.y**2)**0.5)

    def show_plot(self):
        plt.figure(figsize=(15, 7))

        self.t = np.array(self.t)
        self.v = np.array(self.v)
        self.r = np.array(self.r)

        sp = plt.subplot(221)
        plt.plot(self.t, self.v)
        plt.title(r'$V$ от $t$')
        plt.grid()
        plt.xlabel('$t$, с')
        plt.ylabel('$V$, м/с')

        sp = plt.subplot(222)
        plt.plot(self.t, self.r)
        plt.title(r'$\rho$ от $t$')
        plt.grid()
        plt.xlabel('$t$, с')
        plt.ylabel(r'$\rho$, м')

        sp = plt.subplot(223)
        plt.plot(self.r, self.v)
        plt.title(r'$V$ от $\rho$')
        plt.grid()
        plt.xlabel(r'$\rho$, м')
        plt.ylabel('$V$, м/с')

        plt.show()
