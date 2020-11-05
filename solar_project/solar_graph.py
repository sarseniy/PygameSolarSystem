import matplotlib.pyplot as plt
import numpy as np

from vector import *
from solar_model import gravitational_constant


class Graph:
    def __init__(self):
        self.t = []
        self.planet_mass = 0
        self.star_mass = 0

        self.planet_vx = []
        self.planet_vy = []
        self.planet_x = []
        self.planet_y = []
        self.planet_v = []

        self.star_x = []
        self.star_y = []
        self.star_vx = []
        self.star_vy = []
        self.star_v = []

        self.momentum_of_impulse = []

        self.star_motion_energy = []
        self.planet_motion_energy = []
        self.gravitation_energy = []
        self.total_energy = []

        self.r = []
        self.f = False

    def gain_data(self, objs, time):
        for obj in objs:
            if obj.type == 'Planet':

                self.planet_x.append(obj.x)
                self.planet_y.append(obj.y)
                self.planet_vx.append(obj.Vx)
                self.planet_vy.append(obj.Vy)
                self.t.append(time)
                if self.planet_mass == 0:
                    self.planet_mass = obj.m
                self.f = True

            if obj.type == 'Star':
                self.star_x.append(obj.x)
                self.star_y.append(obj.y)
                self.star_vx.append(obj.Vx)
                self.star_vy.append(obj.Vy)
                if self.star_mass == 0:
                    self.star_mass = obj.m
                self.f = True

        if self.f:
            self.write_data()

    def write_data(self):
        self.planet_v.append((self.planet_vx[-1]**2 + self.planet_vy[-1]**2)**0.5)
        self.r.append(((self.planet_x[-1] - self.star_x[-1])**2 + (self.planet_y[-1] - self.star_y[-1])**2)**0.5)

        r_vec = Vector(self.planet_x[-1], self.planet_y[-1]) - Vector(self.star_x[-1], self.star_y[-1])
        v_vec = Vector(self.planet_vx[-1], self.planet_vy[-1])
        self.momentum_of_impulse.append(abs(self.planet_mass * area(r_vec, v_vec)))

        self.star_v.append((self.star_vx[-1] ** 2 + self.star_vy[-1] ** 2) ** 0.5)

        self.planet_motion_energy.append(self.planet_v[-1]**2 * self.planet_mass / 2)
        self.star_motion_energy.append(self.star_v[-1] ** 2 * self.star_mass / 2)
        self.gravitation_energy.append(-gravitational_constant * self.star_mass * self.planet_mass / self.r[-1])
        self.total_energy.append(self.planet_motion_energy[-1] + self.star_motion_energy[-1]
                                 + self.gravitation_energy[-1])

    def show_plot(self):
        plt.figure(figsize=(15, 7))

        self.t = np.array(self.t)
        self.planet_v = np.array(self.planet_v)
        self.r = np.array(self.r)
        self.momentum_of_impulse = np.array(self.momentum_of_impulse)

        self.star_v = np.array(self.star_v)

        self.planet_motion_energy = np.array(self.planet_motion_energy)
        self.star_motion_energy = np.array(self.star_motion_energy)
        self.gravitation_energy = np.array(self.gravitation_energy)

        sp = plt.subplot(321)
        plt.plot(self.t, self.planet_v, 'g', label='Скорость от времени')
        plt.legend(loc='best', fontsize=8)
        plt.grid()
        plt.xlabel('$t$, с')
        plt.ylabel('$V$, м/с')

        sp = plt.subplot(322)
        plt.plot(self.t, self.r, 'r', label='Расстояние до звезды от времени')
        plt.legend(loc='best', fontsize=8)
        plt.grid()
        plt.xlabel('$t$, с')
        plt.ylabel(r'$\rho$, м')

        sp = plt.subplot(323)
        plt.plot(self.r, self.planet_v, label='Скорость планеты от расстояния до звезды')
        plt.legend(loc='best', fontsize=8)
        plt.grid()
        plt.xlabel(r'$\rho$, м')
        plt.ylabel('$V$, м/с')

        sp = plt.subplot(324)
        plt.plot(self.t, self.momentum_of_impulse, 'b', label='Момент импульса планеты от времени')
        plt.legend(loc='best', fontsize=8)
        plt.grid()
        plt.xlabel(r'$t$, с')
        plt.ylabel(r'$\vec{L}$, кг*м/с')

        sp = plt.subplot(325)
        plt.plot(self.t, self.total_energy, 'b', label='Суммарная энергия')
        plt.legend(loc='best', fontsize=8)
        plt.ylabel(r'$E$, Дж')
        plt.xlabel('$t$, с')
        plt.grid()

        sp = plt.subplot(326)
        plt.plot(self.t, self.planet_motion_energy, label='Кинетическая энергия планеты')
        plt.plot(self.t, self.star_motion_energy, label='Кинетическая энергия звезды')
        plt.plot(self.t, self.gravitation_energy, label='Энергия гравитационного взаимодействия')
        plt.legend(loc='best', fontsize=8)
        plt.ylabel(r'$E$, Дж')
        plt.xlabel('$t$, с')
        plt.grid()

        plt.show()


if __name__ == '__main__':
    print('This module is not for direct run!')
