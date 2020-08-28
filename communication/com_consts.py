

import sys
sys.path.append("../")

import pygame
pygame.init()




# lobby consts
FONT = pygame.font.SysFont('comicsans', 30)
SCREEN_WIDTH = 500  # 1 / root(2) proportion. like A4
SCREEN_HIGET = 320
NORMAL_COLOR = [255, 255, 255, 255]
HOVER_COLOR = [200, 200, 200, 255]
TEXT_BLINKING_CYCLE_LENGTH = 1.0
BUTTONS = {
    "IP": {
        "normal_color": NORMAL_COLOR,
        "hover_color": [200, 200, 200, 255],
        "x": 100,
        "y": 160,
        "width": 300,
        "height": 40,
        "text": "Join IP"
    },
    "HOST": {
        "normal_color": NORMAL_COLOR,
        "hover_color": HOVER_COLOR,
        "x": 100,
        "y": 240,
        "width": 300,
        "height": 40,
        "text": "Host a game"
    }
}
IP_ENTER_PARMS = {
    "x": 100,
    "y": 100,
    "width": 300,
    "height": 40,
    "text": "",
    "defualt_text": "123.456.789.0"
}

LOBBY_BACKGROUND_IMAGE = pygame.image.load(r"lobby_background.png")

#Communication
GAME_PORT = 16969
COMMUNICATION_PASSWORD = "Sp31l5h0p"
COMMUNICATION_PASSWORD_LENGTH = len(COMMUNICATION_PASSWORD)
PLAYERS_NUM = 2
CLIENT_SELECT_TIME_OUT = 0.05

# json params
CONNECTED_PLAYERS = "CONNECTED_PLAYERS"
CARDS_DRAWN = "CARDS_DRAWN"


