import abc

class Entity(abc.ABC):
    def __init__(self, avatar, row, col, map_instance):
        self.avatar = avatar
        self.row = row
        self.col = col
        self.map_instance = map_instance

