"""
Define Place
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
