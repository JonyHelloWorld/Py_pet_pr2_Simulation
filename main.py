import json
import logging.config
from modul.map import Map
from modul.grass import Grass
from modul.rock import Rock
from modul.tree import Tree
from modul.herbivore import Herbivore
from modul.predator import Predator
import time
import random
import re
import threading

from logging import getLogger # basicConfig, DEBUG, INFO, ERROR, FileHandler, StreamHandler

# 2 варианта настройки логирования (считать настройки из файла или прописать их в коде)
try:
    with open("Log/logging.conf", "r") as file:
        config = json.load(file)
        print("JSON загружен успешно.")

except json.JSONDecodeError as e:
    print("Ошибка в JSON-файле:", e)

logging.config.dictConfig(config)
logger = getLogger()#
# FORMAT = '%(asctime)s : %(name)s : %(levelname)s : %(message)s'
# file_handler = FileHandler('data.log')
# file_handler.setLevel(DEBUG)
# terminal = StreamHandler()
# terminal.setLevel(DEBUG)
# basicConfig(format = FORMAT, level = DEBUG, handlers = [file_handler, terminal])

# флаг прерывания бесконечного цикла
is_exit = threading.Event()
is_exit.set() # включил

class Simulation:
    """
    класс Симуляция в котором создаем карту, сущности и запускаем бесконечную симуляцию
    """
    def __init__(self, rows, cols):
        self.map_instance = Map(rows, cols)
        self.create_an_entity(rows, Grass)
        self.create_an_entity(rows, Tree)
        self.create_an_entity(rows, Rock, rows // 2)
        self.create_an_entity(rows, Herbivore, rows // 3)
        self.create_an_entity(rows, Predator, rows // 3)

    def create_an_entity(self, rows, entity, quantity_entity = None):
        """
        создание сущностей
        :param "rows": размер карты (по умолчанию принимаю, что карта квадратная)
        :param "entity": вид сущности
        :param "quantity_entity": количество создаваемых сущностей (по умолчанию пустое значение)
        """
        if quantity_entity == None:
            for i in range(0, rows):
                row = random.randint(1, rows)
                col = random.randint(1, rows)
                while not self.map_instance.is_coordinate_empty(row, col):
                    row = random.randint(1, rows)
                    col = random.randint(1, rows)
                obj = entity(row, col, self.map_instance)
                self.map_instance.add_in_dic(row, col, obj)

        else: # генерация сущностей в процессе игры
            for i in range(1, quantity_entity):
                row = random.randint(1, rows)
                col = random.randint(1, rows)
                # цикл проверяет, что сгенерированные координаты пустые, иначе генерит новые
                while not self.map_instance.is_coordinate_empty(row, col):
                    row = random.randint(1, rows)
                    col = random.randint(1, rows)
                obj = entity(row, col, self.map_instance)
                self.map_instance.add_in_dic(row, col, obj)

    def render_map(self):
        """
        отрисовка карты (берем словарь, где Ключ это адрес ячейки и выводим изображение сущности в терминале
        пустоты заполняем коричневыми прямоугольниками - землей
        """
        for row in range(1, self.map_instance.rows + 1):
            for col in range(1, self.map_instance.cols + 1):
                if (row, col) in self.map_instance._dic:
                    print(f"{self.map_instance._dic[(row, col)].avatar} ", end="")
                else:
                    print("\U0001F7EB ", end="")
            print()

    def begin_simulation(self):
        """
        метод запускаем бесконечную симуляцию пока не будет нажат Enter, после этого выход
        """
        if input("нажмите 1, чтобы запустить бесконечную симуляцию мира) \n") == "1":
            while is_exit.is_set():
                quantity_grass = 0
                quantity_herbivore = 0
                for coordinates, creature in self.map_instance._dic.copy().items():
                    if isinstance(creature, Predator):
                        creature.make_move()
                    elif isinstance(creature, Herbivore):
                        quantity_herbivore += 1
                        creature.make_move()
                    elif isinstance(creature, Grass):
                        quantity_grass += 1

                if  quantity_herbivore == 0:
                    self.create_an_entity(self.map_instance.rows, Herbivore, self.map_instance.rows // 3)

                if quantity_grass == 0:
                    self.create_an_entity(self.map_instance.rows, Grass, self.map_instance.rows // 2)
                time.sleep(0.5)
                self.render_map()

    def exit_simulation(self):
        """
        метод ждет нажатие Enter и останавливает поток
        """
        input("нажмите Enter для выхода из симуляции\n")
        is_exit.clear()

size_map = int(input("введите размер карты \n"))
simulation = Simulation(size_map, size_map)
logger.info("генерирую карту")

simulation.render_map()
logger.info('мир создан и заселён, \nзапустить бесконечную симуляцию?')
# создал поток и запустил
thread_simulation = threading.Thread(target = simulation.begin_simulation, daemon = True,)
thread_simulation.start()
simulation.exit_simulation()
thread_simulation.join()
