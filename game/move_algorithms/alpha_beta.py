import copy

from basic_structures.place import Place
from move_algorithms.helper_functions import *
from move_algorithms.simulation import *


def make_decision(map_lists, grid):
    
    dep_list = map_lists[0] # [Place] list where there are some of current species
    dep = dep_list[0]

    # Get species
    species = None
    if dep_list[0].vampires != 0:
        species = 0
    elif dep_list[0].werewolves != 0:
        species = 1
        
    # Apply alpha-beta
    best_move = None
    alpha = float('-inf')
    beta = float('inf')

    n_sp = dep.get_n_from_sp_int(species)
    possible_moves = find_possible_dest(pos = [dep.x , dep.y], 
                                        grid = grid,
                                        dep_list = dep_list)
    for move in possible_moves:
        new_map_lists = simulate_move(map_lists, move, species)
        value = alpha_beta_search(new_map_lists, grid, species, depth = 4, alpha=alpha, beta=beta, maximizing_player=True)
        if value > alpha:
            alpha = value
            best_move = [dep.x, dep.y, n_sp, move[0], move[1]]
    return 1, [best_move]


def alpha_beta_search(map_lists, grid, species, depth, alpha, beta, maximizing_player):
    """
    Template for a compute_move_function
    """

    # print("\n Call to function alpha_beta_search")
    # print("\t alpha_beta_search INPUTS")
    # print(f"\t\t map_lists = {map_lists}")


    if depth == 0:
        return evaluate(map_lists, species)

    dep_list = map_lists[0]
    dep = dep_list[0]
    
    if maximizing_player:
        # playing ally
        # max_value function

        value = float('-inf')
        n_sp = dep.get_n_from_sp_int(species)
        possible_moves = find_possible_dest(pos = [dep.x , dep.y], 
                                            grid = grid,
                                            dep_list = dep_list)
        for move in possible_moves:
            new_map_lists = simulate_move(copy.deepcopy(map_lists), move, species)
            value = max(value, alpha_beta_search(new_map_lists, grid, species , depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break  # Beta cut-off
        return value
    
    else:
        # playing enemy
        # min_value_function

        enemy_map_lists = copy.deepcopy(map_lists[::-1])
        enemy_species = 0 if species==1 else 1

        value = float('inf')
        n_sp = dep.get_n_from_sp_int(species)
        possible_moves = find_possible_dest(pos = [dep.x , dep.y], 
                                            grid = grid,
                                            dep_list = dep_list)
        for move in possible_moves:
            new_map_lists = simulate_move(copy.deepcopy(enemy_map_lists), move, enemy_species)
            value = min(value, alpha_beta_search(new_map_lists, grid, enemy_species, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cut-off
        return value
    




# ##########
# Heuristics
# ##########
    




# def evaluate(map_lists, species):
#     """
#     1. Comparison of populations
#     2. Humans in neighborhood
#     3. Enemies in neighborhood
#     """

#     dep_list = map_lists[0]     # [Place] list where there are some of current species
#     target_human = map_lists[1] # [Place] list of humans
#     target_enemy = map_lists[2] # [Place] list of enemies

#     # Factor to penalize if enemies are 1.5 times more numerous than us
#     enemy_factor = 1.5

#     # 1. Total number of our species in relation to enemies
#     if species == 0:
#         species_score = sum([dep.vampires for dep in dep_list])
#         enemy_score = sum([target_en.werewolves for target_en in target_enemy])
#     else:
#         species_score = sum([dep.werewolves for dep in dep_list])
#         enemy_score = sum([target_en.vampires for target_en in target_enemy])

#     species_enemy_ratio = species_score / max(1, (enemy_factor * enemy_score))

#     # 2. Number of humans in the vicinity
#     human_score = 0
#     for human in target_human:
#         distance = min([abs(dep.x - human.x) + abs(dep.y - human.y) for dep in dep_list])
#         if distance <= 2:  # Consider humans within a distance of 2
#             human_score += human.humans

#     # 3. Enemy numbers in the vicinity with a malus for 1.5 times more enemies
#     enemy_score_vicinity = 0
#     for enemy in target_enemy:
#         distance = min([abs(dep.x - enemy.x) + abs(dep.y - enemy.y) for dep in dep_list])
#         if distance <= 2:  # Consider enemies within a distance of 2
#             enemy_score_vicinity += enemy.vampires if species == 1 else enemy.werewolves

#     # Apply malus if enemies are 1.5 times more numerous than us
#     if enemy_score_vicinity > enemy_factor * species_score:
#         enemy_score_vicinity -= 0.5 * enemy_score_vicinity

#     # Combine scores with appropriate weights
#     total_score = 0.5 * species_enemy_ratio + 0.3 * human_score - 0.2 * enemy_score_vicinity

#     return total_score





def evaluate(map_lists, species):
    """
    Updated heuristic function to evaluate the state of the game.
    """

    # print('\n Call to function evaluate')
    # print("\t evaluate INPUT")
    # print(f"\t\t map_lists = {map_lists}")

    dep_list = map_lists[0]     # [Place] list where there are some of current species
    target_human = map_lists[1] # [Place] list of humans
    target_enemy = map_lists[2] # [Place] list of enemies

    # 0. a. Check Victory
    if not target_enemy:
        win = 1
    else: 
        win = 0

    # 1. Total number of our species in relation to enemies
    species_enemy_ratio = 0
    
    if species == 0:
        species_score = sum([dep.vampires for dep in dep_list])
        enemy_score = sum([target_en.werewolves for target_en in target_enemy])
    else:
        species_score = sum([dep.werewolves for dep in dep_list])
        enemy_score = sum([target_en.vampires for target_en in target_enemy])

    # species_enemy_ratio = species_score / max(1, (enemy_factor * enemy_score))
    # print(f"\t Ally vs Enemy: {species_enemy_ratio}")
        
    delta_species = species_score - enemy_score
    # print(f"\t Ally vs Enemy: {delta_species}")

    # 2. Nearest groups
    nearest_hum_i_can_eat , nearest_ene_i_can_eat , nearest_ene_that_can_eat_me = get_nearest_groups(map_lists, species)

    # Combine scores with appropriate weights
    w_win = 1000000
    w_delta = 10
    w_humans_to_eat = 1000
    w_enemies_to_eat = 800
    w_enemies_to_flee = 300

    total_score = w_win * win

    total_score += w_delta * delta_species
    # a potential augmentation of 5 allies would give:
    # for a weight = 100: score of 500
    # for a weight = 10: score of 50

    if nearest_hum_i_can_eat != 0:
        # we want to improve heuristic
        # when minimizing the distance
        # max distance is 15 (1/15 = 0.06)
        # w around 100 would give score around 6
        # w around 1000 would give score around 60
        total_score += 1 / nearest_hum_i_can_eat * w_humans_to_eat
    
    if nearest_ene_i_can_eat != 0:
        # we want to improve heuristic
        # when minimizing the distance
        # max distance is 15 (1/15 = 0.06)
        # w around 100 would give score around 6
        # w around 1000 would give score around 60
        # we prefer eating humans thatn enemies in general
        total_score += 1 / nearest_ene_i_can_eat * w_enemies_to_eat

    if nearest_ene_i_can_eat != 0:
        # we want to improve heuristic
        # when minimizing the distance
        # max distance is 15 (1/15 = 0.06)
        # w around 100 would give score around 6
        # w around 1000 would give score around 60
        # we prefer eating humans thatn enemies in general
        total_score += 1 / nearest_ene_i_can_eat * w_enemies_to_eat

    
    if nearest_ene_that_can_eat_me != 0:
        # we want to improve heuristic
        # when maximizing the distance
        # max distance is 15 (1/15 = 0.06)
        # w around 100 would give score around 6
        # w around 1000 would give score around 60
        # we want to flee only when near enemy (3 cases)
        total_score -=  w_enemies_to_flee * nearest_ene_that_can_eat_me # w / 3 ou w / 4 > les autres poids

    return total_score





# def evaluate(map_lists, species):
#     """
#     Updated heuristic function to evaluate the state of the game.
#     """
#     dep_list = map_lists[0]     # [Place] list where there are some of current species
#     target_human = map_lists[1] # [Place] list of humans
#     target_enemy = map_lists[2] # [Place] list of enemies

#     # Factor to penalize if enemies are 1.5 times more numerous than us
#     enemy_factor = 1.5

#     # 1. Total number of our species in relation to enemies
#     if species == 0:
#         species_score = sum([dep.vampires for dep in dep_list])
#         enemy_score = sum([target_en.werewolves for target_en in target_enemy])
#     else:
#         species_score = sum([dep.werewolves for dep in dep_list])
#         enemy_score = sum([target_en.vampires for target_en in target_enemy])

#     species_enemy_ratio = species_score / max(1, (enemy_factor * enemy_score))

#     # 2. Number of humans in the vicinity
#     human_score = 0
#     for human in target_human:
#         distance = min([abs(dep.x - human.x) + abs(dep.y - human.y) for dep in dep_list])
#         if distance <= 2:  # Consider humans within a distance of 2
#             human_score += human.humans

#     # 3. Enemy numbers in the vicinity with a malus for 1.5 times more enemies
#     enemy_score_vicinity = 0
#     for enemy in target_enemy:
#         distance = min([abs(dep.x - enemy.x) + abs(dep.y - enemy.y) for dep in dep_list])
#         if distance <= 2:  # Consider enemies within a distance of 2
#             enemy_score_vicinity += enemy.vampires if species == 1 else enemy.werewolves

#     # Apply malus if enemies are 1.5 times more numerous than us
#     if enemy_score_vicinity > enemy_factor * species_score:
#         enemy_score_vicinity -= 0.5 * enemy_score_vicinity

#     # Combine scores with appropriate weights
#     total_score = 5* species_enemy_ratio +  0* human_score - 0 * enemy_score_vicinity

#     return total_score





# def evaluate(map_lists, species, depth):
#     """
#     Updated heuristic function to evaluate the state of the game.
#     """
#     dep_list = map_lists[0]     # [Place] list where there are some of current species
#     target_human = map_lists[1] # [Place] list of humans
#     target_enemy = map_lists[2] # [Place] list of enemies

#     # Factor to penalize if enemies are 1.5 times more numerous than us
#     enemy_factor = 1.5
    
#     # 1. Total number of our species in relation to enemies
#     if species == 0:
#         species_score = sum([dep.vampires for dep in dep_list])
#         enemy_score = sum([target_en.werewolves for target_en in target_enemy])
#     else:
#         species_score = sum([dep.werewolves for dep in dep_list])
#         enemy_score = sum([target_en.vampires for target_en in target_enemy])

#     species_enemy_ratio = species_score - enemy_score

#     # 2. Number of humans in the vicinity
#     human_score = 0
#     for human in target_human:
#         distance = min([abs(dep.x - human.x) + abs(dep.y - human.y) for dep in dep_list])
#         if distance <= 3:  # Consider humans within a distance of 2
#             human_score += human.humans

#     # 3. Enemy numbers in the vicinity with a malus for 1.5 times more enemies
#     enemy_score_vicinity = 0
#     for enemy in target_enemy:
#         distance = min([abs(dep.x - enemy.x) + abs(dep.y - enemy.y) for dep in dep_list])
#         if distance <= 3:  # Consider enemies within a distance of 2
#             enemy_score_vicinity += enemy.vampires if species == 1 else enemy.werewolves

#     # Apply malus if enemies are 1.5 times more numerous than us
#     if enemy_score_vicinity > enemy_factor * species_score:
#         enemy_score_vicinity -= 0.5 * enemy_score_vicinity

#     # Combine scores with appropriate weights
#     total_score = 10 * species_enemy_ratio + 0.3 * human_score - 0.2 * enemy_score_vicinity

#     return total_score





# def evaluate(map_lists, species):
#     """
#     Heuristic function to evaluate the state of the game.
#     """
#     dep_list = map_lists[0]     # [Place] list where there are some of the current species
#     target_human = map_lists[1] # [Place] list of humans
#     target_enemy = map_lists[2] # [Place] list of enemies
#     dep = dep_list[0]
#     n_sp = dep.get_n_from_sp_int(species)

#     # Factor to penalize if enemies are 1.5 times more numerous than us
  
#     # 1. Total number of our species in relation to enemies
#     if species == 0:
#         species_score = sum([dep.vampires for dep in dep_list])
#         enemy_score = sum([target_en.werewolves for target_en in target_enemy])
#     else:
#         species_score = sum([dep.werewolves for dep in dep_list])
#         enemy_score = sum([target_en.vampires for target_en in target_enemy])

#     species_enemy_ratio = species_score - enemy_score

#     # 2. Number of humans in the nieghbordhood
#     human_score = 0
#     for human in target_human:
#         distance = distance_in_moves(dep, human) 
#         if dep.get_n_from_sp_int(species) > human.humans:
#             human_score += human.humans / max(1, distance)

#     # 3. Enemy numbers in the vicinity with a malus for 1.5 times more enemies
#     enemy_score_vicinity = 0
#     for enemy in target_enemy:
#         distance = distance_in_moves(dep, enemy) # Manhattan distance
#         if species == 0:
#             if n_sp > enemy.werewolves:
#                 enemy_score_vicinity += enemy.werewolves / max(1, distance)  # Avoid division by zero
#         else:
#             if n_sp > enemy.vampires:
#                 enemy_score_vicinity += enemy.vampires / max(1, distance)

#     # Combine scores with appropriate weights
#     total_score =  0.7*species_enemy_ratio  +  0.2*human_score - 0.1*enemy_score_vicinity

#     return total_score





# def evaluate(map_lists, species, depth):
#     """
#     Heuristic function to evaluate the state of the game.
#     """
#     dep_list = map_lists[0]     # [Place] list where there are some of the current species
#     target_human = map_lists[1] # [Place] list of humans
#     target_enemy = map_lists[2] # [Place] list of enemies
#     dep = dep_list[0]
#     n_sp = dep.get_n_from_sp_int(species)

#     # 1. Total number of our species in relation to enemies
#     if species == 0:
#         species_score = sum([dep.vampires for dep in dep_list])
#         enemy_score = sum([target_en.werewolves for target_en in target_enemy])
#     else:
#         species_score = sum([dep.werewolves for dep in dep_list])
#         enemy_score = sum([target_en.vampires for target_en in target_enemy])

#     species_enemy_diff = species_score - enemy_score

#    # distance_with_humans_diff
    
#     sp_distance_to_human = float('inf')
#     for human in target_human:
#         sp_distance_to_human = min(sp_distance_to_human, distance_in_moves(dep, human))
    
#     en_distance_to_human = float('inf')
#     for en in target_enemy:
#         for human in target_human:
#             en_distance_to_human = min(en_distance_to_human, distance_in_moves(en, human))
    
#     distance_with_humans_diff = sp_distance_to_human - en_distance_to_human
#     if depth < 3:
#         return 10*species_enemy_diff + distance_with_humans_diff
#     else :
#         return species_enemy_diff 
    

        
   
