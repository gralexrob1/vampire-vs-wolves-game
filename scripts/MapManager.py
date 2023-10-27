

class Place:
    def __init__(self , place_array):
        # [(x , y , humans , vampires , werewolves)]
        self.x = place_array[0]
        self.y = place_array[1]
        self.humans = place_array[2]
        self.vampires = place_array[3]
        self.werewolves = place_array[4]

    def __str__(self):
        return f"P[{self.x} {self.y} {self.humans} {self.vampires} {self.werewolves}]"
        
class Move:
    def __init__(self , move_array):
        # [x1 , y1 , n , x2 , y2]
        self.x1 = move_array[0]
        self.y1 = move_array[1]
        self.n = move_array[2]
        self.x2 = move_array[3]
        self.y2 = move_array[4]



class Map_Manager:
    def __init__(self , map_place_array , species):
        self.map = self.change_with_updated_map(map_place_array)
        #self.map_with_target = self.map
        self.species = species

        

    def change_with_updated_map(self , map_place_array , save=False) -> [Place]:
        map = []
        for place_array in map_place_array:
            map.append(Place(place_array))
        if save:
            self.map = map
        return map
    

    def change_with_upd(self , upd_array):
        out_map = []


        for place in self.map:
            update_found_for_place = False

            for update in upd_array:
                place_upd = Place(update)

                if self.compare_place_xy(place , place_upd):
                    update_found_for_place = True
                    out_map.append(place_upd)

            if not update_found_for_place:
                out_map.append(place)


        # Check all updates have been added (should happen above but doesn't ???)
        for update in upd_array:
            update_done = False

            place_upd = Place(update)
            for place in out_map:
                if self.compare_place_xy(place , place_upd):
                    update_done = True
            if not update_done:
                out_map.append(place_upd)


        ### Test
        for place in out_map:
            print(f"Place [{place.x} , {place.y} , {place.humans} , {place.vampires} , {place.werewolves}]")


        ### ---
        self.map = out_map

    

    def make_departure_list(self):
        # Return [Place] where there are species
        out = []
        for place in self.map:
            
            if self.species == 0:
                if place.vampires != 0:
                    out.append(place)
            elif self.species == 1:
                if place.werewolves != 0:
                    out.append(place)
        return out


    def make_target_list(self , human=False , enemy=False):
        # Return [Place] where there are human or enemy or both
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
        

        return out


    def clean_map(self):
        clean = []
        for part in self.map:
            if part.humans != 0 and part.vampires != 0 and part.werewolves != 0:
                clean.append(part)
        self.map = clean
    

    def __str__(self):
        out = ""
        for place in self.map:
            out += place.__str__()
        return out
    

    def compare_place_xy (self , pos1:Place , pos2:Place) -> bool:
        return (pos1.x == pos2.x and pos1.y == pos2.y)
        

    def calc_distance_moves(self , pos1:Place , pos2:Place):
        """
        In :
            pos1    Place
            pos2    Place
        Out :
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



