

import os
import socket
from consts import *


class ServerGame:
    def __init__(self, ip):

        self.client_sockets = []

        self.listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket.bind((socket.gethostname(), GAME_PORT))
        self.listening_socket.listen(2)
        while len(self.client_sockets) < PLAYERS_NUM:
            new_socket, new_address = self.listening_socket.accept()
            new_socket.send(COMMUNICATION_PASSWORD)
            if new_socket.recv(COMMUNICATION_PASSWORD_LEN) != COMMUNICATION_PASSWORD:
                print(f"Recived the wrong password from a client on {new_address}.")
                print("Abbandoning connection.")
                new_socket.close()
            else:
                print(f"Recived a new player from {new_address}")
                self.client_sockets.append(new_socket)