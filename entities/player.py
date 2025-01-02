import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, group, player_id):
        super().__init__()  # Adds all attributes and methods from parent object

        ### USE FOR IMAGE
        # # Load the player image
        # self.image = pygame.image.load("entities/assets/Player.png")
        # # Get the rectangle for positioning
        # self.rect = self.image.get_rect()

        ### USE FOR COLOR
        # Create a plain surface with a single color (e.g., red)
        self.image = pygame.Surface((50, 50))  # 50x50 size
        self.image.fill((255, 0, 0))  # Fill with red color (RGB)
        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)  # Starting position (x=100, y=100)

        # Add the sprite to the group
        group.add(self)

        self.player_id = player_id

        # TODO: load controls from json depending on player_id
        self.controls = {
            "up": pygame.K_w,
            "left": pygame.K_a,
            "down": pygame.K_s,
            "right": pygame.K_d,
        }

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.controls["left"]]:
            self.rect.x -= 5
        if keys[self.controls["right"]]:
            self.rect.x += 5
        if keys[self.controls["up"]]:
            self.rect.y -= 5
        if keys[self.controls["down"]]:
            self.rect.y += 5

