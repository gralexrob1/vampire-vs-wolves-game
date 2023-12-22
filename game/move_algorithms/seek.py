from basic_structures.place import Place
from move_algorithms.helper_functions import *


def compute_move_seek(map_lists , grid):
    dep_list = map_lists[0]
    target_human = map_lists[1]
    target_enemy = map_lists[2]

    mode = 1
    if len(target_human) == 0:
        # print("targeting enemies")
        mode = 2
        target_human = target_enemy

    # get species from dep_list
    species = None
    if dep_list[0].vampires != 0:
        species = 0
    elif dep_list[0].werewolves != 0:
        species = 1


    # list all departure -> human and order them by distance
    dep_hum_dist = [] # [ [dist , dep , hum] , ... ]
    for dep in dep_list:
        for hum in target_human:
            dep_hum_dist.append([distance_in_moves(dep , hum) , dep , hum])
    dep_hum_dist = sorted(dep_hum_dist, key=lambda x: x[0])
    #print(f"Dep -> Hum : {dep_hum_dist}")

    # look for one where n of species >= n of humans
    best_dep = None
    best_hum = None
    possible_found = False

    for dep_hum in dep_hum_dist:
        n_sp = None
        if species == 0:
            n_sp = dep_hum[1].vampires
        elif species == 1:
            n_sp = dep_hum[1].werewolves

        n_hu = dep_hum[2].humans

        if mode == 2:
            if species == 0:
                n_hu = dep_hum[2].werewolves
            elif species == 1:
                n_hu = dep_hum[2].vampires


        if n_sp >= n_hu*1.5:
            possible_found = True
            best_dep = dep_hum[1]
            best_hum = dep_hum[2]
            # print(f"sp {n_sp} - {n_hu} hu (1.5)")
            break

    if not possible_found:
        for dep_hum in dep_hum_dist:
            n_sp = None
            if species == 0:
                n_sp = dep_hum[1].vampires
            elif species == 1:
                n_sp = dep_hum[1].werewolves

            n_hu = dep_hum[2].humans
            if n_sp >= n_hu*1.2: # lower expectations
                possible_found = True
                best_dep = dep_hum[1]
                best_hum = dep_hum[2]
                # print(f"sp {n_sp} - {n_hu} hu (1.2)")
                break

    # a dep -> hum with good odds found
    if possible_found:
        # Now make the move
        possible_targets = find_possible_dest(pos=[best_dep.x , best_dep.y],
                                              grid=grid,
                                              dep_list=dep_list)
        
        # list all target -> human and order by distance
        targ_hum_dist = [] # [ [dist , targ , hum] , ... ]
        for target in possible_targets:
            targ_hum_dist.append([distance_in_moves(target, best_hum , diag_weight=1.5) , target , best_hum])
        targ_hum_dist = sorted(targ_hum_dist, key=lambda x: x[0])

        # IF len(targ_hum_dist) == 0 !!!!! when there are no humans ?
        best_target = targ_hum_dist[0][1]
        #print(f"target : {best_target}")
            
        n = None
        if species == 0:
            n = best_dep.vampires
        elif species == 1:
            n = best_dep.werewolves

        move = [best_dep.x , best_dep.y , n , best_target[0] , best_target[1]]
        # print(f"send move : {move}")
        return 1 , [move]
    
    else:
        return 0 , []
