from basic_structures.place import Place
from move_algorithms.helper_functions import *
from math import sqrt

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


    sent_b_trg = []

    for dep in dep_list:
        n_in_dep = dep.get_n_from_sp_int(species)

        # 1st make a list of targets and the value to go to them (humans and enemies combined)
        combined_list = [] # [ [target , value , n_humans , n_enemies] , ... ]
        avoid_list = []    # [ target , ... ]
        avoid_to_swap = []
        
        for target in target_human:
            distance = float(distance_(dep , target))
            expected_value = compute_expected_outcome_value(E1=n_in_dep ,
                                                            E2=target.humans,
                                                            enemy=False)
            
            value = expected_value
            if distance != 0:
                value = expected_value/distance

            if expected_value < n_in_dep:
                avoid_list.append(target)
                avoid_to_swap.append([target , value , target.humans , 0])
            else:
                combined_list.append([target , value , target.humans , 0])


        
        for target in target_enemy:
            distance = float(distance_(dep , target))
            expected_value = compute_expected_outcome_value(E1=n_in_dep ,
                                                            E2=target.get_n_from_sp_int(ene_sp),
                                                            enemy=True)
            
            value = expected_value
            if distance != 0:
                value = expected_value/distance
            
            if expected_value < n_in_dep:
                avoid_list.append(target)
                avoid_to_swap.append([target , value , 0 , target.get_n_from_sp_int(ene_sp)])
            else:
                combined_list.append([target , value , 0 , target.get_n_from_sp_int(ene_sp)])


        # remove targets alread sent (used when there is splitting)
        combined_list_nse = []
        
        if len(sent_b_trg) == 0:
            combined_list_nse = combined_list
        else:
            for i in sent_b_trg:
                for j in combined_list:
                    if compare_place_pos(i , j[0]) == False:
                        combined_list_nse.append(j)

        
        if len(combined_list_nse) == 0:
            combined_list_nse = avoid_to_swap

        
        maxed_trg = max(combined_list_nse , key=lambda x: x[1])
        best_target = maxed_trg[0]
        sent_b_trg.append(best_target)






        # find bad targets and add them to an avoid list
        avoid_zones = []
        for avoid in avoid_list:
            avoid_zones += make_avoid_zone(avoid)
  
        print("avoid" , avoid_list)



        # Now find possible destination from dep
        possible_dest = find_possible_dest(pos=[dep.x , dep.y],
                                           grid=grid,
                                           dep_list=dep_list+avoid_list+avoid_zones)
        
        # Find which destination (from dep) is closest to the best_target
        dest_target = []
        for dest in possible_dest:
            distance = distance_(dest , best_target)
            dest_target.append([dest , distance])
        dest_target = min(dest_target , key=lambda x: x[1])
        best_dest = dest_target[0]

        print(f"from [{dep.x} {dep.y}] go to {best_dest}")
        

        
        # Send only needed amount
        n_humans = maxed_trg[2]
        n_enemies = maxed_trg[3]
        n_to_send = n_in_dep


        # Splitting
        """
        if n_humans == 0:
            if n_in_dep >= 1.5*n_enemies:
                n_to_send = 1.5*n_enemies
        elif n_enemies == 0:
            if n_in_dep >= n_humans:
                n_to_send = n_humans
        """


        # Now append this move to moves
        move = [dep.x , dep.y , n_to_send , best_dest[0] , best_dest[1]]
        moves.append(move)



    #print(f"send {len(moves)} --- {moves}")
    return len(moves) , moves





def make_avoid_zone (central_place):
    # Make zone 2 cells on all sides of central_place
    x = central_place.x
    y = central_place.y

    all_avoid_coord = [[x-1 , y-1],
                       [x   , y-1],
                       [x+1 , y-1],
                       [x+1 , y  ],
                       [x+1 , y+1],
                       [x   , y+1],
                       [x-1 , y+1],
                       [x-1 , y  ],
                       
                       [x-2 , y-2],
                       [x-1 , y-2],
                       [x   , y-2],
                       [x+1 , y-2],
                       [x+2 , y-2],
                       [x+2 , y-1],
                       [x+2 , y  ],
                       [x+2 , y+1],
                       [x+2 , y+2],
                       [x+1 , y+2],
                       [x   , y+2],
                       [x-1 , y+2],
                       [x-2 , y+2],
                       [x-2 , y+1],
                       [x-2 , y  ],
                       [x-2 , y-1]]
    
    out = [] # [Place]

    for coord in all_avoid_coord:
        out.append(Place([coord[0] , coord[1] , 0 , 0 , 0]))

    return out



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



def distance_(pos1 , pos2):
    x1 = None
    y1 = None
    x2 = None
    y2 = None

    if type(pos1) == Place:
        x1 = pos1.x
        y1 = pos1.y
    elif type(pos1) == list:
        x1 = pos1[0]
        y1 = pos1[1]
        
    if type(pos2) == Place:
        x2 = pos2.x
        y2 = pos2.y
    elif type(pos2) == list:
        x2 = pos2[0]
        y2 = pos2[1]

    return sqrt( (x1 - x2)**2 + (y1 - y2)**2 )



