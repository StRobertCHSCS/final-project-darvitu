import arcade, math
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
        # create textures
        self.textures_left = []
        self.textures_right = []
        self.textures_attack_left = []
        self.textures_attack_right = []
        self.create_textures()
        # if it is hitting an enemy
        self.is_attack_state = False

        # spawn facing forward
        self.move_direction(direction)

        # setting position of Player
        self.center_x = window_width
        self.center_y = window_height

        # setting up window size
        self.WINDOW_HEIGHT = window_height
        self.WINDOW_WIDTH = window_width

        # size of player
        self.player_width = player_width
        self.player_height = player_height

        # player health - if it reaches 0 then game over
        self.health = 100

    # load textures
    def create_textures(self) -> None:
        """
        loads textures
        :return: none
        """
        # add textures to respective locations
        self.textures_left.append(arcade.load_texture("images/player_phase_1.png", mirrored=True, scale=1))
        self.textures_left.append(arcade.load_texture("images/player_phase_2.png", mirrored=True, scale=1))
        self.textures_right.append(arcade.load_texture("images/player_phase_1.png", scale=1))
        self.textures_right.append(arcade.load_texture("images/player_phase_2.png", scale=1))
        self.textures_attack_right.append(arcade.load_texture("images/player_phase_1.png"))
        self.textures_attack_right.append(arcade.load_texture("images/player_attack_1.png", scale=1))
        self.textures_attack_right.append(arcade.load_texture("images/player_attack_2.png", scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/player_phase_1.png", mirrored=True, scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/player_attack_1.png", mirrored=True, scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/player_attack_2.png", mirrored=True, scale=1))

    # animation and destruction of enemies
    def attack(self, towers) -> None:
        """
        Sets animations and destroys affected enemies
        :return: none
        """
        if self.textures == self.textures_left or self.textures == self.textures_attack_left:
            self.textures = self.textures_attack_left
        else:
            self.textures = self.textures_attack_right
        self.is_attack_state = True
        self.texture_change_frames = 10

        for tower in towers:
            if math.sqrt(math.pow(self.center_x - tower.fireball.center_x, 2) + math.pow(
                    self.center_y - tower.fireball.center_y,
                    2)) < 100:
                tower.fireball.is_wall_hit = True

    # animation for moving
    def move_direction(self, direction) -> None:
        """
        Sets animation to the direction of the player movement
        :param direction: direction of player movement
        :return: None
        """
        if direction == "DOWN" or direction == "RIGHT" or direction == "UP":
            if not self.is_attack_state:
                self.textures = self.textures_right
        elif direction == "LEFT":
            if not self.is_attack_state:
                self.textures = self.textures_left

    def move_player(self, direction):
        self.direction = direction
        if self.direction is not None and self.health > 0:
            if self.direction == "RIGHT":
                self.change_x = 5
            if self.direction == "LEFT":
                self.change_x = -5
            if self.direction == "UP":
                self.change_y = 5
            if self.direction == "DOWN":
                self.change_y = -5

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

    def game_over(self) -> None:
        """
        Displays game over state of player
        :return: none
        """
        self.direction = None
        self.change_x = 0
        self.change_y = 0
        self.texture = arcade.load_texture("images/game_over.png", scale=0.1, mirrored=True)

    def update_animation(self):
        """
        Logic for selecting the proper texture to use.
        """
        if self.is_attack_state:
            self.frame = 0
            if self.textures == self.textures_attack_left or self.textures == self.textures_left:
                self.textures = self.textures_attack_left
            else:
                self.textures = self.textures_attack_right
        if self.frame % self.texture_change_frames == 0:
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
                self.texture_change_frames = 15
                self.is_attack_state = False
            self.set_texture(self.cur_texture_index)
        self.frame += 1
