

import os
import socket
import json
from select import select
from consts import *
import GUI


class ClientGame:
    def __init__(self, ip):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.connect((ip, GAME_PORT))
        
        # Send authentication to the server, to avoid port scanning
        self.server_socket.send(COMMUNICATION_PASSWORD)
        
        self.gui = GUI.Gui()
        self.run_game()

    def run_game(self):
        """
        Runs the game loop.
        """
        while True:
            # Check shortly for new information from the server
            active_sockets, _, _ = select([self.server_socket], [], [], CLIENT_SELECT_TIME_OUT)
            if active_sockets:
                information_str = self.server_socket.recv(4096)
                information = json.loads(information_str)
                self.gui.update(information)

            self.gui.load_events(self)
            self.gui.update_display()

    def send(self, json_object):
        information = json.dumps(json_object)
        self.server_socket.send(information)
