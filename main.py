import pygame  # pip install pygame-ce
from gamestates.game import Game
from gamestates.menu import Menu

pygame.init()
WIDTH, HEIGHT = 640, 360  # Use 320x180 or multiples

class App:
    def __init__(self):
        self.change_scale(2)  # 3 is 1080x1920

        self.fps = 60
        self.clock = pygame.time.Clock()

        # Game States
        self.game_state = 0  # Starting game state
        self.menu = Menu(self)  # 0
        self.game = Game(self)  # 1

    def change_scale(self, SCALE):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SCALED | pygame.HIDDEN)
        self.window = pygame.Window.from_display_module()
        self.window.size = (WIDTH * SCALE, HEIGHT * SCALE)
        self.window.position = pygame.WINDOWPOS_CENTERED
        self.window.show()

    def run(self):
        while True:
            if self.game_state == 0:
                self.menu.update()
            if self.game_state == 1:
                self.game.update()
            self.clock.tick(self.fps)

app = App()
app.run()