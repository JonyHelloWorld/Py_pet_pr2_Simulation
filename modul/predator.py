from modul.creature import Creature
from logging import getLogger

logger = getLogger(__name__)

class Predator(Creature):
    """
    класс Хищники
    """
    def __init__(self, row, col, map_instance):
        super().__init__(row=row, col=col, hp=100, speed=1, avatar="\U0001F981", map_instance=map_instance, attack=50)

    def make_move(self):
        """
        метод перемещения существа, для хищника свой, так как есть атака
        """
        logger.debug("%s на позиции (%s, %s) вызываю поиск цели", self.avatar, self.row, self.col)
        result_attack = self.do_attack()
        is_target, path = result_attack
        logger.debug("вызываю метод attack (is_target, path) (%s, %s)", is_target, path)
        if is_target:
            logger.debug(f"Путь: {path}")
            obj = self.map_instance.cut_from_dic(self.row, self.col)
            row, col = path
            self.map_instance.add_in_dic(row, col, obj)
            obj.row, obj.col = path  # обновляем координаты внутри объекта
            logger.debug("%s переместился на %s)", self.avatar, path)
        else:
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

    def do_attack(self):
        """
        метод реализует атаку, лев может атаковать соседние клетки, смотрим есть ли на них Травоядное,
        если есть атакуем
        :return: True/False- есть или нет рядом Травоядное
        :return: path - новые координаты куда перемещаемся,
        если съели или старые если не съели (у Травоядного еще осталось ХР)
        """
        for attack_row, attack_col in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_row, new_col = self.row + attack_row, self.col + attack_col
            new_coords = (new_row, new_col)
            target_obj = self.map_instance.get_from_dic(new_row, new_col)

            if self.map_instance.is_coordinate_in_map(new_row, new_col) and target_obj and target_obj.avatar == "\U0001F407":
                self.map_instance._dic[new_coords].hp -= self.map_instance._dic[(self.row, self.col)].attack
                logger.debug("%s нашел зайца и атаковал, осталось ХР %s ", self.avatar, self.map_instance._dic[new_coords].hp)
                if self.map_instance._dic[new_coords].hp <= 0:
                    logger.debug("Лев съел зайца на %s", new_coords)
                    path = (new_row, new_col) # съел и перешел на новую клетку
                    logger.debug("path из do_attack %s", path)
                    logger.debug("isinstance(path, tuple), %s", isinstance(path, tuple))
                    return True, path
                else:
                    path = (self.row, self.col) # атаковал, но не съел
                    logger.debug("path из do_attack %s", path)
                    logger.debug("isinstance(path, tuple), %s", isinstance(path, tuple))
                    return True, path

        return False, None