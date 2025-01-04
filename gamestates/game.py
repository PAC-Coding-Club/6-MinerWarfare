import pygame
from level.level import Level


class Game:
    def __init__(self, app):
        self.clock = pygame.time.Clock()
        self.app = app

        self.level = Level(self)

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.game_state = 0

        # Update
        self.app.players.update()

        # Render
        self.level.draw(self.app.screen)
        for player in self.app.players:
            player.draw(self.app.screen)

        pygame.display.set_caption("FPS: " + str(int(self.app.clock.get_fps())))
