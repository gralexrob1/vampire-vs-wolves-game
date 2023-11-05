from basic_structures.place import Place
from basic_structures.move import Move
from move_algorithms.helper_functions import *
import random

"""
This is an example of a file with a compute_move_function
This is called in move_manager if the strategy is "random"

compute_move_functions take in
    map_lists = [dep_list , target_human , target_enemy]
    grid = [m,n]
and need to return
    len(moves) , moves

where moves = [move]
and   move  = [x1 , y1 , n , x2 , y2]


-> compute_move_functions could be on separate files for separate implementation
-> they need to be called in move_manager
"""


def compute_move_random(map_lists , grid):
    """
    Example compute_move function
    Returns len([moves]) , [moves]
    """
    dep_list = map_lists[0]     # [Place]
    target_human = map_lists[1] # [Place]
    target_enemy = map_lists[2] # [Place]

    moves = []

    for dep in dep_list:
        possible_targets = find_possible_dest(pos=[dep.x , dep.y],
                                              grid=grid,
                                              dep_list=dep_list)


        if len(possible_targets) > 0:
            target_coord = possible_targets[random.randint(0 , len(possible_targets)-1)] 
            move = [dep.x , dep.y , 1 , target_coord[0] , target_coord[1]]
            moves.append(move)
            

    print(f"Sending {len(moves)} moves : {moves}")
    return len(moves) , moves



def compute_move_template(map_lists , grid):
    """
    Template for a compute_move_function
    """
    dep_list = map_lists[0]     # [Place]
    target_human = map_lists[1] # [Place]
    target_enemy = map_lists[2] # [Place]
    moves = []

    # add code here ...

    return len(moves) , moves
