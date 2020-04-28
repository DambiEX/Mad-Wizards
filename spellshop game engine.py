"""
TODO: fix cards not acting in correct order. in the gui they are represented well but the action is wrong
TODO: fix card graphics continue rotating if you press right right right.
"""


import pygame, sys, random, time
from pygame.locals import *  # TODO i have no fucking idea what this means. will research later.

# magic numbers:
SELECTOR = "selector"
NO_SELECTED_CARD = 69  # didnt want a None to be confused with a 0 so i made it clear.
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
STEP, MAGIC_MISSILES, PATIENCE = "step", "magic_missiles", "patience"

# dicts that hold all of the textures.
GRAPHICS_DICT = {
"floor" : pygame.image.load("FLOOR.bmp"),
"player" : pygame.image.load("PLAYER.bmp"),
"selector" : pygame.image.load("SELECTOR.bmp")
}
CARDS_GRAPHICS_DICT = {
STEP : pygame.image.load("TINY_STEP.bmp"),  # TODO: make it load "STEP" instead of "TINY_STEP"
MAGIC_MISSILES : pygame.image.load("MAGIC_MISSILES.bmp"),
PATIENCE : pygame.image.load("PATIENCE.bmp")
}

for i in GRAPHICS_DICT.items():  # makes all non-card textures transparent. including tiles, but that is not a problem.
    i[1].set_colorkey((255, 255, 255))

#CONSTS
#engine
MAP_WIDTH = 7
MAP_HEIGHT = 7
TILE_SIZE = 55
CARD_SIZE = int(TILE_SIZE * MAP_WIDTH / 5)
WINDOW_SIZE = (MAP_WIDTH * TILE_SIZE, (MAP_HEIGHT * TILE_SIZE) + CARD_SIZE)
TURN_DURATION = 8.0  # for when we play with a timer
# TODO: give every player a starting location
P1_STARTING_X = 3
P1_STARTING_Y = 5

# game rules:
HAND_SIZE = 5
CARDS_PLAYED_PER_ROUND = 2

