from move_algorithms.move_template import compute_move_random
from move_algorithms.move_file_1 import *
from move_algorithms.move_file_2 import *
from move_algorithms.move_file_3 import compute_move_ab
from move_algorithms.alpha_beta import *



class MoveManager:

    def __init__(self):
        pass


    def compute_move(self , strategy , map_lists , grid):
        return compute_move_expect(map_lists , grid)
        
        
