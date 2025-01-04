import pygame

from entities.player import Player


class InputHandler:
    def __init__(self, control_type, joystick=None):
        self.control_type = control_type  # "keyboard" or "joystick"
        self.joystick = joystick  # Reference to the assigned joystick object

        # Define default control mappings for keyboard
        self.key_binds = {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "select_tool_1": pygame.K_1,
            "select_tool_2": pygame.K_2,
        }

        # Define joystick button/axes mappings (example)
        self.axis_threshold = 0.2  # Deadzone for joystick
        self.joystick_binds = {
            "up_axis": 1,  # Y-axis negative movement
            "right_axis": 0,  # X-axis positive movement
            "button_tool_1": 0,  # Button 0 selects tool 1
            "button_tool_2": 1,  # Button 1 selects tool 2
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
        }

        if self.control_type == "keyboard":
            keys = pygame.key.get_pressed()  # Get active keyboard state
            controls["up"] = keys[self.key_binds["up"]]
            controls["down"] = keys[self.key_binds["down"]]
            controls["left"] = keys[self.key_binds["left"]]
            controls["right"] = keys[self.key_binds["right"]]
            controls["select_tool_1"] = keys[self.key_binds["select_tool_1"]]
            controls["select_tool_2"] = keys[self.key_binds["select_tool_2"]]

        elif self.control_type == "joystick" and self.joystick:
            # Get joystick axis values and apply a deadzone
            if self.joystick.get_axis(self.joystick_binds["up_axis"]) < -self.axis_threshold:
                controls["up"] = True
            if self.joystick.get_axis(self.joystick_binds["up_axis"]) > self.axis_threshold:
                controls["down"] = True
            if self.joystick.get_axis(self.joystick_binds["right_axis"]) < -self.axis_threshold:
                controls["left"] = True
            if self.joystick.get_axis(self.joystick_binds["right_axis"]) > self.axis_threshold:
                controls["right"] = True

            # Check joystick button presses
            controls["select_tool_1"] = self.joystick.get_button(self.joystick_binds["button_tool_1"])
            controls["select_tool_2"] = self.joystick.get_button(self.joystick_binds["button_tool_2"])

        return controls


class ControlMenu:
    def __init__(self, app):
        self.app = app

        self.num_players = 2
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        self.input_handlers = []
        self.input_handlers.append(InputHandler("keyboard"))

        for joystick in self.joysticks:
            print(f"Joystick {joystick.get_instance_id()}: {joystick.get_name()}")
            self.input_handlers.append(InputHandler("joystick", joystick))

    def update(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.app.change_state([0])
                    self.app.menu.load_buttons("menu_player_select")

            for input_handler in self.input_handlers:
                user_input = input_handler.get_input()
                for value in user_input.values():
                    if value:
                        make_player = True
                        for player in self.app.players:
                            if player.input_handler == input_handler:
                                make_player = False
                        if make_player:
                            Player(self.app, self.app.players, input_handler)

        font = pygame.font.Font(None, 36)
        text = font.render(str(self.app.players.__len__()), True, (255, 255, 255))
        self.app.screen.blit(text, (10, 10))
