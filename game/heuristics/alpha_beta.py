from heuristics.heuristics import *


class AlphaBeta:


    def __init__(self, heuristic, depth, alpha, beta, allies, humans, ennemies):

        self.heuristic = heuristic
        self.depth = depth
        self.alpha = alpha
        self.beta = beta

        self.allies = allies
        self.humans = humans
        self.ennemies = ennemies
    

    def get_move_combination(self):
        
        allies_legal_moves = list()

        for ally in self.allies:

            legal_moves = find_possible_dest(
                pos = [ally.x , ally.y], 
                grid = grid,
                dep_list = dep_list
            )


    def search(self, state, depth, alpha, beta, maximizing_player):

        if depth == 0 or game_is_over(state):
            return heuristic(state)

        if maximizing_player:
            value = value = float('-inf')

            for move in generate_moves(state):
                new_state = make_move(state, move)
                value = max(value, alpha_beta_search(new_state, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cut-off
            return value
        
        else:
            value = infinity
            for move in generate_moves(state):
                new_state = make_move(state, move)
                value = min(value, alpha_beta_search(new_state, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cut-off
            return value





def compute_move_alpha_beta(map_lists, grid, heuristic, depth, alpha, beta, maximizing_player):
    """
    Main for alpha beta execution
    """    

    allies_list = map_lists[0] # [Place] list where there are some of current species
    human_list = map_lists[1] # [Place] list of humans
    ennemy_list = map_lists[2] # [Place] list of enemies
 
    if maximizing_player:
        value = float('-inf')
        for dep in dep_list:
            possible_moves = find_possible_dest(pos = [dep.x , dep.y], 
                                                grid = grid,
                                                dep_list = dep_list)
            for move in possible_moves:
                new_state = make_move(move)
                value = max(value, compute_move_alpha_beta(new_state, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cut-off
        return value
    else:
        value = float('inf')
        for move in find_possible_dest(pos = [dep.x , dep.y], 
                                                grid = grid,
                                                dep_list = dep_list):
            new_state = make_move(state, move)
            value = min(value, alpha_beta_search(new_state, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cut-off







def alpha_beta_search(state, depth, alpha, beta, maximizing_player):

    if depth == 0 or game_is_over(state):
        return heuristic(state)

    if maximizing_player:
        value = -infinity
        for move in generate_moves(state):
            new_state = make_move(state, move)
            value = max(value, alpha_beta_search(new_state, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            if beta <= alpha:
                break  # Beta cut-off
        return value
    
    else:
        value = infinity
        for move in generate_moves(state):
            new_state = make_move(state, move)
            value = min(value, alpha_beta_search(new_state, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            if beta <= alpha:
                break  # Alpha cut-off
        return value
