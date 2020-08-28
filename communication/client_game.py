

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
        
        self.wait_for_players()

        self.run_game()

    def wait_for_players():
        """
        Waits for players connection, and starts the game once a que
        is recived from the server
        """
        start_game = False
        while not start_game:
            information = self.recv()
            if START_GAME in information:
                start_game = information[START_GAME]
            self.gui.display_waiting_room(**information)
        information = self.recv()
        self.gui.start_game(**information)

    def run_game(self):
        """
        Runs the game loop.
        """
        while True:
            # Check shortly for new information from the server
            active_sockets, _, _ = select([self.server_socket], [], [], CLIENT_SELECT_TIME_OUT)
            if active_sockets:
                information = self.recv()
                self.gui.update(**information)

            self.gui.load_events(self)
            self.gui.update_display()

    def recv(self):
        """
        Recives json from the server, and loads it into a dict
        :rtype: dict(str|any)
        """
        information_str = self.server_socket.recv(4096)
        return json.loads(information_str)

    def send(self, json_object):
        """
        Sends a dict as a json string to the server.
        :type json_object: dict(str|any)
        """
        information_str = json.dumps(json_object)
        self.server_socket.send(information_str)
