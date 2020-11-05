# coding: utf-8
# license: GPLv3

import tkinter as tk
from tkinter import filedialog

from solar_vis import *
from solar_model import *
from solar_input import *
from solar_graph import *
import thorpy
import time
import numpy as np

root = tk.Tk()
root.withdraw()

timer = None

alive = True

perform_execution = False
"""Флаг цикличности выполнения расчёта"""

model_time = 0
"""Физическое время от начала расчёта.
Тип: float"""

time_scale = 1000.0
"""Шаг по времени при моделировании.
Тип: float"""

space_objects = []
"""Список космических объектов."""


def execution(delta):
    """Функция исполнения -- выполняется циклически, вызывая обработку всех небесных тел,
    а также обновляя их положение на экране.
    Цикличность выполнения зависит от значения глобальной переменной perform_execution.
    При perform_execution == True функция запрашивает вызов самой себя по таймеру через от 1 мс до 100 мс.
    """
    global model_time
    recalculate_space_objects_positions([dr for dr in space_objects], delta)
    model_time += delta


def start_execution():
    """Обработчик события нажатия на кнопку Start.
    Запускает циклическое исполнение функции execution.
    """
    global perform_execution
    perform_execution = True


def pause_execution():
    global perform_execution
    perform_execution = False


def stop_execution():
    """Обработчик события нажатия на кнопку Start.
    Останавливает циклическое исполнение функции execution.
    """
    global alive
    alive = False


def open_file():
    """Открывает диалоговое окно выбора имени файла и вызывает
    функцию считывания параметров системы небесных тел из данного файла.
    Считанные объекты сохраняются в глобальный список space_objects
    """
    global space_objects
    global model_time

    file_dir = filedialog.askopenfilename(initialdir="*")
    space_objects = read_space_objects_data_from_file(file_dir)
    model_time = 0.0
    max_distance = max([max(abs(obj.x), abs(obj.y)) for obj in space_objects])
    calculate_scale_factor(max_distance)


def handle_events(events, menu):
    global alive
    for event in events:
        menu.react(event)
        if event.type == pg.QUIT:
            alive = False


def slider_to_real(val):
    return np.exp(5 + val)


def slider_reaction(event):
    global time_scale
    time_scale = slider_to_real(event.el.get_value())


def init_ui(screen):
    slider = thorpy.SliderX(100, (5, 15), "Simulation speed")
    slider.user_func = slider_reaction
    button_stop = thorpy.make_button("Quit", func=stop_execution)
    button_pause = thorpy.make_button("Pause", func=pause_execution)
    button_play = thorpy.make_button("Play", func=start_execution)
    timer = thorpy.OneLineText("Seconds passed")

    button_load = thorpy.make_button(text="Load a file", func=open_file)

    box = thorpy.Box(elements=[
        slider,
        button_pause,
        button_stop,
        button_play,
        button_load,
        timer])
    reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=slider_reaction,
                                event_args={"id": thorpy.constants.EVENT_SLIDE},
                                params={},
                                reac_name="slider reaction")
    box.add_reaction(reaction1)

    menu = thorpy.Menu(box)
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((0, 0))
    box.blit()
    box.update()
    return menu, box, timer


def check_graph_availability(objects):
    stars = 0
    planets = 0
    for obj in objects:
        if obj.type == 'Planet':
            planets += 1
        if obj.type == 'Star':
            stars += 1
    if stars == 1 and planets == 1:
        return True
    else:
        return False



def main():
    """Главная функция главного модуля.
    Создаёт объекты графического дизайна библиотеки tkinter: окно, холст, фрейм с кнопками, кнопки.
    """

    global time_step
    global time_speed
    global space
    global start_button
    global perform_execution
    global timer

    print('Modelling started!')

    pg.init()

    output_file = 'output.txt'
    out = open(output_file, 'w')
    out.close()

    width = 1400
    height = 800
    screen = pg.display.set_mode((width, height))
    last_time = time.perf_counter()
    drawer = Drawer(screen)
    menu, box, timer = init_ui(screen)
    perform_execution = True

    gr = Graph()

    while alive:
        gr_drawing_flag = check_graph_availability(space_objects)
        handle_events(pg.event.get(), menu)
        cur_time = time.perf_counter()
        if perform_execution:
            execution((cur_time - last_time) * time_scale)
            text = "%d seconds passed" % (int(model_time))
            timer.set_text(text)

        last_time = cur_time
        drawer.update(space_objects, box)
        time.sleep(1.0 / 60)

        if gr_drawing_flag:
            gr.gain_data(space_objects, model_time)

        write_space_objects_data_to_file(output_file, space_objects, model_time)

    print('Modelling finished!')
    pg.quit()

    if gr_drawing_flag:
        gr.show_plot()


if __name__ == "__main__":
    main()
