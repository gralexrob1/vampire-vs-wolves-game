"""
Define Place, Move
Printable, can return array version to send to the server
"""

class Place:
    def __init__(self , place_array):
        """
        place_array: [(x , y , humans , vampires , werewolves)]
        """
        self.x = place_array[0]
        self.y = place_array[1]
        self.humans = place_array[2]
        self.vampires = place_array[3]
        self.werewolves = place_array[4]

    def make_array(self):
        return [self.x , self.y , self.humans , self.vampires , self.werewolves]

    def __str__(self):
        return f"P[{self.x} {self.y} {self.humans} {self.vampires} {self.werewolves}]"


class Move:
    def __init__(self , move_array):
        """
        move_array: [x1 , y1 , n , x2 , y2]
        """
        self.x1 = move_array[0]
        self.y1 = move_array[1]
        self.n = move_array[2]
        self.x2 = move_array[3]
        self.y2 = move_array[4]

    def make_array(self):
        return [self.x1 , self.y1 , self.n , self.x2 , self.y2]
    
    def __str__(self):
        return f"M{self.x1} {self.y1} {self.n} {self.x2} {self.y2}"