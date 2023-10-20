import random
from MapManager import Map_Manager , Move , Place


class Game_Manager:
    def __init__(self):
        self.grid = [0,0]
        self.houses = []
        self.start_pos = [0,0]
        self.start_map = []

        # not defined : -1 , vampires : 0 , werewolves : 1
        self.current_species = -1
        self.species_is_set = False

        #self.updated_map = [] # In map [(x , y , humans , vampires , werewolves)]
        self.initial_map_set = False

        self.received_data = [0 , 0 , 0 , 0] # [set , hum , hme , map]

        self.map = Map_Manager([] , -1)




    def set_current_species(self , start_map , start_pos):
        if self.species_is_set:
            return # guard statement ?
        
        # Takes in start_map and start_pos
        # Returns current species
        for object in start_map:
            if object[0] == start_pos[0] and object[1] == start_pos[1]:
                if object[3] != 0:
                    print("Playing as Vampires")
                    self.current_species = 0
                    self.map.species = 0
                    self.species_is_set = True
                elif object[4] != 0:
                    print("Playing as Werewolves")
                    self.current_species = 1
                    self.map.species = 1
                    self.species_is_set = True
                    
            

    def avoid_walls(self , pos , grid):
        # Takes in current pos [x,y] and grid size [m,n]
        # Returns list of all possible destinations [[x1,y1] , [x2,y2] , ...]
        x = pos[0]
        y = pos[1]
        max_y = grid[0]-1
        max_x = grid[1]-1
        
        all_dest = [
            [x-1 , y-1],
            [x   , y-1],
            [x+1 , y-1],
            [x+1 , y  ],
            [x+1 , y+1],
            [x   , y+1],
            [x-1 , y+1],
            [x-1 , y  ],
        ]

        possible_dest = []

        for dest in all_dest:
            if dest[0] >= 0 and dest[0] <= max_x and dest[1] >= 0 and dest[1] <= max_y:
                possible_dest.append(dest)

        #print(f"Possible dest : {possible_dest}")
        return possible_dest
    

    def compute_next_move(self , upd_array):
        # Takes in an_updated_map
        # Returns no of moves (int) , list of moves [[x1,y1,n,x2,y2] , ...]
        moves = []
        print(f"upd func : {upd_array}")

        self.map.change_with_upd(upd_array)
        dep_list = self.map.make_departure_list()
        
        for dep in dep_list:
            possible_targets = self.avoid_walls([dep.x , dep.y] , self.grid)


            if len(possible_targets) > 0:
                target_coord = possible_targets[random.randint(0 , len(possible_targets)-1)]
                    
                move = [dep.x , dep.y , 1 , target_coord[0] , target_coord[1]]
                moves.append(move)
                break # send only 1 move at a time ?
                
            
        
        print(f"Sending {len(moves)} moves : {moves}")
        return len(moves) , moves


    def compute_best_move(self , dep_list , target_human , target_enemy):
        # In :
        #   dep_list     [Place]
        #   target_human [Place]
        #   target_enemy [Place]
        #
        # Out :
        #   best Move

        dist = 100
        selected_target = Place([0,0,0,0,0])
        seleced_dep = Place([0,0,0,0,0])
        

        for t_h in target_human:
            for dep in dep_list:
                dist_n = self.map.calc_distance_moves(t_h , dep)
                if dist_n < dist:
                    dist = dist_n
                    selected_target = t_h
                    seleced_dep = dep
                    print(f"dep. : {dep} , target : {t_h}")


                

        pass




    def initial_game_update(self , message):
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
                self.map.change_with_updated_map(message[1] , save=True)
                print(f"initial map set {self.map.map}")
                #self.updated_map = message[1]
                
        if sum(self.received_data) == 4:
            # All data received
            self.set_current_species(self.start_map , self.start_pos)

