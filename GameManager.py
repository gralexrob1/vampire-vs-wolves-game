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
            return # guard statement ?
        
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
    

    def compute_next_move(self , upd_array, strategy):
        """
        In:
            upd_array  (from the server)
            stategy    str
        Out:
            number of moves (int) , list of moves [[x1,y1,n,x2,y2] , ...]
        """
        #print(f"upd func : {upd_array}")

        self.map.change_with_upd(upd_array)
        dep_list = self.map.make_departure_list()
        targ_hum = self.map.make_target_list(human=True)
        targ_ene = self.map.make_target_list(enemy=True)

        if strategy == "strat_name":
            # return self.compute_move_function(dep_list , targ_hum , targ_ene)
            pass
        else:
            # default is random moves
            return self.compute_move_random(dep_list , targ_hum , targ_ene)
        
        
        
    def compute_move_template(self , dep_list , target_human , target_enemy):
        """
        In :
            dep_list     [Place]
            target_human [Place]
            target_enemy [Place]
        Out :
            best moves [dep.x , dep.y , 1 , target_coord[0] , target_coord[1]]
        """
        pass

    


    def compute_move_random(self , dep_list , target_human , target_enemy):
        """
        Example compute_move function
        Returns n of moves , [moves]
        """
        
        moves = []

        for dep in dep_list:
            possible_targets = self.avoid_walls([dep.x , dep.y] , self.grid)

            if len(possible_targets) > 0:
                target_coord = possible_targets[random.randint(0 , len(possible_targets)-1)] 
                move = [dep.x , dep.y , 1 , target_coord[0] , target_coord[1]]
                moves.append(move)
                break # send only 1 move at a time ?

        print(f"Sending {len(moves)} moves : {moves}")
        return len(moves) , moves

    
    def compute_move_avoid(self , dep_list , target_human , target_enemy):
        """
        Currently working on this
        """
        min_dist = 9999 # Large 1st dist, if smaller found, update
        best_dep = Place([0,0,0,0,0])
        best_hum = Place([0,0,0,0,0])


        for dep in dep_list:
            for hum in target_enemy:
                # calculate distance from all player to all humans
                dist = self.map.calc_distance_moves(dep , hum)

                if dist < min_dist:
                    min_dist = dist
                    best_dep = dep
                    best_hum = hum
        
        print(f"d={min_dist} from {best_dep} to {best_hum}")

        # Now make the move
        possible_targets = self.avoid_walls([best_dep.x , best_dep.y] , self.grid)


        # Avoid enemies
        # ...
        pass

    


    def initial_game_update(self , message):
        """
        In:
            message   sent from the server at the start of the game
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
                self.map.change_with_updated_map(message[1] , save=True)
                print(f"initial map set {self.map.map}")
                #self.updated_map = message[1]
                
        if sum(self.received_data) == 4:
            # All data received
            self.set_current_species(self.start_map , self.start_pos)

