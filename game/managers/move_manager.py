from move_algorithms.alpha_beta import *
from move_algorithms.random import *
from move_algorithms.reflex import *
from move_algorithms.seek import *


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
        
        elif strategy == "alpha_beta":
            return make_decision(map_lists , grid)