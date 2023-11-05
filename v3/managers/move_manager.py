from move_algorithms.move_template import compute_move_random


class MoveManager:
    def __init__(self):
        pass


    def compute_move(self , strategy , map_lists , grid):
        if strategy == "random":
            return compute_move_random(map_lists , grid)
        # List the strategies here

