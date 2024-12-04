from logging import getLogger


logger = getLogger(__name__)


class Map:
    """
    класс Карта
    """
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self._dic = {}


    def is_coordinate_empty(self, row, col):
        """
        проверяем есть ли по данным координатам сущность
        :param "row": ряд
        :param "col": колонка
        :return: True/False - нет сущности/есть сущность
        """
        if (row, col) not in self._dic:
            return True
        else:
            return False

    def add_in_dic(self, row, col, obj):
        """
        добавляем сущность в словарь
        :param "row": ряд
        :param "col": колонка
        :param "obj": объект сущности
        """
        self._dic[(row, col)] = obj

    def cut_from_dic(self, row, col):
        """
        вырезаем объект из словаря (чтобы затем переместить его на новые координаты)
        :param "row": ряд
        :param "col": колонка
        """
        obj = self._dic.pop((row, col))
        return obj

    def get_from_dic(self, row, col):
        """
        считываем объект из словаря
        :param "row": ряд
        :param "col": колонка
        """
        obj = self._dic.get((row, col))
        return obj

    def is_coordinate_empty_grass_or_herbivore(self, row, col, avatar):
        """
        проверяем, что по координатам нет травы или травоядного
        :param "row": ряд
        :param "col": колонка
        :param "avatar": аватар того для кого проверяем (Заяц может сходить только на Траву,
        а Лев может сходить только на Зайца)
        :return: True/False - может идти по координатам/не может
        """
        match avatar:
            case "\U0001F407":
                if self.is_coordinate_empty(row, col):
                    return True
                else:
                    obj = self.get_from_dic(row, col)
                    if obj.avatar == "\U0001F331":
                        return True
                    else:
                        return False
            case "\U0001F981":
                if self.is_coordinate_empty(row, col):
                    return True
                else:
                    obj = self.get_from_dic(row, col)
                    if obj.avatar == "\U0001F407":
                        return True
                    else:
                        return False

    def is_coordinate_in_map(self, row, col):
        """
        проверяем, что координаты в пределах карты
        :param "row": ряд
        :param "col": колонка
        :return: True/False - в пределах карты/нет
        """
        coordinate_in_map = False
        if 1 <= row <= self.rows and 1 <= col <= self.cols:
            coordinate_in_map = True
        return coordinate_in_map