from basic_structures.place import Place
from move_algorithms.helper_functions import *

import random 


def compute_move_random(map_lists , grid):
    """
    Example compute_move function
    Returns len([moves]) , [moves]
    """
    dep_list = map_lists[0]     # [Place] list where there are some of current species
    target_human = map_lists[1] # [Place] list of humans
    target_enemy = map_lists[2] # [Place] list of enemies

    moves = [] # [ [x1 , y1 , n , x2 , y2] , ... ]

    for dep in dep_list:
        possible_targets = find_possible_dest(pos=[dep.x , dep.y],
                                              grid=grid,
                                              dep_list=dep_list)

        if len(possible_targets) > 0:
            target_coord = possible_targets[random.randint(0 , len(possible_targets)-1)] 
            move = [dep.x , dep.y , 1 , target_coord[0] , target_coord[1]]
            moves.append(move)
            
    # print(f"Sending {len(moves)} moves : {moves}")
    return len(moves) , moves
