

import json


PACKET_LENGTH_INDICATOR_SIZE = 16


class PacketHandler:
    def __init__(self, socket):
        self.socket = socket

    def fileno(self):
        retirm self.socket.fileno()

    def send(self, json_object):
        data = json.loads(json_object)
        length = str(len(data)).zfill(PACKET_LENGTH_INDICATOR_SIZE)
        packet = length + data
        self.socket.send(packet)

    def recv(self):
        data = ""
        length_left = int(self.socket.recv(PACKET_LENGTH_INDICATOR_SIZE))
        while lengthlength_left > 0:
            new_data += self.socket.recv(length_left)
            length_left -= len(new_data)
            data += new_data
        return json.loads(data)
