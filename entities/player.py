import pygame


class Tool():
    def __init__(self, tool_type=None):
        self.type = tool_type


class Player(pygame.sprite.Sprite):
    def __init__(self, app, group, input_handler):
        super().__init__()  # Adds all attributes and methods from parent object

        self.input_handler = input_handler
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

        self.tools = {
            1: Tool("pickaxe"),
            2: Tool("Knife"),
        }
        self.selected_tool = 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def select_tool(self, tool_id):
        self.selected_tool = tool_id

    def update(self):
        # TODO: Add better player movement and gravity
        controls = self.input_handler.get_input()

        # Movement controls
        if controls["left"]:
            self.rect.x -= 3
        if controls["right"]:
            self.rect.x += 3
        if controls["up"]:
            self.rect.y -= 3
        if controls["down"]:
            self.rect.y += 3

        # Select tool based on controls
        if controls["select_tool_1"]:
            self.selected_tool = 1
        if controls["select_tool_2"]:
            self.selected_tool = 2

        # Apply gravity
        self.rect.y += 1

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
