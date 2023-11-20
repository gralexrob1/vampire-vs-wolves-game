from move_algorithms.move_template import compute_move_random
from move_algorithms.move_file_1 import *
from move_algorithms.move_file_2 import *
from move_algorithms.move_file_3 import compute_move_ab

class MoveManager:
    def __init__(self):
        pass


    def compute_move(self , strategy , map_lists , grid):
        if strategy == "random":
            return compute_move_random(map_lists , grid)
        elif strategy == "seek":
            return compute_move_seek(map_lists , grid)
        elif strategy == "expect":
            return compute_move_expect(map_lists , grid)
        elif strategy == "ab_pierre":
            return compute_move_ab(map_lists , grid)
        # List the strategies here
