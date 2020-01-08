import arcade


class Player(arcade.AnimatedTimeSprite):
    def __init__(self, window_width: int, window_height: int, player_speed=250, direction="DOWN"):
        super().__init__()

        """Constructor of the Player class, that is the entity that the user will be moving controlling.

        :param direction: default direction of player
        :param player_speed: speed of player
        :param window_width: width of game window
        :param window_heigth: height of game window
        """
        # setting speed and direction based on creation of Player object
        self.player_speed = player_speed
        self.direction = direction

        # change animation rate
        self.texture_change_frames = 30

        # spawn facing forward
        self.face_direction(direction)

        # setting position of Player
        self.center_x = window_width // 2
        self.center_y = window_height // 2

        # setting up window size
        self.WINDOW_HEIGHT = window_height
        self.WINDOW_WIDTH = window_width

    # animation for the player to face when it is not moving
    def face_direction(self, direction) -> None:
        """
        Faces the character animation based on the direction.
        :param direction: direction for the character to face
        :return: None
        """
        if direction == "LEFT":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=104, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=312, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(1):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=208, width=96, height=104,
                                        scale=0.5))
        elif direction == "DOWN":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=0, width=96, height=104, scale=0.5))

        else:
            print("Invalid direction to face")

    # animation for moving
    def move_direction(self, direction) -> None:
        """
        Sets animation to the direction of the player movement
        :param direction: direction of player movement
        :return: None
        """
        if direction == "DOWN":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=416, width=96, height=104,
                                        scale=0.5))
        elif direction == "LEFT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=520, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=624, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/test_sprite_sheet.png", x=i * 96, y=728, width=96, height=104,
                                        scale=0.5))
        else:
            print("Direction not valid to move")

    def move_player(self, delta_time, direction):
        self.direction = direction
        if self.direction is not None:
            self.texture_change_frames = 2.5
            if self.direction == "RIGHT":
                self.change_x = 5
            if self.direction == "LEFT":
                self.change_x = -5
            if self.direction == "UP":
                self.change_y = 5
            if self.direction == "DOWN":
                self.change_y = -5
        else:
            self.texture_change_frames = 30
