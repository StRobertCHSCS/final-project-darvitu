from random import random
from typing import Tuple

import arcade
from arcade import rotate_point

from player import Player


class BossBullet(arcade.AnimatedTimeSprite):
    def __init__(self, x, y):
        """Constructor of the bullet class, that is the entity that the boss will be shooting.

                                  :param direction: default direction of player
                                  :param player_speed: speed of player
                                  :param window_width: width of game window
                                  :param window_heigth: height of game window
                                  """
        super().__init__()

        super().__init__()

        # setting position of bullet
        self.center_x = x
        self.center_y = y

        # create textures for animations
        self.create_textures()
        # if  hits player
        self.is_player_hit = False

    # create textures
    def create_textures(self) -> None:
        """
        Creates textures for enemy. By default, all entities except player will face right.
        :return: none
        """
        # add textures to respective locations
        self.textures.append(arcade.load_texture("images/boss_bullet.png", scale=1))
        self.textures.append(arcade.load_texture("images/boss_sprite.png", scale=1))


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
            x1, y1 = rotate_point(self.center_x - 40,
                                  self.center_y - 40,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x2, y2 = rotate_point(self.center_x + 40,
                                  self.center_y - 40,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x3, y3 = rotate_point(self.center_x + 40,
                                  self.center_y + 40,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x4, y4 = rotate_point(self.center_x - 40,
                                  self.center_y + 40,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)

            self._point_list_cache = ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
        return self._point_list_cache

    points = property(get_points, arcade.Sprite.set_points)


