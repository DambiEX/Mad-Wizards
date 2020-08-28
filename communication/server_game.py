 

import os
import socket
from select import select
from consts import *
import game_engine


class ServerGame:
    def __init__(self, ip, run=True):

        self.client_sockets = []

        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.game_engine = game_engine.GameEngine()

        if run:
            self.wait_for_players_connection()
            self.run_game()


    @property
    def connected_players(self):
        return len(self.client_sockets)

    def wait_for_players_connection(self):
        """
        Open the server socket and waits to recive players.
        """
        self.listening_socket.bind((socket.gethostname(), GAME_PORT))  # Open the server
        self.listening_socket.listen(PLAYERS_NUM)
        print(f"Waiting fo {PLAYERS_NUM} players to connect.")
        while self.connected_players < PLAYERS_NUM:
            new_socket, new_address = self.listening_socket.accept()
            if new_socket.recv(COMMUNICATION_PASSWORD_LEN) != COMMUNICATION_PASSWORD:
                print(f"Recived the wrong password from a client on {new_address}.")
                print("Abbandoning connection.")
                new_socket.close()
            else:
                print(f"Accepted a new player from {new_address}.")
                print(f"{self.connected_players} out of {PLAYERS_NUM} connected.")
                
                self.client_sockets.append(new_socket)
                self.send({CONNECTED_PLAYERS: self.connected_players})
        self.game_engine.start_game(self)

    def run_game(self):
        """
        The main game loop
        Checks for client actions, then executes them in the game_engine
        """
        while self.game_engine.in_proggress:
            read_sockets, _, _ = select(self.client_sockets, [], [], 10)
            for client_socket in read_sockets:
                information_str = client_socket.recv(4096)
                information = json.loads(information_str)
                self.game_engine.update(information)
            self.game_engine.check_for_actions(self)

    def send(self, json_object):
        """
        Sends a dict as a json string to all the clients.
        :type json_object: dict(str|any)
        """
        information = json.dumps(json_object)
        for client_socket in self.client_sockets:
            client_socket.send(information)
                


