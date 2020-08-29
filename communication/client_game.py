

import os
import socket
import json
from select import select
from com_consts import *
from packet_handler import PacketHandler
import GUI


class ClientGame:
    def __init__(self, ip):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((ip, GAME_PORT))
        
        # Send authentication to the server, to avoid port scanning
        server_socket.send(COMMUNICATION_PASSWORD)

        self.server_socket = PacketHandler(server_socket)
        
        self.gui = GUI.Gui()
        
        self.wait_for_players()

        self.run_game()

    def wait_for_players():
        """
        Waits for players connection, and starts the game once a que
        is recived from the server
        """
        start_game = False
        while not start_game:
            information = self.server_socket.recv()
            if START_GAME in information:
                start_game = information[START_GAME]
            self.gui.display_waiting_room(**information)
        
        self.gui.start_game(**self.server_socket.recv())

    def run_game(self):
        """
        Runs the game loop.
        """
        while True:
            # Check for new information from the server
            if self.server_socket.filno > 0:
                self.gui.update(**self.server_socket.recv())

            self.gui.load_events(self)
            self.gui.update_display()
