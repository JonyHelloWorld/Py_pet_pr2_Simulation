from modul.Entity import Entity
from collections import deque
from logging import getLogger

logger = getLogger(__name__)

class Creature(Entity):
    """
    класс Животные (потомки Травоядные и Хищники)
    """
    def __init__(self, row, col, hp, speed, avatar, map_instance, attack = None):
        super().__init__(avatar, row, col, map_instance)
        self.hp = hp
        self.speed = speed
        self.attack = attack

    # @abc.abstractmethod
    def make_move(self):
        """
        метод перемещения существа
        """
        logger.debug("%s на позиции (%s, %s) вызываю поиск цели", self.avatar, self.row, self.col)

        path = self.breadth_first_search()
        if not path:
            logger.debug("Путь не найден")
            return

        # ограничиваем длину пути скоростью сущности
        move_steps = min(self.speed, len(path))
        new_coordinates = path[:move_steps][-1]  # обрезаем путь до значения скорости и берем предпоследний элемент

        logger.debug(f"Путь: {path}, новые координаты: {new_coordinates}")

        obj = self.map_instance.cut_from_dic(self.row, self.col)
        row, col = new_coordinates
        self.map_instance.add_in_dic(row, col, obj)

        obj.row, obj.col = new_coordinates  # обновляем координаты внутри объекта
        logger.debug("%s переместился на (%s, %s)", self.avatar, new_coordinates[0], new_coordinates[1])

    def breadth_first_search(self):
        """
        метод поиска пути в ширину
        :return: path - путь до цели в виде списка координат
        """
        queue_coordinats = deque([((self.row, self.col), [])])  # очередь: ((координаты), путь)
        searched_coordinats = set()

        while queue_coordinats:
            (coordinats, path) = queue_coordinats.popleft()  # извлекаем первый элемент из очереди
            row, col = coordinats  # распаковываем координаты

            # если координаты уже проверены, переходим к следующему в очереди
            if coordinats in searched_coordinats:
                continue

            searched_coordinats.add(coordinats)

            # проверка цели
            # current_obj = self.map_instance.dic.get(coordinats)
            current_obj = self.map_instance.get_from_dic(*coordinats)

            if current_obj:
                if self.avatar == "\U0001F407" and current_obj.avatar == "\U0001F331":
                    logger.debug("%s нашёл траву на (%s, %s)", self.avatar, row, col)
                    return path #+ [coordinats]
                elif self.avatar == "\U0001F981" and current_obj.avatar == "\U0001F407":
                    logger.debug("%s нашел зайца на (%s, %s)", self.avatar, row, col)
                    return path

            # добавление клеток в очередь
            for d_row, d_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_row, new_col = row + d_row, col + d_col
                new_coords = (new_row, new_col)

                # валидация координат
                if (self.map_instance.is_coordinate_in_map(new_row, new_col) and
                    self.map_instance.is_coordinate_empty_grass_or_herbivore(new_row, new_col, self.avatar) and
                    new_coords not in searched_coordinats):

                    queue_coordinats.append((new_coords, path + [new_coords]))
                    logger.debug(f"Добавляю в очередь: {new_coords}, текущий путь: {path + [new_coords]}")

        logger.debug("Путь не найден")
        return None

