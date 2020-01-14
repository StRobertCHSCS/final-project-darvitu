import arcade
import math
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

        # set direction facing for statue
        self.direction = None
        # load fireball
        self.fireball = self.create_fireball()

    def point_towards(self, player: Player) -> None:
        """
        Points wizard towards the player
        :return: none
        """
        if self.center_x < player.center_x:
            self.texture = arcade.load_texture("images/wizard_tower.png", scale=1.5)
            self.direction = "RIGHT"
        else:
            self.texture = arcade.load_texture("images/wizard_tower.png", mirrored=True, scale=1.5)
            self.direction = "LEFT"

    def create_fireball(self) -> arcade.Sprite:
        """
        Creates a fireball
        :return: a fireball
        """
        return Fireball(self.center_x, self.center_y)

    def shoot(self, player: Player) -> None:
        """
        Shoots fireball, calls fireball.shoot_fireball()
        :param player: player to shoot at
        :return: none
        """
        self.fireball.shoot_fireball(player)


class Fireball(arcade.Sprite):
    def __init__(self, center_x, center_y):
        """
        Creates a fireball
        :param center_x: center x of the fireball start point
        :param center_y: center y of the fireball start point
        """
        # call parent
        super().__init__(center_x=center_x, center_y=center_y)
        self.center_x = center_x
        self.center_y = center_y
        self.texture = arcade.load_texture("images/fireball.png")

    def shoot_fireball(self, player: Player) -> None:
        """
        Draws a fireball
        :param player: player to shoot at
        :return: none
        """
        # condition if the fireball has hit the wall to send a new one
        self.has_reached_wall = False

        # finding the side lengths of the triangles
        delta_x = abs(self.center_x - player.center_x)
        delta_y = abs(self.center_y - player.center_y)
        # finding the related acute angle
        theta = math.tan(delta_y / delta_x)
        # find where the player is in relation to the fireball
        if self.center_x + 10 < player.center_x:
            if self.center_y <= player.center_y:
                self.angle = theta
            else:
                self.angle = 360 - theta
        elif self.center_x - 10 > player.center_x:
            if self.center_y <= player.center_y:
                self.angle = 180 - theta
            else:
                self.angle = 180 + theta
        # determine end points of fireball
        end_x, end_y = player.center_x, player.center_y
        if player.direction == "UP":
            end_y = player.center_y + 25
        if player.direction == "DOWN":
            end_y = player.center_y - 25
        if player.direction == "LEFT":
            end_x = player.center_x - 25
        if player.direction == "RIGHT":
            end_x = player.center_x + 25


        # move fireball
        self.change_x = (end_x - self.center_x) / 10
        self.change_y = (end_y - self.change_y) / 10
        print(self.change_x, self.change_y)