"""
TOMULTI = TODO when i implement multiplayer
"""

from GUI import Gui
from consts import *
import pygame
import sys, random, time
from pygame.locals import *


class GameEngine:
    """
    the main engine for the game. everything is stored and calculated here.
    players will not need to have this on their computer, they will only need the gui.
    does not do user events and graphics, that goes to the "gui" file.
    """
    def __init__(self):
        self.game_board = self.get_game_board()  # the game map.
        self.wizard_list = self.spawn_wizards()
        self.player_GUIs = []

    def get_game_board(self):
        """
        generates a 2d game map.
        """
        game_board = []

        for h in range(MAP_HEIGHT):
            game_board.append([])
        for h in range(MAP_HEIGHT):
            for w in range(MAP_WIDTH):
                game_board[w].append(Tile(w, h))

        for h in range(MAP_HEIGHT):  # finds the tiles surrounding every tile.
            for w in range(MAP_WIDTH):
                game_board[w][h].find_neighbouring_tiles(game_board)

        return game_board

    def spawn_wizards(self):
        """
        makes a list of Wizard objects
        TOMULTI: spawn more than one player
        """
        p1 = Wizard(*UNIT_PARAM_DICT["P1"])
        wizard_list = [p1]  # TOMULTI: , p2, p3, p4
        return wizard_list

    def get_cards_info_for_gui(self, wizard):
        mock_hand = []
        for card in wizard.hand:
            mock_hand.append([card.spell, card.direction])  # not the graphic so we don't send pics on the web.
        return mock_hand

    def send_info_to_gui(self, gui_number, new_hand):
        """
        sends a list of all the wizards as lists of [x, y, health, graphic] so the gui knows where everyone is.
        if send_hand: sends the hands of the right player as a list of [spell, direction],
        that the gui uses to find the right graphic.
        the players will send back the order and direction they want to play in another function.
        """

        wizard_info_list = []
        for wizard in self.wizard_list:
            wizard_info_list.append((wizard.x, wizard.y, wizard.health, wizard.graphic))
        self.player_GUIs[gui_number].mock_wizards_list = wizard_info_list
        if new_hand:
            self.player_GUIs[gui_number].update_hand(new_hand)  # TOMULTI: send different hands to different GUIs
        self.player_GUIs[gui_number].graphics()

    def execute_cards_list(self, cards_list):
        """
        :param cards_list: a list of Card objects.
        """
        for card in cards_list:
            if card:  # handles the filler None objects.
                card.spells_dict[card.spell]()
            else:
                print("null card")
                return

    def dont_crash_into_each_other(self):
        """
        see if 2 players are standing in the same tile, if they are,
        they move 1 tile back and this function is called again to
        check for new collisions.
        TOMULTI: implement this when i have multiplayer
        """
        
        going_to_crash_into_each_other = False
        potential_collisions = []
        for wizard in self.wizard_list:
            potential_collisions.append(wizard.tile)

        # if more than 1 wizard is standing in a tile, its a collision
        forbidden_tiles = [tile for tile in potential_collisions
                           if potential_collisions.count(tile) > 1]

        for wizard in self.wizard_list:
            if wizard.tile in forbidden_tiles:
                going_to_crash_into_each_other = True
                wizard.return_to_previous_location()
                # moves a wizard 1 tile backwards. if he moved more than once it still moves him 1 tile.
                print("wizards crashed into each other")  # TOMULTI: call the colliding player's name

        if going_to_crash_into_each_other:
            print("going up a recurse level in the wizard collision function")
            self.dont_crash_into_each_other()

        for wizard in self.wizard_list:  # empties the prev locations list before the next round
            wizard.previous_locations = []
        
    def new_round(self):
        """
        this is a ROUND, not a TURN. there are 5 turns in a round.
        handles all the things that happen when a round ends and a new one starts.
        TODO: implement damage_cards_list, and make dmg cards go there and only movement cards go to move_list
        """

        for card_index in range(HAND_SIZE):  # for every turn in the round
            movement_cards_list = [None, None, None, None]   # list of Card objects. 1 per wizard. resets each turn
            for index, wizard in enumerate(self.wizard_list):  # every wizard plays 1 card
                # TODO: if played less than 2 cards:
                movement_cards_list[index] = wizard.hand[card_index]
            self.execute_cards_list(movement_cards_list)
            self.dont_crash_into_each_other()
            for wizard in range(len(self.wizard_list)):
                self.send_info_to_gui(wizard, False)  # updates graphics after every card is executed
            time.sleep(0.3)  # so we can see every card happening. <insert animation here> :P
            #  TODO: execute dmg list

        # TOMULTI: the gui will know to differentiate wizards based on the order of the list.
        for wizard in range(len(self.wizard_list)):
            self.player_GUIs[wizard].new_round()
            self.send_info_to_gui(wizard, self.get_cards_info_for_gui(self.wizard_list[wizard]))
            self.player_GUIs[wizard].send_data_to_game_engine()
            # TODO: everyone draws a new hand, instead of just resetting position

    def run_round(self):
        """
        gives wizards a set amount of time to rearrange their cards before the turn ends.
        right now infinite time, for testing.
        """

        """start_time = time.time() + round_DURATION  # for when and if we want timer on the rounds
        while start_time-time.time() > 0.0:"""
        while True:
            for wizard in range(len(self.wizard_list)):
                self.player_GUIs[wizard].get_events()  # does stuff based on what the wizard clicks.
                self.player_GUIs[wizard].graphics()

    def run_game(self):
        # this loop is here because the gui needs to boot before we send it info.
        # TOMULTI do this for every gui with the correct hand
        for wizard in range(len(self.wizard_list)):
            self.player_GUIs.append(Gui(self, wizard))
            self.send_info_to_gui(wizard, self.get_cards_info_for_gui(self.wizard_list[wizard]))

        while True:
            self.run_round()
            self.new_round()


