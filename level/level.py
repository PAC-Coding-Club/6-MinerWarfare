import pygame
import random


class Block(pygame.sprite.Sprite):
    def __init__(self, group, x, y, size=24, color=(100, 100, 100), block_type=1):
        super().__init__()  # Adds all attributes and methods from parent object
        group.add(self)

        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.block_type = block_type

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Level:
    def __init__(self, game, level_data=None):
        self.game = game
        if not level_data:
            def weighted_random():
                return random.choices([0, 1, 2], weights=[10, 1, 0.1], k=1)[0]
            width, height = 80, 45
            level_data = [[weighted_random() for _ in range(width)] for _ in range(height)]

        self.grid = []
        self.block_size = 8
        self.blocks = pygame.sprite.Group()

        # Load blocks based on the level data
        for row_index, row in enumerate(level_data):
            block_row = []
            for col_index, cell in enumerate(row):
                if cell == 1:  # Create a block for non-empty cells
                    x = col_index * self.block_size
                    y = row_index * self.block_size
                    block = Block(self.blocks, x, y, self.block_size, color=(120, 120, 255))  # Solid blocks are blue
                    block_row.append(block)
                elif cell == 2:  # Another type of block
                    x = col_index * self.block_size
                    y = row_index * self.block_size
                    block = Block(self.blocks, x, y, self.block_size, color=(255, 200, 100))  # Type 2 blocks are orange
                    block_row.append(block)
                else:
                    block_row.append(None)  # Empty space
            self.grid.append(block_row)

    def draw(self, screen):
        """Draw the entire grid of blocks on the screen."""
        for row in self.grid:
            for block in row:
                if block:  # Only draw blocks that exist
                    block.draw(screen)

    def load_new_level(self, level_data):
        """Load a new level grid and reset the current grid."""
        self.__init__(level_data)




