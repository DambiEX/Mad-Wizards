import pygame, sys, random, time
from pygame.locals import *

# magic numbers:
SELECTOR = "selector"
NO_SELECTED_CARD = 69  # didn't want a None to be confused with a 0 so i made it clear.
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
# TOMULTI: give every player a starting location
PLAYER_STARTING_HEALTH = 30
P1_STARTING_X = 3
P1_STARTING_Y = 5

# game rules:
# NUMBER OF TURNS IN A ROUND = 5
HAND_SIZE = 5
CARDS_PLAYED_PER_ROUND = 2

UNIT_PARAM_DICT = {  # starting x, starting y, starting health
    "P1": (P1_STARTING_X, P1_STARTING_Y, PLAYER_STARTING_HEALTH, "player")}

# graphics:
GRAPHICS_DICT = {
    "floor": pygame.image.load("FLOOR.bmp"),
    "player": pygame.image.load("PLAYER.bmp"),
    "selector": pygame.image.load("SELECTOR.bmp")
    }
CARDS_GRAPHICS_DICT = {
    STEP: pygame.image.load("STEP.bmp"),
    MAGIC_MISSILES: pygame.image.load("MAGIC_MISSILES.bmp"),
    PATIENCE: pygame.image.load("PATIENCE.bmp")
    }

for i in GRAPHICS_DICT.items():  # makes all non-card textures transparent. including tiles, but that is not a problem.
    i[1].set_colorkey((255, 255, 255))
