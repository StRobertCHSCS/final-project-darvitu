import arcade

from blob import Blob
from goblin import Goblin
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
