from basic_structures.place import Place
from basic_structures.move import Move
from managers.map_manager import MapManager
import math
from helper_functions import *

"""
Still working on this
alpha beta
"""


def evaluate_state(state:MapManager , player:int) -> float:
    """
    In:
        state   MapManager
        player  int         (vampires : 0 , werewolves : 1)
    Out:
        float
    """
    return 0


def is_terminal(state:MapManager) -> bool:
    """
    In:
        state   MapManager
    Out:
        bool
    """
    return False


def get_possible_actions(state:MapManager , player:int , grid):
    """
    In:
        state   MapManager
        player  int         (vampires : 0 , werewolves : 1)
    Out:
        [Move]
    """
    state.species = player
    dep_list = state.make_target_list(dep=True)
    dep_1 = dep_list[0] # no splitting
    n_in_dep_1 = dep_1.get_n_from_sp_int(player)

    possible_dest = find_possible_dest(pos=[dep_1.x , dep_1.y],
                                       grid=grid,
                                       dep_list=dep_list)
    
    out = []
    for p_dest in possible_dest:
        out.append(Move([dep_1.x , dep_1.y , n_in_dep_1 , p_dest[0] , p_dest[1]]))

    return out


def result(state:MapManager , action:Move):
    """
    In:
        state   MapManager
        action  Move
    Out:
        MapManager
    """
    return


def minimax(state:MapManager , depth:int , max_player:bool , alpha:float , beta:float):
    
    if depth == 0 or is_terminal(state):
        return evaluate_state(state)
    
    if max_player:
        max_eval = -math.inf
        for action in get_possible_actions(state):
            eval = minimax(result(state , action) , depth-1 , False , alpha , beta)
            max_eval = max(max_eval , eval)
            alpha = max(alpha , eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = math.inf
        for action in get_possible_actions(state):
            eval = minimax(result(state , action) , depth-1 , True , alpha , beta)
            min_eval = min(min_eval , eval)
            beta = min(beta , eval)
            if beta <= alpha:
                break
        return min_eval
        



def compute_move_ab(map_lists , grid):
    """
    Function that is called in move_manager
    """
    dep_list = map_lists[0]
    target_human = map_lists[1]
    target_enemy = map_lists[2]

    initial_state = MapManager()
    initial_state.grid = grid
    initial_state.map = dep_list + target_human + target_enemy

    best_move = None
    best_value = -math.inf

    for action in get_possible_actions(initial_state):
        move_value = minimax(result(initial_state , action) , depth=3 , max_player=False , alpha=-math.inf , beta=math.inf)
        if move_value > best_value:
            best_value = move_value
            best_move = action

    return 1 , [best_move]
