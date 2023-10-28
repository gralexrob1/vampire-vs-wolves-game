from v2_basic_structure import *


def compare_place_pos(pos1:Place , pos2:Place) -> bool:
    """
    In:
        pos1    Place
        pos2    Place
    Out:
        if the places are the same   bool
    """
    return (pos1.x == pos2.x and pos1.y == pos2.y)


def distance_in_moves(pos1:Place , pos2:Place):
    """
    In:
        pos1    Place
        pos2    Place
    Out:
        minimum distance in units of moves   int
    """
    dx = abs(pos1.x - pos2.x)
    dy = abs(pos1.y - pos2.y)

    if dx > dy:
        min_diag = dy
        min_diag += dx - dy
        return min_diag
    else:
        min_diag = dx
        min_diag += dy - dx
        return min_diag


def avoid_walls(pos , grid):
    """
    In:
        pos    [x,y]
        grid   [m,n]
    Out:
        possible destinations [[x1,y1] , [x2,y2] , ...]
    """
    x = pos[0]
    y = pos[1]
    max_y = grid[0]-1
    max_x = grid[1]-1
        
    all_dest = [[x-1 , y-1],
                [x   , y-1],
                [x+1 , y-1],
                [x+1 , y  ],
                [x+1 , y+1],
                [x   , y+1],
                [x-1 , y+1],
                [x-1 , y  ]]

    possible_dest = []

    for dest in all_dest:
        if dest[0] >= 0 and dest[0] <= max_x and dest[1] >= 0 and dest[1] <= max_y:
            possible_dest.append(dest)
    return possible_dest