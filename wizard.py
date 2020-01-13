import arcade
from player import Player


class WizardTower(arcade.Sprite):
    def __init__(self, center_x, center_y, width, height):
        """
        Wizard tower that shoots towards player
        :param center_x: center x of the wizard
        :param center_y: center y of the wizard
        :param width: width of the wizard
        :param height: height of the wizard
        """
        super().__init__(center_x=center_x, center_y=center_y)
        # initiate width and height variables
        self.width = width
        self.height = height
        # load fireball
        self.fireball = Fireball()

    def point_towards(self, player: Player) -> None:
        """
        Points wizard towards the player
        :return: none
        """
        if self.center_x < player.center_x:
            self.texture = arcade.load_texture("images/wizard_tower.png", mirrored=True)
        else:
            self.texture = arcade.load_texture("images/wizard_tower.png")


class Fireball(arcade.Sprite):
    def __init__(self, center_x, center_y):
        """
        Creates a fireball
        :param center_x: center x of the fireball start point
        :param center_y: center y of the fireball start point
        """
        self.center_x = center_x
        self.center_y = center_y
        self.texture = arcade.load_texture("images/fireball.png")

    def shoot_fireball(self, player: Player) -> None:
        """
        Draws a fireball
        :param player: player to shoot at
        :return:
        """
        delta_x = abs(self.center_x - player.center_x)
