from basic_structures.place import Place
from move_algorithms.helper_functions import *
from move_algorithms.helper_functions import distance_in_moves

class MapManager:
    def __init__(self):
        self.map = []                        # [Place]
        self.initial_map_set = False
        self.species = -1                    # not defined : -1 , vampires : 0 , werewolves : 1
        self.species_is_set = False
        self.received_data = [0 , 0 , 0 , 0] # [set , hum , hme , map]
        self.grid = [0,0]                    # [m,n]
        self.start_pos = [0,0]               # [x,y]


    def change_with_updated_map(self , map_place_array , save=False) -> [Place]:
        """
        In:
            map_place_array    [Place]
            save                bool
        Out:
            [Place]
        Overwrites the map with values from map_place_array
        """
        map = []
        for place_array in map_place_array:
            map.append(Place(place_array))
        if save:
            self.map = map
        return map


    def change_with_upd(self , upd_array):
        """
        In:
            upd_array   (from the server)
        
        Updates the map with the previous turn's moves
        """
        
        out_map = []
        for place in self.map:
            update_found_for_place = False
            for update in upd_array:
                place_upd = Place(update)
                if compare_place_pos(place , place_upd):
                    update_found_for_place = True
                    out_map.append(place_upd)
            if not update_found_for_place:
                out_map.append(place)
        # Check all updates have been added (should happen above but doesn't ???)
        for update in upd_array:
            update_done = False
            place_upd = Place(update)
            for place in out_map:
                if compare_place_pos(place , place_upd):
                    update_done = True
            if not update_done:
                out_map.append(place_upd)
        self.map = out_map




    def make_target_list(self , human=False , enemy=False , dep=False):
        """
        Return [Place] where there are human or enemy or both
        """
        out = []
        for place in self.map:
            if human:
                if place.humans != 0:
                    out.append(place)
            if enemy:
                if self.species == 0:
                    if place.werewolves != 0:
                        out.append(place)
                elif self.species == 1:
                    if place.vampires != 0:
                        out.append(place)
            if dep:
                out = []
                for place in self.map:
                    if self.species == 0:
                        if place.vampires != 0:
                            out.append(place)
                    elif self.species == 1:
                        if place.werewolves != 0:
                            out.append(place)

        return out


    def clean_map(self):
        """
        Removes Place in map is there is no one on it
        """
        clean = []
        for part in self.map:
            if part.humans != 0:
                clean.append(part)
            elif part.vampires != 0:
                clean.append(part)
            elif part.werewolves != 0:
                clean.append(part)
        self.map = clean
    

    def find_species(self , start_map , start_pos):
        """
        In:
            start_map   [(x , y , humans , vampires , werewolves)]
            start_pos   [x , y]

        Set the current species:
            not defined :-1 
               vampires : 0
             werewolves : 1
        """
        if self.species_is_set:
            return
        for object in start_map:
            if object[0] == start_pos[0] and object[1] == start_pos[1]:
                if object[3] != 0:
                    print("Playing as Vampires")
                    self.current_species = 0
                    self.species = 0
                    self.species_is_set = True
                elif object[4] != 0:
                    print("Playing as Werewolves")
                    self.current_species = 1
                    self.species = 1
                    self.species_is_set = True


    def initial_game_update(self , message):
        """
        In:
            message     sent from the server at the start of the game
        """
        if message[0] == "set":
            self.grid = message[1]
            self.received_data[0] = 1
        elif message[0] == "hum":
            self.houses = message[1]
            self.received_data[1] = 1
            #print("HOUSES" , self.houses)
        elif message[0] == "hme":
            self.start_pos = message[1]
            self.received_data[2] = 1
        elif message[0] == "map":
            self.start_map = message[1]
            self.received_data[3] = 1

            if not self.initial_map_set:
                self.initial_map_set = True
                self.change_with_updated_map(message[1] , save=True)
                print(f"initial map set {self.map}")
                
        if sum(self.received_data) == 4:
            # All data received
            self.find_species(self.start_map , self.start_pos)


    def __str__(self):
        out = ""
        for place in self.map:
            out += place.__str__()
        return out



    def total_number(self , human:bool=False , vampires:bool=False , werewolves:bool=False):
        """
        Return the total number of humans or vampires of werewolves in the map
        """
        n_human = 0
        n_vampi = 0
        n_wolve = 0

        for place in self.map:
            n_human += place.humans
            n_vampi += place.vampires
            n_wolve += place.werewolves

        if human:
            return n_human
        elif vampires:
            return n_vampi
        elif werewolves:
            return n_wolve


    def longest_distance(self):
        """
        Out: the longest distance (in moves) of the given map,
             from top left corner to bottom right corner.
        """ 
        return distance_in_moves([0,0] , self.grid)


    def apply_moves(self , move_list , save=False , debug=False):
        """
        ----- Experimental -----
        In:
            move_list    [Move]
            save          bool

        Apply [Move] to MapManager.map (instead of upd_list from server)
        Requires that MapManager.species has been set
        """
        print("IN MAP :" , self.map) if debug else None
        
        out_map = self.map
        for move in move_list:
            print(move) if debug else None
            # Remove from origin
            for i , place in enumerate(out_map):
                if place.x == move.x1 and place.y == move.y1:
                    out_map[i].modify_n_sp(self.species , -move.n)
                    
            # Add at destination
            place_in_map = False
            for i , place in enumerate(out_map):
                if place.x == move.x2 and place.y == move.y2:
                    place_in_map = True
                    out_map[i].modify_n_sp(self.species , move.n)

            if place_in_map == False:
                new_place = Place([move.x2 , move.y2 , 0 , 0 , 0])
                new_place.modify_n_sp(self.species , move.n)
                out_map.append(new_place)

        if save:
            self.map = out_map
            self.clean_map()
            print("OUT MAP :" , self.map) if debug else None
