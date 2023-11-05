from managers.map_manager import MapManager
from managers.move_manager import MoveManager


class GameManager:
    """
    GameManager controls:
        the map
        the moves
    """

    def __init__(self):
        self.map = MapManager()

    
    def request_next_move(self, upd_array, strategy):
        """
        In:
            upd_array  (from the server)
            stategy    str
        Out:
            number of moves (int) , list of moves [[x1,y1,n,x2,y2] , ...]
        """
        # Get info form map
        self.map.change_with_upd(upd_array)
        dep_list = self.map.make_departure_list()
        target_human = self.map.make_target_list(human=True)
        target_enemy = self.map.make_target_list(enemy=True)

        map_lists = [dep_list , target_human , target_enemy]

        # Get info from move_manager
        move_manager = MoveManager()
        return move_manager.compute_move(strategy=strategy,
                                         map_lists=map_lists,
                                         grid=self.map.grid)