UNIT_PARAM_DICT = {  # starting x, starting y, starting health
    "P1": (P1_STARTING_X, P1_STARTING_Y, 30)}


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

    def get_arena(self):
        """
        generates a 2d game map.
        """
        arena = []

        for h in range(MAP_HEIGHT):
            arena.append([])
        for h in range(MAP_HEIGHT):
            for w in range(MAP_WIDTH):
                arena[w].append(Tile(w, h, None))  # 3rd parameter is tile type  # TODO: make it generate the whole tiles in this function
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
        TODO: spawn more than one player
        """
        p1 = Wizard(*UNIT_PARAM_DICT["P1"], GRAPHICS_DICT["player"])
        wizard_list = [p1]  # TODO: , p2, p3, p4
        return wizard_list

    def send_wizards_info_to_gui(self):
        """
        sends only part of the info so you wont be able to read someone else's hand.
        theoretically, the gui will know to differentiate wizards based on the order of the list.
        :return: wizard_info_list, a list of wizards with only the details the gui needs to know.
        TODO: make it send directly to gui, instead of returning the list.
        """
        wizard_info_list = []
        for wizard in self.wizard_list:
            wizard_info_list.append((wizard.x, wizard.y, wizard.health, wizard.graphic))
        return wizard_info_list

    def send_card_info_to_gui(self):
        """
        sends the hands of all of players as a list of strings, that the gui uses to find the right graphic.
        the players will send the order and direction they want to play back in another function.
        """
        for wizard in self.wizard_list:
            mock_hand = []
            for card in wizard.hand:
                mock_hand.append(card.spell)  # not the graphic so we dont have to send pics on the web.
                gui.update_hand_display(mock_hand)  # TODO: send different hands to different GUIs

    def execute_action(self, action):
        """
        actually executes the Action objects that were stored in the cards
        and are now stored in the actions_list
        """
        if not action:  # handles the filler None objects.
            print("null action")
            return
        action.abilities_dict[action.ability]()

    def execute_actions_list(self, actions_list):
        """
        :param actions_list: a list of Action objects.
        """
        while actions_list:
            self.execute_action(actions_list.pop(0))

    def dont_crash_into_each_other(self):
        """
        see if 2 players are standing in the same tile, if they are,
        they move 1 tile back and this function is called again to check for new collisions.
        TODO: implement this when i have multiplayer
        """
        
        going_to_crash_into_each_other = False
        potential_collisions = []
        for wizard in self.wizard_list:
            potential_collisions.append(wizard.tile)

        # if more than 1 wizard is standing in a tile, its a collision
        forbidden_tiles = [tile for tile in potential_collisions if potential_collisions.count(tile) > 1]

        for wizard in self.wizard_list:
            if wizard.tile in forbidden_tiles:
                going_to_crash_into_each_other = True
                wizard.return_to_previous_location()  # moves a wizard 1 tile backwards. if he moved more than once it still moves him 1 tile.
                print("wizards crashed into each other")  # TODO: call the colliding player's name

        if going_to_crash_into_each_other:
            print("going up a recurse level in the wizard collision function")
            self.dont_crash_into_each_other()

        for wizard in self.wizard_list:  # empties the prev locations list before the next turn
            wizard.previous_locations = []
        
    def new_turn(self):
        """
        handles all the things that happen when a turn ends and a new one starts.
        TODO: implement damage_actions_list, and make dmg cards go there and only movement cards go to move_list
        """

        for card_index in range(HAND_SIZE):  # for every turn in the round
            movement_actions_list = [None, None, None, None]   # list of "action" objects. resets each turn
            for index, wizard in enumerate(self.wizard_list):  # every wizard plays 1 card
                # TODO: if played less than 2 cards:
                movement_actions_list[index] = wizard.hand[card_index].execute()
            self.execute_actions_list(movement_actions_list)
            self.dont_crash_into_each_other()
            gui.mock_wizards_list = self.send_wizards_info_to_gui()
            gui.graphics()  # update graphics after every action
            time.sleep(0.5)  # so we can see every action happening. <insert animation here> :P
            # execute dmg list

        #self.execute_actions_list(movement_actions_list)
        gui.mock_wizards_list = self.send_wizards_info_to_gui()
        self.send_card_info_to_gui()
        gui.new_turn()
        gui.graphics()

    def run_turn(self):
        """
        gives wizards a few seconds to choose their actions before the actions list executes.
        updates graphics in the meanwhile.
        """

        """start_time = time.time() + TURN_DURATION  # for when and if we want timer on the rounds
        while start_time-time.time() > 0.0:"""
        while True:
            gui.get_events()  # does stuff based on what the wizard clicks.
            gui.graphics()

    def run_game(self):

        # these are here because the gui needs to boot before we send it info.
        self.send_card_info_to_gui()
        gui.mock_wizards_list = self.send_wizards_info_to_gui()

        while True:
            self.run_turn()
            self.new_turn()


class Gui:
    """
    handles what the user sees and does. this is what every player has on their system.
    does not change the game in any way, only sends info to and from game_engine.
    TODO: not implemented: at the end of every turn send actions to "game_engine"
    """
    def __init__(self):
        pygame.init()  # opens the game window
        pygame.display.set_caption("The Game")
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.player = game_engine.wizard_list[0]  # TODO: every player gets a different wizard
        self.mock_wizards_list = []
        self.hand_display = []  # a list of card graphics to display. the info sent back is only the positions.
        self.selected_card = NO_SELECTED_CARD  # the card the player is interacting with. int 0-4. NO SELECT is 69
        self.card_playing_order = [0, 1, 2, 3, 4]  # the index is the order in the queue, the value is the card. starts identical.
        self.cards_direction = [UP, UP, UP, UP, UP]

    def new_turn(self):
        self.card_playing_order = [0, 1, 2, 3, 4]
        self.cards_direction = [UP, UP, UP, UP, UP]

    def update_hand_display(self, string_hand):
        graphics_hand = []
        for card in string_hand:
            graphics_hand.append([CARDS_GRAPHICS_DICT[card], UP])  # TODO: DEBUG!!!!
        self.hand_display = graphics_hand

    def graphics(self):
        """
        displays every "thing"(wizard, tile, card, card selector) on the screen.
        takes parameters from "game_engine"
        param wizard_list: list of (x, y, health, graphic)
        """
        for h in range(MAP_HEIGHT):  # draws the map
            for w in range(MAP_WIDTH):
                self.screen.blit(GRAPHICS_DICT["floor"], (h * TILE_SIZE, w * TILE_SIZE))

        for wizard in self.mock_wizards_list:  # displays all wizards
            self.screen.blit(wizard[3], (wizard[0] * TILE_SIZE, wizard[1] * TILE_SIZE))

        for index, card in enumerate(self.hand_display):
            rotated_card = pygame.transform.rotate(card, 360 - self.cards_direction[index] * 90)
            self.screen.blit(rotated_card,((1 + (CARD_SIZE * index)), (TILE_SIZE * MAP_HEIGHT)))  # draws the hand beneath the map

        """for index, card in enumerate(self.player.hand):
            self.screen.blit(card.graphic, ((1 + (CARD_SIZE * index)), (TILE_SIZE * MAP_HEIGHT)))  # draws the hand beneath the map
            """

        if self.selected_card != NO_SELECTED_CARD:  # it might be == 0.
            self.screen.blit(GRAPHICS_DICT[SELECTOR], ((1 + (CARD_SIZE * self.selected_card)), MAP_HEIGHT * TILE_SIZE))

        pygame.display.update()  # updates the display

    def get_events(self):
        """
        gets user input from mouse and keyboard
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:

                if event.key == K_SPACE:
                    game_engine.new_turn()   # TODO: seperate gui from game_engine

                if event.key == K_q:
                    self.send_data_to_game_engine()

                if self.selected_card != NO_SELECTED_CARD:
                    if event.key == K_LEFT:
                        self.rotate_card(LEFT)
                    elif event.key == K_RIGHT:
                        self.rotate_card(RIGHT)
                    elif event.key == K_DOWN:
                        self.rotate_card(DOWN)
                    elif event.key == K_UP:
                        self.rotate_card(UP)

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
                    elif event.key == K_6:
                        self.select_card(NO_SELECTED_CARD)  # cancel selection

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

            #else:
                #print(event)  # prints events for debugging

            """elif event.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()"""

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
        changes the order of cards in the gui output to the game engine
        also changes the graphics to display current card placement
        """
        if card_index >= new_pos:
            self.card_playing_order.insert(new_pos, self.card_playing_order[card_index])
            self.card_playing_order.pop(card_index+1)

            self.hand_display.insert(new_pos, self.hand_display[card_index])
            self.hand_display.pop(card_index + 1)

        else:
            self.card_playing_order.insert(new_pos+1, self.card_playing_order[card_index])
            self.card_playing_order.pop(card_index)

            self.hand_display.insert(new_pos + 1, self.hand_display[card_index])
            self.hand_display.pop(card_index)

    def rotate_card(self, new_direction):
        self.cards_direction[self.selected_card] = new_direction
        #self.hand_display[self.selected_card] = pygame.transform.rotate(self.hand_display[self.selected_card], 360 - new_direction * 90)
        self.select_card(NO_SELECTED_CARD)

    def send_data_to_game_engine(self):
        self.player.reorganize_cards(self.card_playing_order, self.cards_direction)


class Card:
    def __init__(self, wizard, spell, direction):
        self.owner = wizard
        self.spell = spell
        self.direction = direction
        self.action = None
        self.graphic = CARDS_GRAPHICS_DICT[spell]  # "step"

    def rotate(self, direction):
        self.graphic = pygame.transform.rotate(CARDS_GRAPHICS_DICT[self.spell], 360 - direction * 90)

    def execute(self):
        self.action = Action(self.spell, self.owner, self.direction)
        return self.action


class Action:
    """
    saves the details of the action a wizard makes.
    is executed by "execute_action" in game_engine. it selects the
    correct action from a dictionary, and executes its effects.
    this class includes wizard movement and all wizard abilities.
    """

    def __init__(self, ability, wizard, direction):
        """
        :param ability: string. what ability this action is.
        :param wizard: wizard. the wizard that makes the action.
        :param direction: the target direction for the action.
        """
        self.ability = ability
        self.wizard = wizard
        self.direction = direction

        self.abilities_dict = {
            STEP: self.step,  # 1 step in the direction
        }

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

    def distance(self, target):
        """
        returns manhattan distance between self and target
        """
        return abs(self.x - target.x) + abs(self.y - target.y)


class Tile(Thing):
    """
    map tiles. generated at the start of the game
    """
    def __init__(self, x, y, tile_type = None):
        Thing.__init__(self, x, y, None)
        self.wizard = None  # what wizards are standing on the tile.
        self.neighbours = [None, None, None, None]  # tiles touching this one
        self.left_neighbour, self.right_neighbour, self.up_neighbour, self.down_neighbour \
            = None, None, None, None
        self.tile_type = tile_type

        if not tile_type:  # chooses a tile type with different probability for rare type.
            tile_type = "floor"

        self.graphic = GRAPHICS_DICT[tile_type]
        self.tile_type = tile_type

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

        #stats:
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

    def reorganize_cards(self, order_list, direction_list):
        """
        :param order_list: list containing the ints 0-4 in the order the player organized
        :param direction_list: contains directions (int, 0-3) according to the index stored in order_list
        :return:
        """
        print("reorganizing cards")

        new_hand = []
        for card_index in order_list:
            new_hand.append(self.hand[card_index])
            new_hand[-1].direction = direction_list[card_index]

            #keeping this because there was a bug and im not sure its gone:
        """for i, card_index in enumerate(order_list):  # need 2 seperate loops because at first the list is not initialized.
            new_hand[i].direction = direction_list[card_index]  # TODO this line is suspicious for the bug
            print("card index: " + str(card_index))
            print("direction: " + str(new_hand[card_index].direction))"""
        self.hand = new_hand

    def move_to(self, tile):
        self.x = tile.x
        self.y = tile.y
        self.tile = tile
        tile.wizard = self
    
    def return_to_previous_location(self):
        if self.previous_locations:
            self.move_to(self.wizard.previous_locations.pop(0))


# maybe i will change later for the gui to init before game_engine.
game_engine = GameEngine()
gui = Gui()
game_engine.run_game()