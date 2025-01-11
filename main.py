import pygame  # pip install pygame-ce

from gamestates.control_menu import ControlMenu
from gamestates.game import Game
from gamestates.menu import Menu

pygame.init()
pygame.joystick.init()
WIDTH, HEIGHT = 640, 360  # Use 320x180 or multiples


class App:
    def __init__(self):
        self.change_scale(2)  # 3 is 1080x1920

        # Stuff needed in multiple game states
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.players = pygame.sprite.Group()

        # Game States
        self.menu = None
        self.game = None
        self.control_menu = None

        self.game_states = [0]  # Starting game state
        self.change_state(self.game_states)

    def change_scale(self, SCALE):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED | pygame.HIDDEN)
        self.window = pygame.Window.from_display_module()
        self.window.size = (WIDTH * SCALE, HEIGHT * SCALE)
        self.window.position = pygame.WINDOWPOS_CENTERED
        self.window.show()

    def run(self):
        while True:
            events = pygame.event.get()
            if 0 in self.game_states:
                self.menu.update(events)
            if 1 in self.game_states:
                self.game.update(events)
            if 2 in self.game_states:
                self.control_menu.update(events)
            pygame.display.update()
            self.screen.fill((60, 60, 60))
            self.clock.tick(self.fps)

    def change_state(self, new_state):
        print(new_state)

        if 0 in new_state:
            if self.menu is None:
                self.menu = Menu(self)
        if 1 in new_state:
            if self.game is None:
                self.game = Game(self)
        if 2 in new_state:
            # Control menu is not saved.
            # Allows new controllers to be found by leaving and re-entering the menu
            self.control_menu = ControlMenu(self)
        self.game_states = new_state


app = App()
app.run()