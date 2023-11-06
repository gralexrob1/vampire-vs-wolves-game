import sys
import time
from server_interaction.client import ClientSocket
from managers.game_manager import GameManager

game_manager = GameManager()


class args:
    def __init__(self , ip , port):
        self.ip = ip
        self.port = port


def play_game(strategy, args):
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
            nb_moves, moves = game_manager.request_next_move(message[1], strategy=strategy)
            client_socket.send_mov(nb_moves, moves)
            

if __name__ == '__main__':
    ip = str(sys.argv[1]) # "localhost"
    port = int(sys.argv[2]) # 5555
    strategy = str(sys.argv[3]) # "random" or "seek"
    play_game(strategy=strategy , args=args(ip=ip , port=port))