class Card:
    def __init__(self, wizard, spell, direction):
        self.wizard = wizard
        self.spell = spell
        self.direction = direction

        self.spells_dict = {
            STEP: self.step,  # 1 step in the direction
        }

    """
    all of the class functions are function a for every spell.
    every function saves the details of the spell a wizard casts.
    the card is executed by "execute_card" in game_engine.
    these functions include wizard movement and all wizard spells.
    """

    def step(self):
        """
        :return: True if the step was made successfully.
        """
        target_tile = game_engine.game_board[self.wizard.x][self.wizard.y].neighbours[self.direction]
        if target_tile:  # if not out of the map
            self.wizard.previous_locations.append(self.wizard.tile)
            self.wizard.move_to(target_tile)
            return True
        else:
            print("out of the map")
            return False


class Thing:
    """
    class for things that have a location and will be displayed on the map.
    includes: wizards, tiles, the selector
    """
    def __init__(self, x, y, image_file_name):
        self.x = x if x else 0
        self.y = y if y else 0
        self.graphic = image_file_name


class Tile(Thing):
    """
    map tiles. generated at the start of the game
    """
    def __init__(self, x, y):
        Thing.__init__(self, x, y, None)
        self.wizard = None  # what wizards are standing on the tile.
        self.neighbours = [None, None, None, None]  # tiles touching this one
        self.left_neighbour, self.right_neighbour, self.up_neighbour, self.down_neighbour \
            = None, None, None, None
        self.graphic = "floor"

    def find_neighbouring_tiles(self, game_board):
        """
        finds the tiles that touch this one.
        """
        x = self.x
        y = self.y
        if y > 0:
            self.up_neighbour = game_board[x][y - 1]
            self.neighbours[0] = self.up_neighbour
        if x < MAP_WIDTH - 1:
            self.right_neighbour = game_board[x + 1][y]
            self.neighbours[1] = self.right_neighbour
        if y < MAP_HEIGHT - 1:
            self.down_neighbour = game_board[x][y + 1]
            self.neighbours[2] = self.down_neighbour
        if x > 0:
            self.left_neighbour = game_board[x - 1][y]
            self.neighbours[3] = self.left_neighbour


class Wizard(Thing):
    """
    players
    """
    def __init__(self, x, y, health, image_file_name):
        Thing.__init__(self, x, y, image_file_name)

        # stats:
        self.max_health = health
        self.health = health
        self.tile = None
        self.previous_locations = []
        self.hand = [Card(self, STEP, UP),
                     Card(self, STEP, UP),
                     Card(self, STEP, UP),
                     Card(self, STEP, UP),
                     Card(self, STEP, UP),
                     ]

    def reorganize_cards(self, mock_hand):
        """
        receives instructions from the gui, and assigns the correct order and
        direction to cards in hand.
        :param mock_hand: a list of short lists with [spell, direction] received from the gui.
        :return: new_hand: a list of cards with correct order and directions.
        """
        print("reorganizing cards")
        new_hand = [None, None, None, None, None]
        for mock_index, mock_card in enumerate(mock_hand):
            index_to_pop = None
            for real_index in range(len(self.hand)):  # real = in the game.engine hand
                if mock_card[0] == self.hand[real_index].spell:  # if the instructions match the spell
                    index_to_pop = real_index
            if index_to_pop is not None:  # one of the indexes is 0 so this syntax is needed
                new_hand[mock_index] = self.hand.pop(index_to_pop)
                new_hand[mock_index].direction = mock_card[1]
        self.hand = new_hand

    def move_to(self, tile):
        self.x = tile.x
        self.y = tile.y
        self.tile = tile
        tile.wizard = self
    
    def return_to_previous_location(self):
        if self.previous_locations:
            self.move_to(self.previous_locations.pop(0))


game_engine = GameEngine()
game_engine.run_game()
