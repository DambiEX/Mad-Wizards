"""
TODO: make sure that no graphics are sent over the internet
finish seperating gui and game_engine
"""

from GUI import Gui
from consts import *
import pygame, sys, random, time
from pygame.locals import *


class GameEngine:
    """
    the main engine for the game. everything is stored and calculated here.
    players will not need to have this on their computer, they will only need the gui.
    does not do user events and graphics, that goes to the "gui" class.
    """
    def __init__(self):
        self.arena = self.get_arena()  # the game map.
        self.find_tiles_neighbours()  # finds the tiles sorrounding every tile.
        self.wizard_list = self.spawn_wizards()
        self.player_guis = []

    def get_arena(self):
        """
        generates a 2d game map.
        """
        arena = []

        for h in range(MAP_HEIGHT):
            arena.append([])
        for h in range(MAP_HEIGHT):
            for w in range(MAP_WIDTH):
                arena[w].append(Tile(w, h))  # 3rd parameter is tile type
        return arena

    def find_tiles_neighbours(self):
        """
        finds the tiles surrounding every tile.
        """
        for h in range(MAP_HEIGHT):
            for w in range(MAP_WIDTH):
                self.arena[w][h].find_neighbouring_tiles(self.arena)

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
            mock_hand.append([card.spell, card.direction])  # not the graphic so we dont send pics on the web.
        return mock_hand

    def send_info_to_gui(self, gui_number, new_hand):
        """
        sends a list of all the wizards as lists of [x, y, health, graphic] so the gui knows where everyone is.
        if send_hand: sends the hands of all of players as lists of [spell, direction],
        that the gui uses to find the right graphic.
        the players will send back the order and direction they want to play in another function.
        """

        wizard_info_list = []
        for wizard in self.wizard_list:
            wizard_info_list.append((wizard.x, wizard.y, wizard.health, wizard.graphic))
        self.player_guis[gui_number].mock_wizards_list = wizard_info_list
        if new_hand:
            self.player_guis[gui_number].update_hand(new_hand)  # TOMULTI: send different hands to different GUIs
        self.player_guis[gui_number].graphics()

    def execute_card(self, card):
        """
        actually executes the Card functions that were stored in the cards
        and are now stored in the cards_list
        """
        if card:  # handles the filler None objects.
            card.spells_dict[card.spell]()
        else:
            print("null card")
            return

    def execute_cards_list(self, cards_list):
        """
        :param cards_list: a list of Card objects.
        """
        while cards_list:
            self.execute_card(cards_list.pop(0))

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
            movement_cards_list = [None, None, None, None, None]   # list of Card objects. resets each turn
            for index, wizard in enumerate(self.wizard_list):  # every wizard plays 1 card
                # TODO: if played less than 2 cards:
                movement_cards_list[index] = wizard.hand[card_index]
            self.execute_cards_list(movement_cards_list)
            self.dont_crash_into_each_other()
            for wizard in range(len(self.wizard_list)):
                self.send_info_to_gui(wizard, False)  # updates graphics after every card is executed
            time.sleep(0.5)  # so we can see every card happening. <insert animation here> :P
            #  TODO: execute dmg list

        # TOMULTI: the gui will know to differentiate wizards based on the order of the list.

        for wizard in range(len(self.wizard_list)):
            self.player_guis[wizard].new_round()
            self.send_info_to_gui(wizard, self.get_cards_info_for_gui(self.wizard_list[wizard]))
            self.player_guis[wizard].send_data_to_game_engine()
            # TODO: everyone draws a new hand, instead of just resetting position

    def run_round(self):
        """
        gives wizards a set amount of time to rearrange their cards
        before the cards list executes.
        updates graphics in the meanwhile.
        """

        """start_time = time.time() + round_DURATION  # for when and if we want timer on the rounds
        while start_time-time.time() > 0.0:"""
        while True:
            for wizard in range(len(self.wizard_list)):
                self.player_guis[wizard].get_events()  # does stuff based on what the wizard clicks.
                self.player_guis[wizard].graphics()

    def run_game(self):

        # these are here because the gui needs to boot before we send it info.
        #TOMULTI do this for every gui with the correct hand
        for wizard in range(len(self.wizard_list)):
            self.player_guis.append(Gui(self, wizard))
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
    the rest of the class functions are function for every card.
    every function saves the details of the action a wizard makes.
    the action is executed by "execute_card" in game_engine.
    these functions include wizard movement and all wizard abilities.
    """

    def step(self):
        """
        moves a step in the path from move().
        :return: True if the step was made successfully.
        """
        target_tile = game_engine.arena[self.wizard.x][self.wizard.y].neighbours[self.direction]
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
    def __init__(self, x, y, image_file):
        self.x = x if x else 0
        self.y = y if y else 0
        self.graphic = image_file


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

    def find_neighbouring_tiles(self, arena):
        """
        finds the tiles that touch this one.
        """
        x = self.x
        y = self.y
        if y > 0:
            self.up_neighbour = arena[x][y - 1]
            self.neighbours[0] = self.up_neighbour
        if x < MAP_WIDTH - 1:
            self.right_neighbour = arena[x + 1][y]
            self.neighbours[1] = self.right_neighbour
        if y < MAP_HEIGHT - 1:
            self.down_neighbour = arena[x][y + 1]
            self.neighbours[2] = self.down_neighbour
        if x > 0:
            self.left_neighbour = arena[x - 1][y]
            self.neighbours[3] = self.left_neighbour


class Wizard(Thing):
    """
    players
    """
    def __init__(self, x, y, health, image_file):
        Thing.__init__(self, x, y, image_file)

        # stats:
        self.base_health = health
        self.health = self.base_health
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
        :param mock_hand: a list of lists with [spell, direction] received from the gui.
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


# maybe i will change later for the gui to init before game_engine.
game_engine = GameEngine()
game_engine.run_game()