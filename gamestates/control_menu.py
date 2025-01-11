import math
import pygame
from entities.player import Player


class InputHandler:
    def __init__(self, control_type, joystick=None):
        self.control_type = control_type  # "keyboard" or "joystick"
        self.joystick = joystick  # Reference to the assigned joystick object
        self.player = None

        # Define default control mappings for keyboard
        self.key_binds = {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "select_tool_1": pygame.K_1,
            "select_tool_2": pygame.K_2,
            "switch_tool_right": None,
            "switch_tool_left": None,
            "use": pygame.MOUSEBUTTONDOWN,
        }

        # Define joystick button/axes mappings (example)
        self.axis_threshold = 0.2  # Deadzone for joystick
        self.joystick_binds = {
            "left_y_axis": 1,  # Y-axis negative movement
            "left_x_axis": 0,  # X-axis positive movement
            "right_y_axis": 3,  #
            "right_x_axis": 2,  #
            "left_trigger_axis": 4,
            "right_trigger_axis": 5,
            "button_tool_1": None,  # Button 0 selects tool 1
            "button_tool_2": None,  # Button 1 selects tool 2
            "right_bumper": 5,
            "left_bumper": 4,

        }

    def get_input(self):
        """
        Returns a dictionary of movement and action controls.
        This abstracts whether the input is via keyboard or joystick.
        """
        controls = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "select_tool_1": False,
            "select_tool_2": False,
            "switch_tool_right": False,
            "switch_tool_left": False,
            "use": False,
            "angle": None,
        }

        if self.control_type == "keyboard":
            keys = pygame.key.get_pressed()  # Get active keyboard state
            controls["up"] = keys[self.key_binds["up"]]
            controls["down"] = keys[self.key_binds["down"]]
            controls["left"] = keys[self.key_binds["left"]]
            controls["right"] = keys[self.key_binds["right"]]
            controls["select_tool_1"] = keys[self.key_binds["select_tool_1"]]
            controls["select_tool_2"] = keys[self.key_binds["select_tool_2"]]
            controls["use"] = pygame.mouse.get_pressed()[0]

            if self.player:
                coords = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(self.player.rect.center)
                angle = math.atan2(-coords.y, coords.x)
                if math.degrees(angle) < 0:
                    angle += 2 * math.pi
                controls["angle"] = angle

        elif self.control_type == "joystick" and self.joystick:
            # Get joystick axis values and apply a deadzone
            if self.joystick.get_axis(self.joystick_binds["left_y_axis"]) < -self.axis_threshold:
                controls["up"] = True
            if self.joystick.get_axis(self.joystick_binds["left_y_axis"]) > self.axis_threshold:
                controls["down"] = True
            if self.joystick.get_axis(self.joystick_binds["left_x_axis"]) < -self.axis_threshold:
                controls["left"] = True
            if self.joystick.get_axis(self.joystick_binds["left_x_axis"]) > self.axis_threshold:
                controls["right"] = True

            # Check joystick button presses
            if self.joystick_binds["button_tool_1"]:
                controls["select_tool_1"] = self.joystick.get_button(self.joystick_binds["button_tool_1"])
            if self.joystick_binds["button_tool_2"]:
                controls["select_tool_2"] = self.joystick.get_button(self.joystick_binds["button_tool_2"])

            if self.joystick_binds["right_bumper"]:
                controls["switch_tool_right"] = self.joystick.get_button(self.joystick_binds["right_bumper"])
            if self.joystick_binds["left_bumper"]:
                controls["switch_tool_left"] = self.joystick.get_button(self.joystick_binds["left_bumper"])

            if self.joystick_binds["right_trigger_axis"]:
                value = self.joystick.get_axis(self.joystick_binds["right_trigger_axis"])
                if value > -self.axis_threshold and value != 0:
                    controls["use"] = True

            if self.player:
                x = self.joystick.get_axis(self.joystick_binds["right_x_axis"])
                y = self.joystick.get_axis(self.joystick_binds["right_y_axis"])

                # No input = None, with a dead zone
                if abs(x) < self.axis_threshold and abs(y) < self.axis_threshold:
                    controls["angle"] = None
                else:
                    angle = math.atan2(-y, x)
                    if math.degrees(angle) < 0:
                        angle += 2 * math.pi
                    controls["angle"] = angle

        return controls


class ControlMenu:
    def __init__(self, app):
        self.app = app

        self.joysticks = None
        self.input_handlers = []
        self.input_handlers.append(InputHandler("keyboard"))
        self.refresh_inputs()

        for sprite in self.app.players.sprites():
            sprite.kill()
        self.app.players.empty()

    def refresh_inputs(self):
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

        for joystick in self.joysticks:
            print(f"Joystick {joystick.get_instance_id()}: {joystick.get_name()}")

            activated = False
            for handler in self.input_handlers:
                if handler.joystick:
                    if joystick.get_instance_id() == handler.joystick.get_instance_id():
                        activated = True
            if not activated:
                self.input_handlers.append(InputHandler("joystick", joystick))

    def update(self, events):
        self.refresh_inputs()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.change_state([0, 2])
                    self.app.menu.load_buttons("menu_controls")

            for input_handler in self.input_handlers:
                user_input = input_handler.get_input()
                if input_handler.control_type == "keyboard":
                    user_input["use"] = False  # Use gets triggered by mouse click on the menu
                for value in user_input.values():
                    if value:
                        make_player = True
                        for player in self.app.players:
                            if player.input_handler == input_handler:
                                make_player = False
                        if make_player:
                            player = Player(self.app, self.app.players, input_handler)
                            input_handler.player = player

        font_1 = pygame.font.Font(None, 36)
        font_2 = pygame.font.Font(None, 16)

        text = font_1.render(str(self.app.players.__len__()), True, (255, 255, 255))
        self.app.screen.blit(text, (10, 10))

        for i in range(4):
            x = 50
            player_text = font_1.render(f"Player {i+1}", True, (255, 255, 255))
            self.app.screen.blit(player_text, (x + 140 * i, 160))
            if i < len(self.app.players):
                if self.app.players.sprites()[i].input_handler.control_type == "joystick":
                    connected_text = font_2.render(f"Connected: \n{self.app.players.sprites()[i].input_handler.joystick.get_name()}", True, (255, 255, 255))
                else:
                    connected_text = font_2.render(f"Connected: \nKeyboard", True, (255, 255, 255))
            else:
                connected_text = font_2.render(f"Press a Button", True, (255, 255, 255))

            self.app.screen.blit(connected_text, (x + 140 * i, 190))
