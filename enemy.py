import arcade
from player import Player


class Enemy(arcade.AnimatedTimeSprite):
    def __init__(self, window_width: int, window_heigth: int, player_speed=150, direction="DOWN"):
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
        self.center_y = window_heigth // 2

        # defining size of player for later use
        self.width = None
        self.height = None
        self.movement = True

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

    def follow(self, player: Player) -> None:
        """
        Makes enemy follow the player
        Method that is called in the main.py file on_update()
        :param player: the player to follow
        :return: none
        """
        if self.center_x < player.center_x:
            self.center_x += 10
        if self.center_x > player.center_x:
            self.center_x -= 10
        if self.center_y < player.center_y:
            self.center_y += 10
        if self.center_y > player.center_y:
            self.center_y -= 10
