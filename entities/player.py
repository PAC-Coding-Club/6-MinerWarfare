import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, app, group, player_id):
        super().__init__()  # Adds all attributes and methods from parent object

        self.gravity = 1
        self.player_id = player_id
        self.app = app

        ### USE FOR IMAGE
        # # Load the player image
        # self.image = pygame.image.load("entities/assets/Player.png")
        # # Get the rectangle for positioning
        # self.rect = self.image.get_rect()

        ### USE FOR COLOR
        # Create a plain surface with a single color (e.g., red)
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 0, 0))
        # Get the rectangle for positioning
        self.rect = self.image.get_rect()
        self.rect.topleft = (100, 100)  # Starting position (x=100, y=100)

        # Add the sprite to the group
        group.add(self)

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
        # TODO: Add better player movement and gravity
        keys = pygame.key.get_pressed()
        if keys[self.controls["left"]]:
            self.rect.x -= 3
        if keys[self.controls["right"]]:
            self.rect.x += 3
        if keys[self.controls["up"]]:
            self.rect.y -= 3
        if keys[self.controls["down"]]:
            self.rect.y += 3
        self.rect.y += self.gravity

        blocks = []
        for block in self.app.game.level.blocks.sprites():
            distance = ((self.rect.centerx - block.rect.centerx) ** 2 +
                        (self.rect.centery - block.rect.centery) ** 2) ** 0.5

            # Check if the distance is less than 40
            if distance < 40:
                blocks.append(block)

        for block in blocks:
            if self.rect.colliderect(block.rect):
                block_center = pygame.Vector2(block.rect.center)
                top_dist = pygame.Vector2(self.rect.centerx, self.rect.top).distance_to(block_center)
                bottom_dist = pygame.Vector2(self.rect.centerx, self.rect.bottom).distance_to(block_center)
                left_dist = pygame.Vector2(self.rect.left, self.rect.centery).distance_to(block_center)
                right_dist = pygame.Vector2(self.rect.right, self.rect.centery).distance_to(block_center)

                closest = min(top_dist, bottom_dist, left_dist, right_dist)
                print(top_dist, bottom_dist, left_dist, right_dist)
                if closest == top_dist:
                    if self.rect.top < block.rect.bottom:
                        self.rect.top = block.rect.bottom
                elif closest == bottom_dist:
                    if self.rect.bottom > block.rect.top:
                        self.rect.bottom = block.rect.top
                elif closest == left_dist:
                    if self.rect.left < block.rect.right:
                        self.rect.left = block.rect.right
                elif closest == right_dist:
                    if self.rect.right > block.rect.left:
                        self.rect.right = block.rect.left
                else:
                    pass
