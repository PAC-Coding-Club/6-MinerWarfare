import pygame as pg
from entities.player import Player
from level.level import Level


class Game:
    def __init__(self, app):
        self.clock = pg.time.Clock()
        self.app = app

        self.players = pg.sprite.Group()

        # TODO: Create players depending on inputs
        for i in range(1):
            Player(app, self.players, i)
        self.level = Level(self)

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.app.game_state = 0

        # Update
        for player in self.players:
            player.update()

        # Render
        self.level.draw(self.app.screen)
        for player in self.players:
            player.draw(self.app.screen)

        pg.display.update()
        self.app.screen.fill((60, 60, 60))
        pg.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))
