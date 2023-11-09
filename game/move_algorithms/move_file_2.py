from basic_structures.place import Place
from move_algorithms.helper_functions import *

"""
Still working on this

Function based on:
    max expected value
    min distance to travel
"""

def compute_move_expect(map_lists , grid):
    dep_list = map_lists[0]
    target_human = map_lists[1]
    target_enemy = map_lists[2]

    moves = []


    # get species from dep_list
    species = None
    ene_sp = None
    if dep_list[0].vampires != 0:
        species = 0
        ene_sp = 1
    elif dep_list[0].werewolves != 0:
        species = 1
        ene_sp = 0


    for dep in dep_list:
        n_in_dep = dep.get_n_from_sp_int(species)

        # 1st make a list of targets and the value to go to them (humans and enemies combined)
        human_list = []
        for target in target_human:
            distance = float(distance_in_moves(dep , target))
            expected_value = compute_expected_outcome_value(E1=n_in_dep ,
                                                            E2=target.humans,
                                                            enemy=False)
            value = expected_value
            if distance != 0:
                value = expected_value/distance
            human_list.append([target , value])


        enemy_list = []
        for target in target_enemy:
            distance = float(distance_in_moves(dep , target))
            expected_value = compute_expected_outcome_value(E1=n_in_dep ,
                                                            E2=target.get_n_from_sp_int(ene_sp),
                                                            enemy=True)
            value = expected_value
            if distance != 0:
                value = expected_value/distance
            enemy_list.append([target , value])


        combined_list = human_list + enemy_list
        combined_list = sorted(combined_list , key=lambda x: x[1] , reverse=True)

        #print(f"value: {combined_list}")

        v_pri = []
        for object in combined_list:
            t , v = object
            v_pri.append([[t.x , t.y] , v])

        print(f"value: {v_pri}")


        best_target = combined_list[0][0]

        # Now find possible destination from dep
        possible_dest = find_possible_dest(pos=[dep.x , dep.y],
                                           grid=grid,
                                           dep_list=dep_list)
        
        # Find which destination (from dep) is closest to the best_target
        dest_target = []
        for dest in possible_dest:
            distance = distance_in_moves(dest , best_target)
            dest_target.append([possible_dest , distance])
        dest_target = sorted(dest_target , key=lambda x: x[1])

        best_dest = dest_target[0][0][0]
        

        # Now append this move to moves
        move = [dep.x , dep.y , n_in_dep , best_dest[0] , best_dest[1]]
        moves.append(move)



    #print(f"send {len(moves)} --- {moves}")
    return len(moves) , moves






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



