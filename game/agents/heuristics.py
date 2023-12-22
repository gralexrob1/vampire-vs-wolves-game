"""
This file stores the heuristic explored.
Each heuristic function only takes state as argument.
All the functions that allow to compute metrics for the heuristics are stored in the metrics.py file.

max_ally_heuristic
"""


from heuristics.metrics import *


def max_ally_heuristic(state):
    """
    This heuristic rewards the maximization of ally numbers.

    Args
    ----
    state (list(Place)):
        List of groups on the map
    """

    allies = state[0]
    humans = state[1]
    enemies = state[2]

    ally_c = 0
    
    for place in allies:
        # we can sum because there is only on species 
        # in allies and only one species per place
        ally_c += place.vampires + place.werewolves
    
    return ally_c

