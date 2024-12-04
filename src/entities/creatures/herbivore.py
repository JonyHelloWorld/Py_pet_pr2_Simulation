from logging import getLogger

from src.entities.creatures.creature import Creature

logger = getLogger(__name__)

class Herbivore(Creature):
    """
    класс Травоядные
    """
    def __init__(self, row, col, map_instance):
        super().__init__(row=row, col=col, hp=100, speed=1, avatar="\U0001F407", map_instance=map_instance)


    def make_move(self):
        """
        метод перемещения существа, наследуется от предка Creature
        """
        super().make_move()

