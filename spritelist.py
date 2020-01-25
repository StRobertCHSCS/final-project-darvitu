"""
-------------------------------------------------------------------------------
Name: spritelist.py
Purpose: Code for custom build arcade spritelist.

Author:	Wang.D

Created: 01/01/2020
-------------------------------------------------------------------------------
"""
import arcade

from slime import Slime
from executioner import Executioner
from player import Player


class Sprites(arcade.SpriteList):
    def __init__(self):
        """
        Updated SpriteList class
        """
        super().__init__()

    def update_animation(self, player: Player):
        for sprite in self.sprite_list:
            sprite.update_animation(player)
