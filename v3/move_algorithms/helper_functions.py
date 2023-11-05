from basic_structures.place import Place



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


def find_possible_dest (pos , grid , dep_list):
    """
    In:
        pos       [x,y]
        grid      [m,n]
        dep_list  [Place]
    Out:
        possible destinations [[x1,y1] , [x2,y2] , ...]

    Find the possible destinations around pos, given that the departure places
    are not valid destinations
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
    
    # possible dest is avoid walls here

    out = []

    for dest in possible_dest:

        is_poss = True
        for place in dep_list:
            if place.x == dest[0] and place.y == dest[1]:
                is_poss = False
                break

        if is_poss:
            out.append(dest)

    # out is avoid walls + avoid departure places
    return out
