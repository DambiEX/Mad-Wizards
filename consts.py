import pygame, sys, random, time
from pygame.locals import *

# magic numbers:
SELECTOR, WHITE_FLOOR, BLACK_FLOOR = "selector", "white floor", "black floor"
P1, P2, P3, P4 = 0, 1, 2, 3
NO_SELECTED_CARD = "no_selected_card"  # didn't want a None to be confused with a 0 so i made it clear.
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
# spells:
STEP, MAGIC_MISSILES, PATIENCE = "step", "magic_missiles", "patience"

# CONSTS
# engine
MAP_WIDTH = 7
MAP_HEIGHT = 7
TILE_SIZE = 55
CARD_SIZE = int(TILE_SIZE * MAP_WIDTH / 5)
WINDOW_SIZE = (MAP_WIDTH * TILE_SIZE, (MAP_HEIGHT * TILE_SIZE) + CARD_SIZE)
round_DURATION = 8.0  # for when we play with a timer
turn_animation_time = 0.3
# TOMULTI: give every player a starting location
PLAYER_STARTING_HEALTH = 30
P1_STARTING_X = 3
P1_STARTING_Y = 5

# game rules:
# NUMBER OF TURNS IN A ROUND = 5
HAND_SIZE = 5
CARDS_PLAYED_PER_ROUND = 2

PLAYERS_PARAMETERS_LIST = [  # starting x, starting y, starting health
    (P1_STARTING_X, P1_STARTING_Y, PLAYER_STARTING_HEALTH, P1)
    # TOMULTI: p1, p2, p3
    ]

# graphics:
GRAPHICS_DICT = {
    WHITE_FLOOR: pygame.image.load("WHITE_FLOOR.bmp"),
    BLACK_FLOOR: pygame.image.load("BLACK_FLOOR.bmp"),
    P1: pygame.image.load("P1.bmp"),
    SELECTOR: pygame.image.load("SELECTOR.bmp")
    }
CARDS_GRAPHICS_DICT = {
    STEP: pygame.image.load("STEP.bmp"),
    MAGIC_MISSILES: pygame.image.load("MAGIC_MISSILES.bmp"),
    PATIENCE: pygame.image.load("PATIENCE.bmp")
    }

for i in GRAPHICS_DICT.items():  # makes all non-card textures transparent. including tiles, but that is not a problem.
    i[1].set_colorkey((255, 255, 255))
