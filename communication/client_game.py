

import os
import socket
from consts import *


class ClientGame:
    def __init__(self, ip):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((ip, GAME_PORT))
        self.server_socket.send(COMMUNICATION_PASSWORD)
        if self.server_socket.recv(COMMUNICATION_PASSWORD_LEN) != COMMUNICATION_PASSWORD:
            print(f"Recived the wrong password from the server on {ip}:{GAME_PORT}.")
            print("Abbandoning connection.")
            self.server_socket.close()
            return
