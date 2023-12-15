from basic_structures.place import Place
from basic_structures.move import Move
from managers.map_manager import MapManager
import math
from move_algorithms.helper_functions import *
import copy

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
    state.species = player

    ene_sp = None
    if player == 0:
        ene_sp = 1
    elif player == 1:
        ene_sp = 0

    total_value = 0

    dep_list = state.make_target_list(dep=True)
    ene_list = state.make_target_list(enemy=True)
    hum_list = state.make_target_list(human=True)

    #print(f"LISTS: dep {len(dep_list)} , ene {len(ene_list)} , hum {len(hum_list)}")

    max_dist = state.longest_distance()

    for dep in dep_list:
        n_in_dep = dep.get_n_from_sp_int(sp=player)

        for hum in hum_list:
            value = compute_expected_outcome_value(E1=n_in_dep,
                                                   E2=hum.humans,
                                                   enemy=False)
            value -= n_in_dep
            dist = distance_in_moves(dep , hum)
            value *= dist_value(dist , max_dist)
            total_value += value

        for ene in ene_list:
            value = compute_expected_outcome_value(E1=n_in_dep,
                                                   E2=hum.get_n_from_sp_int(sp=ene_sp),
                                                   enemy=True)
            value -= n_in_dep
            dist = distance_in_moves(dep , ene)
            value *= dist_value(dist , max_dist)
            total_value += value

    #print("TOT. VALUE :" , total_value)
    return total_value


def is_terminal(state:MapManager) -> bool:
    """
    In:
        state   MapManager
    Out:
        bool
    """
    if state.total_number(vampires=True) == 0 or state.total_number(werewolves=True) == 0:
        print("IS TERMINAL")
        return True
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
    new_state = copy.deepcopy(state)
    new_state.apply_moves([action] , save=True)
    return new_state


def minimax(state:MapManager , depth:int , max_player:bool , alpha:float , beta:float , w_player:int , grid):
    l_player = None
    if w_player == 0:
        l_player = 1
    elif w_player == 1:
        l_player = 0

    state.species = w_player


    if depth == 0 or is_terminal(state):
        return evaluate_state(state , w_player)
    
    if max_player:
        max_eval = -math.inf
        for action in get_possible_actions(state , w_player , grid):
            eval = minimax(result(state , action) , depth-1 , False , alpha , beta , w_player , grid)
            max_eval = max(max_eval , eval)
            alpha = max(alpha , eval)
            if beta <= alpha:
                break
        return max_eval

    else:
        min_eval = math.inf
        for action in get_possible_actions(state , l_player , grid):
            eval = minimax(result(state , action) , depth-1 , True , alpha , beta , l_player , grid)
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

    player_id = dep_list[0].get_species_in_place()

    initial_state = MapManager()
    initial_state.grid = grid
    initial_state.map = dep_list + target_human + target_enemy

    best_move = None
    best_value = -math.inf

    for action in get_possible_actions(initial_state , player_id , grid):
        move_value = minimax(result(initial_state , action) , depth=5 , max_player=False , alpha=-math.inf , beta=math.inf , w_player=player_id , grid=grid)
        if move_value > best_value:
            best_value = move_value
            best_move = action

    print(f"FINAL : {best_move} , VALUE : {best_value}")
    return 1 , [best_move.make_array()]








def compute_expected_outcome_value(E1 : int, E2: int, enemy: bool, get_enemy=False):
    """
    In:
        E1 = number of our species
        E2 = number of humans (if enemy = False) or enemies (if enemy = True)
        get_enemy = if true return E1,E2 otherwise return E1
    Out:
        returns the expected value of going on the same coordinates
    """
    
    if enemy == False: # human
        
        if E1 >= E2:
           E1 += E2
           E2 = 0

        else:
            E1 = E1**3/(2*E2)**2 + (E1**2)/(4*E2)
            E2 = ((1-(E1/(2*E2)))**2)*E2
    
    if enemy == True: # enemies
        
        if E1 > 1.5*E2:
           E1 = E1
           E2 = 0 
        
        elif E1 == E2:
           E1 = 0.25*E1
           E2 = 0.25*E2
        
        elif (E2 < E1 < 1.5*E2):
           E1 = E1*((E1/E2)-0.5)**2
           E2 = E2*(1-((E1/E2)-0.5))**2
        
        else:
           E1 = E1*(E1/(2*E2))**2
           E2 = E2*(1-(E1/(2*E2)))**2
    
    if get_enemy:
        return E1 , E2
    return E1


def dist_value (dist:int , max_dist:int , min_dist:int=1 , max_reward:float=1 , min_reward:float=0.1):
    """
    Compute the value of being at distance dist from an objective (linear)

    In:
        dist       int
        max_dist   int
        min_dist   int
        max_reward float
        min_reward float
    Out:
        value      float
    """
    dist     = float(dist)
    max_dist = float(max_dist)
    min_dist = float(min_dist)

    a = (max_reward - min_reward) / (min_dist - max_dist)
    return a*dist + max_reward - a*min_dist
