from modul.Entity import Entity

class Rock(Entity):
    """
    класс Камни
    """
    def __init__(self, row, col, map_instance):
        self.avatar = "\U0001FAA8"
        self.row = row
        self.col = col
        self.map_instance = map_instance