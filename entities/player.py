import pygame
import math


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

        self.tools = [
            Tool("Pickaxe"),
            Tool("Knife"),
        ]
        self.selected_tool = 0
        self.angle = 0

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.angle is not None:
            start_pos = self.rect.center

            # Draw direction arrow
            end_pos = (
                start_pos[0] + 50 * math.cos(self.angle),
                start_pos[1] - 50 * math.sin(self.angle)
            )
            pygame.draw.line(surface, (0, 255, 0), start_pos, end_pos, 2)

    def update(self):
        controls = self.input_handler.get_input()
        if not hasattr(self, 'previous_controls'):
            self.previous_controls = controls

        # TODO: Add better player movement and gravity
        # Movement controls
        if controls["left"]:
            self.rect.x -= 3
        if controls["right"]:
            self.rect.x += 3
        if controls["up"]:
            self.rect.y -= 3
        if controls["down"]:
            self.rect.y += 3
        # Apply gravity
        self.rect.y += 1

        # Select tool based on controls
        if controls["select_tool_1"]:
            self.selected_tool = 0
            print("Selected tool", self.tools[self.selected_tool].type)
        if controls["select_tool_2"]:
            self.selected_tool = 1
            print("Selected tool", self.tools[self.selected_tool].type)

        # Handle switch_tool_right logic
        if controls["switch_tool_right"] and not self.previous_controls["switch_tool_right"]:
            self.selected_tool += 1
            if self.selected_tool >= len(self.tools):
                self.selected_tool = 0
            print("Selected tool", self.tools[self.selected_tool].type)

        # Handle switch_tool_left logic
        if controls["switch_tool_left"] and not self.previous_controls["switch_tool_left"]:
            self.selected_tool -= 1
            if self.selected_tool < 0:
                self.selected_tool = len(self.tools) - 1
            print("Selected tool", self.tools[self.selected_tool].type)

        if controls["use"] and not self.previous_controls["use"]:
            if self.selected_tool == 1:
                pass
            if self.selected_tool == 2:
                pass
            print(f"Used {self.tools[self.selected_tool].type}")

        # Set angle
        if controls["angle"] is not None:
            self.angle = controls["angle"]

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

        self.previous_controls = controls