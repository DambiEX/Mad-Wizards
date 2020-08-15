

import os
import pygame
pygame.init()
import time


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

LOBBY_BACKGROUND_IMAGE = pygame.image.load(r"images\lobby_background.png")


class Button:
    """
    Class to represent a lobby gui button
    """
    def __init__(self, normal_color, hover_color, x, y, width, height, text=''):
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.color = self.normal_color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline=(0, 0, 0)):
        """
        Draw the button
        """
        #Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
            
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            
            text = FONT.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_hovering(self, x, y):
        """
        Check if the cordinations x, y are on the button
        """
        if x > self.x and x < self.x + self.width:
            if y > self.y and y < self.y + self.height:
                return True
        
        return False

    def update_hovering(self, x, y):
        """
        Updates the button
        """
        if not self.is_hovering(x, y):
            self.color = self.normal_color
        else:
            self.color = self.hover_color


class InputBox:
    """
    Class to represent a lobby gui textbox
    """
    def __init__(self, x, y, width, height, text, defualt_text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = NORMAL_COLOR
        self.text = text
        self.defualt_text = defualt_text
        self.defualt_text_active = "|" + self.defualt_text[1:]
        self.txt_surface = FONT.render(defualt_text, True, self.color)
        self.active = False

    def handle_event(self, event):
        """
        Updates the the inbox accroding to the event
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = NORMAL_COLOR if not self.active else HOVER_COLOR
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.

    def update_text(self):
        """
        Changes the text for the "typing" feelings
        """
        text = ""

        if self.text:
            if self.active and time.time() % TEXT_BLINKING_CYCLE_LENGTH > TEXT_BLINKING_CYCLE_LENGTH / 2:
                text = self.text + "|" 
            else:
                text = self.text
        else:
            if self.active and time.time() % TEXT_BLINKING_CYCLE_LENGTH > TEXT_BLINKING_CYCLE_LENGTH / 2:
                text = self.defualt_text_active
            else:
                text = self.defualt_text
            
        self.txt_surface = FONT.render(text, True, self.color)

    def draw(self, screen):
        """
        Draws the Input Box
        """
        # Update the text surface
        self.update_text()
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class GameLobby:
    """
    The game lobby application class
    """
    def __init__(self, run_lobby=False):
        
        self.screen = None
        self.mouse_x = 0
        self.mouse_y = 0

        self.buttons = {name: Button(**button_values)
                        for name, button_values in BUTTONS.items()}
        self.ip_input_box = InputBox(**IP_ENTER_PARMS)

        if run_lobby:
            self.run_lobby()

    def run_lobby(self):
        """
        Runs the lobby
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HIGET))
        for i in range(3000000):
            self.update_screen()
            

    def update_screen(self):
        """
        Updates the screen
        """

        self.screen.blit(LOBBY_BACKGROUND_IMAGE, LOBBY_BACKGROUND_IMAGE.get_rect())
        for event in pygame.event.get():
            self.handle_event(event)
        
        for button in self.buttons.values():
            button.update_hovering(self.mouse_x, self.mouse_y)
            button.draw(self.screen)

        self.ip_input_box.draw(self.screen)

        pygame.display.flip()

    def handle_event(self, event):
        """
        Handle event
        """
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

        self.ip_input_box.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.buttons["IP"].is_hovering(self.mouse_x, self.mouse_y):
                self.connect_to_game(self.ip_input_box.text)
            
        if event.type == pygame.QUIT:
            print("Exiting")
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if self.ip_input_box.active:
                if event.key == pygame.K_RETURN:
                    self.connect_to_game(self.ip_input_box.text)

    def connect_to_game(self, ip):
        pass


if __name__ == '__main__':
    GameLobby(run_lobby=True)
