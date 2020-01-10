import arcade
from arcade.draw_commands import rotate_point
from typing import Tuple


class Player(arcade.AnimatedTimeSprite):
    def __init__(self, window_width: int, window_height: int, player_speed=250, direction="DOWN", player_width=32,
                 player_height=48):
        """Constructor of the Player class, that is the entity that the user will be moving controlling.

                :param direction: default direction of player
                :param player_speed: speed of player
                :param window_width: width of game window
                :param window_heigth: height of game window
                :param player_width: width of the player
                :param player_height: height of the player
                """
        super().__init__()

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

        # size of player
        self.player_width = player_width
        self.player_height = player_height

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
                    arcade.load_texture("images/player.png", x=i * 96, y=104, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=312, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(1):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=208, width=96, height=104,
                                        scale=0.5))
        elif direction == "DOWN":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=0, width=96, height=104, scale=0.5))

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
                    arcade.load_texture("images/player.png", x=i * 96, y=416, width=96, height=104,
                                        scale=0.5))
        elif direction == "LEFT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=520, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=624, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=728, width=96, height=104,
                                        scale=0.5))
        else:
            print("Direction not valid to move")

    def move_player(self, direction):
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

    def get_points(self) -> Tuple[Tuple[float, float]]:
        """
        Get the corner points for the rect that makes up the sprite.
        """
        if self._point_list_cache is not None:
            return self._point_list_cache

        if self._points is not None:
            point_list = []
            for point in range(len(self._points)):
                point = (self._points[point][0] + self.center_x,
                         self._points[point][1] + self.center_y)
                point_list.append(point)
            self._point_list_cache = tuple(point_list)
        else:
            x1, y1 = rotate_point(self.center_x - self.player_width / 2,
                                  self.center_y - self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x2, y2 = rotate_point(self.center_x + self.player_width / 2,
                                  self.center_y - self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x3, y3 = rotate_point(self.center_x + self.player_width / 2,
                                  self.center_y + self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x4, y4 = rotate_point(self.center_x - self.player_width / 2,
                                  self.center_y + self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)

            self._point_list_cache = ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
        return self._point_list_cache

    points = property(get_points, arcade.Sprite.set_points)
