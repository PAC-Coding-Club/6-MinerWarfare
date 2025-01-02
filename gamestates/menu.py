import pygame as pg
import os
import json


class InputBox:
    def __init__(self, center_x, center_y, width, height, active_colour, inactive_colour, text_colour, font='freesansbold.ttf', font_size=22, text=''):
        self.active_colour = active_colour
        self.inactive_colour = inactive_colour
        self.text_colour = text_colour
        self.font = pg.font.Font(font, font_size)

        x = center_x - width / 2
        y = center_y - height / 2
        self.rect = pg.Rect(x, y, width, height)
        self.color = self.inactive_colour
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.active_colour if self.active else self.inactive_colour
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.text_colour)
            self.color = self.active_colour if self.active else self.inactive_colour
            self.update()

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.width, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, center_x, center_y, width, height, border, curve, buttonColour, textColour, hoverColour, id, text, font='freesansbold.ttf', font_size=80, text_offset=0):
        self.font_size = font_size
        self.font = pg.font.Font(font, font_size)
        self.text_offset = text_offset

        x = center_x - width / 2
        y = center_y - height / 2
        self.x = x
        self.y = y
        self.border = border
        self.curve = curve
        self.buttonColour = buttonColour
        self.textColour = textColour
        self.hover_colour = hoverColour
        self.id = id
        self.text = text
        self.rect = pg.Rect(self.x, self.y, width, height)

        self.highlighted = False

    def handle_event(self, event):
        if not hasattr(event, "pos"):
            return

        if self.rect.collidepoint(event.pos):
            self.highlighted = True
            if event.type == pg.MOUSEBUTTONDOWN:
                return True
        elif not self.rect.collidepoint(event.pos):
            self.highlighted = False

    def draw(self, screen):
        if self.highlighted:
            pg.draw.rect(screen, self.hover_colour, self.rect, self.border, self.curve)
        else:
            pg.draw.rect(screen, self.buttonColour, self.rect, self.border, self.curve)

        if self.text != "":
            text_surf = self.font.render(self.text, True, self.textColour)
            text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + self.text_offset))
            screen.blit(text_surf, text_rect)


class Menu:
    def __init__(self, app):
        self.app = app

        self.buttons = []
        self.load_buttons()

    def load_buttons(self, menu="menu_main"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Build the path to the JSON file
        json_path = os.path.join(script_dir, "..", "data", "buttons", "menu.json")

        # Open and load the JSON file
        try:
            with open(json_path, "r") as file:
                file_info = json.load(file)  # Use json.load instead of json_load
                print(f"loaded {json_path}")
        except FileNotFoundError:
            print(f"File not found: {json_path}")
            return
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_path}")
            return

        # Check if the menu exists in the loaded data
        if menu not in file_info:
            print(f"Invalid menu: {menu}")
            return

        # Set button info
        button_info = file_info[menu]

        self.buttons = []
        for button in button_info:
            if button["type"] == "click":
                self.buttons.append(
                    Button(button["x"], button["y"], button["width"], button["height"], button["border"], button["curve"], button["buttonColour"], button["textColour"], button["hoverColour"], button["id"], button["text"], button["font"], button["font_size"], button["text_offset"])
                )
            elif button["type"] == "input_box":
                self.buttons.append(
                    InputBox(button["x"], button["y"], button["width"], button["height"], button["active_colour"], button["inactive_colour"], button["textColour"], button["font"], button["font_size"])
                )

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            for button in self.buttons:
                if button.handle_event(event) and isinstance(button, Button):

                    if button.id.startswith("menu_"):  # Check if the button is an input box
                        self.load_buttons(button.id)

                    if button.id.startswith("gamestate_"):
                        value = button.id.split("_")[1]
                        self.app.game_state = int(value)

                    if button.id.startswith("option_resolution_"):
                        value = button.id.split("_")[2]
                        self.app.change_scale(int(value))

                    if button.id.startswith("button_quit"):
                        pg.quit()
                        quit()

                elif isinstance(button, InputBox) and event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    return "input_box_" + str(button.text)

        for button in self.buttons:
            button.draw(self.app.screen)

        pg.display.update()
        self.app.screen.fill((60, 60, 60))