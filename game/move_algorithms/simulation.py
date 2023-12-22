"""
This file gathers all the functions allowing to simulate the game.
"""

import random

from basic_structures.place import Place


def simulate_move(map_lists, move, species): 

    # print("\n Call to function simulate_move")
    # print("\t simulate_move INPUTS")
    # print(f"\t\t map_lists = {map_lists}")
    # print(f"\t\t move = {move}")

    # allies
    dep_list = map_lists[0]     # [Place] list where there are some of current species
    dep = dep_list[0]
    n_sp = dep.get_n_from_sp_int(species)

    # others
    target_human = map_lists[1] # [Place] list of humans
    target_enemy = map_lists[2] # [Place] list of enemies


    # get coordinates
    dep_coordinates = coordinates_extractor(dep_list)
    human_coordinates = coordinates_extractor(target_human)
    enemy_coordinates = coordinates_extractor(target_enemy)


    ## Place vide

    if move not in (dep_coordinates + human_coordinates + enemy_coordinates):

        new_Place = Place([move[0],move[1],0, 0,0])
        new_Place.modify_n_sp(species, n_sp)  
        dep_list.remove(dep)
        dep_list.append(new_Place)
        
        return [dep_list, target_human, target_enemy]  
    
    ## Place where we already have species

    elif move in dep_coordinates:

        for dep in dep_list:
            n_sp_dest = dep.get_n_from_sp_int(species)
        n_sp = n_sp + n_sp_dest
        new_Place = Place([move[0],move[1],0,0,0])
        new_Place.modify_n_sp(species, n_sp) 
        dep_list.remove(dep)
        dep_list.append(new_Place)

        return [dep_list, target_human, target_enemy] 
    
    ## Humans on Place

    elif move in human_coordinates: 

        n_hum = None
        for hum in target_human:
            if [hum.x, hum.y] == move:
                n_hum = hum.humans # Number humans on the destination 
        
        if n_sp >= n_hum: # No battle if we are more than the humans 
            n_sp += n_hum
            n_hum = 0

        else: # Battle scenario

            surviving_humans = 0
            surviving_attackers = 0
            if random.random() <= battle_proba(n_sp, n_hum): # Win scenario
                for sp in range(n_sp):
                    if random.random() <= battle_proba(n_sp, n_hum):  # Each attacker has probability p to stay alive
                        surviving_attackers += 1
                for hum in range(n_hum):
                    if random.random() <= battle_proba(n_sp, n_hum):  # Each human has probability p to stay alive
                        surviving_humans += 1
                n_sp = surviving_attackers + surviving_humans
                n_hum = 0  

            else: # Lose scenario
                for hum in range(n_hum):
                    if random.random() >= battle_proba(n_sp, n_hum):  # Each human has probability 1-p to stay alive
                        surviving_humans += 1
                n_sp = 0
                n_hum = surviving_humans

        new_Place = Place([move[0],move[1],n_hum, 0, 0])
        new_Place.modify_n_sp(species, n_sp)  
        dep_list.remove(dep)
        dep_list.append(new_Place)

        return [dep_list, target_human, target_enemy] 

    ## Enemies on Place       
    
    elif move in enemy_coordinates: 
        n_en = None
        if species == 0: # Si on est vampires, ennemi est werewolves
            for en in target_enemy:
                if [en.x, en.y] == move:
                    n_en = en.werewolves
        else:
            for en in target_enemy: # Si on est werewolves, ennemi est vampires
                if [en.x, en.y] == move:
                    n_en = en.vampires
        
        if n_sp >= (1.5*n_en): # No battle if we are 1.5x more than ennemies
            n_sp = n_sp 
            n_en = 0
                    
        elif n_en >= (1.5*n_sp): # No battle if ennemies are 1.5x more than us
            n_en = n_en 
            n_sp = 0
                    
        else: # Battle
            #  n_sp == n_en OR n_sp < n_en OR n_en < n_sp < 1.5* n_en
            if random.random() <= battle_proba(n_sp, n_en): # Win scenario
                n_sp, n_en = battle_win(n_sp,n_en)
            else: # Lose scenario
                n_sp, n_en = battle_lose(n_sp, n_en)
            
        new_Place = Place([move[0],move[1],0,0,0])
        new_Place.modify_n_en(species, n_en)  
        new_Place.modify_n_sp(species, n_sp)  
        dep_list.remove(dep)
        dep_list.append(new_Place)
    
        return [dep_list, target_human, target_enemy] 
    
    else:
        return 404

    
def battle_proba(sp_1, sp_2):
    
    if sp_1 == sp_2:
        p = 0.5
    elif sp_1 < sp_2:
        p = sp_1/(2*sp_2)
    else:
        p = (sp_1/sp_2) - 0.5
    return p

def battle_win(sp_1,sp_2):

    surviving_attackers = 0
    for sp in range(sp_1):
        if random.random() <= battle_proba(sp_1, sp_2): 
            surviving_attackers += 1
    n_sp = surviving_attackers
    n_en = 0
    return n_sp, n_en

def battle_lose(sp_1, sp_2):
    
    surviving_ennemies = 0
    if random.random() >= battle_proba(sp_1, sp_2): # proba 1-p to survive
        surviving_ennemies += 1
    n_sp = 0
    n_en = surviving_ennemies
    return n_sp, n_en


def coordinates_extractor(Place_list):
    
    coordinates = []
    for Place in Place_list:
        coordinates.append([Place.x, Place.y])
    return coordinates
