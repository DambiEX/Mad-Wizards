import pygame, sys, random, time
from pygame.locals import *
from consts import *


class Gui:
    """
    Handles what the user sees and does. this is what every player has on their system.
    Does not change the game in any way, only sends info to and from game_engine.
    """
    def __init__(self, game_engine, player_number):
        pygame.init()  # opens the game window
        pygame.display.set_caption("Spellshop")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.game_engine = game_engine
        self.player_number = player_number  # game_engine.wizard_list[0]  # TOMULTI: every player gets a different wizard
        self.mock_wizards_list = []  # [x, y, health, graphic]
        self.selected_card = NO_SELECTED_CARD  # the card the player is interacting with. int 0-4. NO SELECT is 69
        self.hand = []

    def new_round_hand(self, cards_drawn):
        """
        Called at the start of every round in game_engine.new_round()
        :param cards_drawn: a list of strings
        """
        self.hand = [[card, UP] for card in cards_drawn]

    def graphics(self):
        """
        Displays every "thing"(wizard, tile, card, card selector) on the screen.
        Deceives parameters from "game_engine"
        self.mock.wizard_list = list of [x, y, health, graphic]
        """
        for h in range(MAP_HEIGHT):  # draws the map
            for w in range(MAP_WIDTH):
                self.screen.blit(GRAPHICS_DICT["floor"], (h * TILE_SIZE, w * TILE_SIZE))

        for wizard in self.mock_wizards_list:  # displays all wizards
            self.screen.blit(GRAPHICS_DICT[wizard[3]], (wizard[0] * TILE_SIZE, wizard[1] * TILE_SIZE))

        for index, card in enumerate(self.hand):  # draws the hand beneath the map
            rotated_card = pygame.transform.rotate(
                CARDS_GRAPHICS_DICT[card[0]], 360 - card[1] * 90)  # [0] is the type, [1] is the direction
            self.screen.blit(rotated_card, ((1 + (CARD_SIZE * index)),
                                            (TILE_SIZE * MAP_HEIGHT)))

        if self.selected_card != NO_SELECTED_CARD:  # the value 0 is allowed.
            self.screen.blit(GRAPHICS_DICT[SELECTOR], ((1 + (CARD_SIZE * self.selected_card)), MAP_HEIGHT * TILE_SIZE))

        pygame.display.update()  # updates the display

    def get_events(self):
        """
        Gets user input from mouse and keyboard
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:

                if event.key == K_SPACE:
                    self.game_engine.new_round()   # TODO: @amir seperate gui from game_engine

                if event.key == K_q:
                    self.send_data_to_game_engine()

                if self.selected_card != NO_SELECTED_CARD:
                    # Rotate the selected card.
                    if event.key == K_LEFT:
                        self.rotate_card(LEFT)
                    elif event.key == K_RIGHT:
                        self.rotate_card(RIGHT)
                    elif event.key == K_DOWN:
                        self.rotate_card(DOWN)
                    elif event.key == K_UP:
                        self.rotate_card(UP)

                    # Move cards around.
                    elif event.key == K_1:
                        self.relocate_card(0)
                    elif event.key == K_2:
                        self.relocate_card(1)
                    elif event.key == K_3:
                        self.relocate_card(2)
                    elif event.key == K_4:
                        self.relocate_card(3)
                    elif event.key == K_5:
                        self.relocate_card(4)
                    elif event.key == K_6:  # TODO: add "or esc"
                        self.select_card(NO_SELECTED_CARD)  # cancel selection

                # Choose which card to interact with.
                elif event.key == K_1:
                    self.select_card(0)
                elif event.key == K_2:
                    self.select_card(1)
                elif event.key == K_3:
                    self.select_card(2)
                elif event.key == K_4:
                    self.select_card(3)
                elif event.key == K_5:
                    self.select_card(4)
            """
            else:
                print(event)  # prints events for debugging

            elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
            """

    def send_data_to_game_engine(self):
        self.game_engine.wizard_list[self.player_number].reorganize_cards(self.hand)

    def select_card(self, selected_index):
        self.selected_card = selected_index
        self.graphics()

    def relocate_card(self, new_card_pos):
        """
        :param new_card_pos: an int in range 5
        """
        self.insert_card(self.selected_card, new_card_pos)
        self.select_card(NO_SELECTED_CARD)

    def insert_card(self, card_index, new_pos):
        """
        Changes the order of cards in the gui output to the game engine.
        Also changes the graphics to display current card placement.
        """
        if card_index >= new_pos:
            self.hand.insert(new_pos, self.hand[card_index])
            self.hand.pop(card_index+1)
        else:
            self.hand.insert(new_pos+1, self.hand[card_index])
            self.hand.pop(card_index)

    def rotate_card(self, new_direction):
        self.hand[self.selected_card][1] = new_direction
        self.select_card(NO_SELECTED_CARD)

