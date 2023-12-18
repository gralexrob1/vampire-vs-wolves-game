import sys
import time
from server_interaction.client import ClientSocket
from managers.game_manager import GameManager


class Args:
    def __init__(self, ip="localhost", port=5555, strategy='random'):
        self.ip = ip
        self.port = port
        self.strategy = strategy


def play_game(args):

    game_manager = GameManager()

    client_socket = ClientSocket(args.ip, args.port)
    client_socket.send_nme("GGs AI v2")
    
    # set message
    message = client_socket.get_message()
    game_manager.map.initial_game_update(message)
    # hum message
    message = client_socket.get_message()
    game_manager.map.initial_game_update(message)
    # hme message
    message = client_socket.get_message()
    game_manager.map.initial_game_update(message)
    # map message
    message = client_socket.get_message()
    game_manager.map.initial_game_update(message)

    # start of the game
    while True:
        message  = client_socket.get_message()
        time_message_received = time.time()
        
        game_manager.map.initial_game_update(message)

        if message[0] == "upd":
            # Update : after opponent's turn
            nb_moves, moves = game_manager.request_next_move(message[1], strategy=args.strategy)
            client_socket.send_mov(nb_moves, moves)
            

if __name__ == '__main__':

    args =  Args(
        ip = str(sys.argv[1]),
        port = int(sys.argv[2]),
        strategy = str(sys.argv[3])
    )

    play_game(args)
