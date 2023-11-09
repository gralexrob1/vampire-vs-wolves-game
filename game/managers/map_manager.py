from basic_structures.place import Place
from move_algorithms.helper_functions import *


class MapManager:
    def __init__(self):
        self.map = [] # [Place]
        self.initial_map_set = False
        self.species = -1 # not defined : -1 , vampires : 0 , werewolves : 1
        self.species_is_set = False
        self.received_data = [0 , 0 , 0 , 0] # [set , hum , hme , map]
        self.grid = [0,0]
        self.start_pos = [0,0]


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
                    if place.vampires != 0:
                        out.append(place)
                elif self.species == 1:
                    if place.werewolves != 0:
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
            if part.humans != 0 and part.vampires != 0 and part.werewolves != 0:
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
