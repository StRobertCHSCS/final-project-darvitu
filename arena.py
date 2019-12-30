"""
-------------------------------------------------------------------------------
Name: arena.py
Purpose: Contains all code regarding the rendering of arena backgrounds for our game

Author:	Wang.D

Created: 29/12/2019
-------------------------------------------------------------------------------
"""

import arcade


class Arena:
    def __init__(self, width, height):
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

    def draw_arena(self, arena: int) -> None:
        """Draws the corresponding arena given the arena number

        Arguments:
            arena {int} -- the arena number to draw
        """
        arcade.draw_texture_rectangle(self.SCREEN_WIDTH / 2,
                                      self.SCREEN_HEIGHT / 2, self.SCREEN_WIDTH, self.SCREEN_HEIGHT,
                                      arcade.load_texture("arena" + str(arena) + ".jpg"))
