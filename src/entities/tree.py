from src.entities.entity import Entity

class Tree(Entity):
    """
    класс Деревья
    """
    def __init__(self, row, col, map_instance):
        self.avatar = "\U0001F332"
        self.row = row
        self.col = col
        self.map_instance = map_instance