import sys
import time
from client import ClientSocket
from argparse import ArgumentParser
import random
from GameManager import Game_Manager


GGs_game_manager = Game_Manager()




class args:
    def __init__(self , ip , port):
        self.ip = ip
        self.port = port


def play_game(strategy, args):
    client_socket = ClientSocket(args.ip, args.port)
    client_socket.send_nme("GGs AI")
    # set message
    message = client_socket.get_message()
    GGs_game_manager.initial_game_update(message)
    # hum message
    message = client_socket.get_message()
    GGs_game_manager.initial_game_update(message)
    # hme message
    message = client_socket.get_message()
    GGs_game_manager.initial_game_update(message)
    # map message
    message = client_socket.get_message()
    GGs_game_manager.initial_game_update(message)

    # start of the game
    while True:
        message  = client_socket.get_message()
        time_message_received = time.time()
        
        GGs_game_manager.initial_game_update(message)

        if message[0] == "upd":
            # Update : after opponent's turn
            nb_moves, moves = GGs_game_manager.compute_next_move(message[0], strategy=strategy)
            client_socket.send_mov(nb_moves, moves)
            


if __name__ == '__main__':

    ip = str(sys.argv[1])
    port = int(sys.argv[2])
    strategy = int(sys.argv[3])

    play_game(strategy=strategy , args=args(ip=ip , port=port))
