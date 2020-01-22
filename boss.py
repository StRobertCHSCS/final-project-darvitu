import arcade
from typing import Tuple
from player import Player


class Boss(arcade.AnimatedTimeSprite):
    def __init__(self, x, y):
        """
        Creates the boss
        :param x: x center
        :param y: y center
        """
        super().__init__()
        self.center_x = x
        self.center_y = y
        # create textures
        self.textures_left = []
        self.textures_right = []
        self.textures_dead = []
        # player health - if it reaches 0 then it does
        self.health = 100
        self.create_textures()
        self.textures = self.textures_left

    # load textures
    def create_textures(self) -> None:
        """
        loads textures
        :return: none
        """
        # add textures to respective locations
        self.textures_left.append(arcade.load_texture("images/boss_sprite.png", mirrored=True, scale=0.5))
        self.textures_left.append(arcade.load_texture("images/boss_sprite_2.png", mirrored=True, scale=0.5))
        self.textures_right.append(arcade.load_texture("images/boss_sprite.png", scale=0.5))
        self.textures_right.append(arcade.load_texture("images/boss_sprite_2.png", scale=0.5))
        self.textures_dead.append(arcade.load_texture("images/blob_dead.png", scale=5))
        self.textures_dead.append(arcade.load_texture("images/blob_dead.png", scale=5))

        # slow animation rate
        self.texture_change_frames = 45

    # animation for facing
    def point_towards(self, player: Player) -> None:
        """
        Sets animation to the direction of the player movement
        :param player:  player
        :return: None
        """
        if self.health < 1:
            self.textures = self.textures_dead
        elif player.center_x < self.center_x:
            self.textures = self.textures_right
        else:
            self.textures = self.textures_left

    # def get_points(self) -> Tuple[Tuple[float, float]]:
    #     """
    #     Get the corner points for the rect that makes up the sprite.
    #     """
    #     if self._point_list_cache is not None:
    #         return self._point_list_cache
    #
    #     if self._points is not None:
    #         point_list = []
    #         for point in range(len(self._points)):
    #             point = (self._points[point][0] + self.center_x,
    #                      self._points[point][1] + self.center_y)
    #             point_list.append(point)
    #         self._point_list_cache = tuple(point_list)
    #     else:
    #         x1, y1 = arcade.rotate_point(self.center_x - self.player_width / 2,
    #                                      self.center_y - self.player_height / 2,
    #                                      self.center_x,
    #                                      self.center_y,
    #                                      self.angle)
    #         x2, y2 = arcade.rotate_point(self.center_x + self.player_width / 2,
    #                                      self.center_y - self.player_height / 2,
    #                                      self.center_x,
    #                                      self.center_y,
    #                                      self.angle)
    #         x3, y3 = arcade.rotate_point(self.center_x + self.player_width / 2,
    #                                      self.center_y + self.player_height / 2,
    #                                      self.center_x,
    #                                      self.center_y,
    #                                      self.angle)
    #         x4, y4 = arcade.rotate_point(self.center_x - self.player_width / 2,
    #                                      self.center_y + self.player_height / 2,
    #                                      self.center_x,
    #                                      self.center_y,
    #                                      self.angle)
    #
    #         self._point_list_cache = ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
    #     return self._point_list_cache

    # points = property(get_points, arcade.Sprite.set_points)

    def update_animation(self, player):
        """
        Logic for selecting the proper texture to use.
        """
        if self.frame % self.texture_change_frames == 0:
            self.cur_texture_index += 1
            if self.health < 100:
                self.health += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
            self.set_texture(self.cur_texture_index)
        self.frame += 1