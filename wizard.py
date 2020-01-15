from typing import Tuple

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
        self.can_shoot = True

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
        if self.fireball.reset and player.health > 0:
            self.reset_fireball()
        elif player.health <= 0:
            self.reset_fireball()
            self.fireball.textures.append(arcade.load_texture("images/fireball_end.png"))

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
        self.can_shoot = False

    def reset_fireball(self) -> None:
        """
        resets fireball after hitting a wall
        :return: none
        """
        self.fireball.is_wall_hit = False
        self.fireball.center_x = self.center_x
        self.fireball.center_y = self.center_y
        self.fireball.change_y = 0
        self.fireball.change_x = 0
        self.can_shoot = True
        self.fireball.reset = False


class Fireball(arcade.AnimatedTimeSprite):
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
        self.is_wall_hit = False
        self.reset = False
        self.take_damage = False
        self.load_textures()
        self.is_player_hit = False

    def load_textures(self) -> None:
        """
        loads textures
        :return: none
        """
        self.textures.append(arcade.load_texture("images/fireball.png", scale=0.3))
        self.textures.append(arcade.load_texture("images/fireball_2.png", scale=0.3))

    def shoot_fireball(self, player: Player) -> None:
        """
        Draws a fireball
        :param player: player to shoot at
        :return: none
        """
        # condition if the fireball has hit the wall to send a new one
        self.is_wall_hit = False
        self.take_damage = False
        # determine end points of fireball
        end_x, end_y = player.center_x, player.center_y
        if player.direction == "UP":
            end_y = player.center_y + 50
        if player.direction == "DOWN":
            end_y = player.center_y - 50
        if player.direction == "LEFT":
            end_x = player.center_x - 50
        if player.direction == "RIGHT":
            end_x = player.center_x + 50
        # finding the side lengths of the triangles
        delta_x = abs(self.center_x - end_x)
        delta_y = abs(self.center_y - end_y)
        # finding the related acute angle
        if delta_x == 0 or delta_y == 0:
            # find where the player is in relation to the fireball
            if delta_x == 0:
                if self.center_y < player.center_y:
                    self.angle = 90
                else:
                    self.angle = 270
            if delta_y == 0:
                if self.center_x < player.center_x:
                    self.angle = 0
                else:
                    self.angle = 180
        else:
            self.theta = math.atan(delta_y / delta_x) * 180 / math.pi
            if self.center_x < player.center_x:
                if self.center_y <= player.center_y:
                    self.angle = self.theta
                else:
                    self.angle = 360 - self.theta
            elif self.center_x > player.center_x:
                if self.center_y <= player.center_y:
                    self.angle = 180 - self.theta
                else:
                    self.angle = 180 + self.theta

        # distance from fireball to player /5 is the movement speed
        speed = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2)) / 5
        # move fireball
        self.change_x = (end_x - self.center_x) / speed
        self.change_y = (end_y - self.center_y) / speed

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
            x1, y1 = arcade.rotate_point(self.center_x - self.width / 4,
                                         self.center_y - self.width / 4,
                                         self.center_x,
                                         self.center_y,
                                         self.angle)
            x2, y2 = arcade.rotate_point(self.center_x + self.width / 4,
                                         self.center_y - self.height / 4,
                                         self.center_x,
                                         self.center_y,
                                         self.angle)
            x3, y3 = arcade.rotate_point(self.center_x + self.width / 4,
                                         self.center_y + self.height / 4,
                                         self.center_x,
                                         self.center_y,
                                         self.angle)
            x4, y4 = arcade.rotate_point(self.center_x - self.width / 4,
                                         self.center_y + self.height / 4,
                                         self.center_x,
                                         self.center_y,
                                         self.angle)

            self._point_list_cache = ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
        return self._point_list_cache

    points = property(get_points, arcade.Sprite.set_points)

    def update_animation(self, player: Player):
        """
        Logic for selecting the proper texture to use.
        """

        if self.frame % self.texture_change_frames == 0:
            if self.is_wall_hit:
                self.reset = True
                if self.is_player_hit and not self.take_damage:
                    player.health -= 10
                    self.take_damage = True
                    self.is_player_hit = False
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
            self.set_texture(self.cur_texture_index)
        self.frame += 1
