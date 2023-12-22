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

    def __repr__(self):
        return f"P[{self.x} {self.y} {self.humans} {self.vampires} {self.werewolves}]"

    def get_n_from_sp_int(self , sp:int):
        """
        Get the number of species in Place from int value:
        vampires   : 0
        werewolves : 1

        In:
            sp      int
        Out:
            number  int
        """
        if sp == 0:
            return self.vampires
        elif sp == 1:
            return self.werewolves
        
    def get_species_in_place(self):
        """
        Get the current species in Place
        vampires   : 0
        werewolves : 1
        """
        if self.vampires != 0:
            return 0
        elif self.werewolves != 0:
            return 1
        
    def get_coords(self):
        return [self.x , self.y]
    
    def modify_n_sp(self , species:int , number:int):
        """
        Modify the number of species in Place
        vampires   : 0
        werewolves : 1
        """
        if species == 0:
            self.vampires += number
        elif species == 1:
            self.werewolves += number
        else:
            print("species not set")

    def modify_n_en(self , species:int , number:int):
        """
        Modify the number of enemy in Place
        vampires   : 0
        werewolves : 1
        """
        if species == 0:
            self.werewolves += number
        elif species == 1:
            self.vampires += number
        else:
            print("species not set")
    
