from basic_structures.place import Place
from move_algorithms.helper_functions import *

"""
Currently working on this
"""


def compute_move_avoid(map_lists , grid):
        
        dep_list = map_lists[0]
        target_human = map_lists[1]
        target_enemy = map_lists[2]


        min_dist = 9999 # Large 1st dist, if smaller found, update
        best_dep = Place([0,0,0,0,0])
        best_hum = Place([0,0,0,0,0])


        for dep in dep_list:
            for hum in target_enemy:
                # calculate distance from all player to all humans
                dist = distance_in_moves(dep , hum)

                if dist < min_dist:
                    min_dist = dist
                    best_dep = dep
                    best_hum = hum
        
        print(f"d={min_dist} from {best_dep} to {best_hum}")

        # Now make the move
        possible_targets = avoid_walls([best_dep.x , best_dep.y] , grid)


        # Avoid enemies
        # ...
        pass



def manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


def convert_place_list_to_xy (places:[Place]):
    """
    converts [Place] to [(x,y)]
    """
    out = []
    for place in places:
        out.append((place.x , place.y))
    return out


def find_best_next_move(map_lists , grid):

    player_positions = convert_place_list_to_xy(map_lists[0])
    target_positions = convert_place_list_to_xy(map_lists[1])
    enemy_positions = convert_place_list_to_xy(map_lists[2])



    m, n = grid
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]  # Possible moves

    def is_valid_move(position):
        x, y = position
        return 0 <= x < m and 0 <= y < n and [x, y] not in enemy_positions

    def get_adjacent_positions(position):
        x, y = position
        adjacent_positions = [(x + dx, y + dy) for dx, dy in moves]
        return [pos for pos in adjacent_positions if is_valid_move(pos)]

    def a_star(start, goal):
        open_set = [(0, start)]  # Priority queue with (f_score, position)
        came_from = {}
        g_score = {pos: float('inf') for pos in player_positions}
        g_score[start] = 0

        while open_set:
            _, current = min(open_set)
            open_set.remove((_, current))
            if current == goal:
                path = [goal]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            for neighbor in get_adjacent_positions(current):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + manhattan_distance(neighbor, goal)
                    open_set.append((f_score, neighbor))

        return None  # No path found

    best_move = None
    best_distance = float('inf')

    for player_pos in player_positions:
        for target_pos in target_positions:
            path = a_star(player_pos, target_pos)
            if path and len(path) > 1:
                distance = len(path) - 1
                if distance < best_distance:
                    best_distance = distance
                    best_move = (path[1][0] - player_pos[0], path[1][1] - player_pos[1])

    print(f"Best move calc: {best_move} , dist: {best_distance}")
    
    return best_move

# Example usage:
player_positions = [(1, 1)]
target_positions = [(3, 3)]
enemy_positions = [[2, 1], [1, 2]]
grid_size = (5, 5)

best_move = find_best_next_move(player_positions, target_positions, enemy_positions, grid_size)
print("Best Move:", best_move)