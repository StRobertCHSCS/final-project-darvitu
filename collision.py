"""
-------------------------------------------------------------------------------
Name: collisino.py
Purpose: Collision engine for all sprites.

Author:	Wang.D

Created: 23/01/2020
-------------------------------------------------------------------------------
"""
import arcade
import time

from boss import Boss
from boss_bullet import BossBullet
from executioner import Executioner
from minion import Minion
from player import Player
from tiledmap import TiledMap
from arcade.geometry import check_for_collision_with_list
from slime import Slime
from mage import Fireball, Mage


class CollisionDetection(arcade.PhysicsEngineSimple):
    def __init__(self, player, walls = None, traps=None) -> None:
        """
        Class in charge of monitoring collisions between player, walls, enemies, and other sprites
        :param player: user
        :param walls: list of walls
        """
        super().__init__(player, walls)
        # initiate class variables
        self.player = player
        self.walls = walls
        self.traps = traps

    def update(self, direction=None, player_to_follow=None) -> None:
        """
        Move everything and resolve collisions
        :return: none
        """
        # player and other enemy detection
        if isinstance(player_to_follow, arcade.SpriteList):
            # checks for player and other entity collisions
            hit_list = \
                check_for_collision_with_list(self.player,
                                              player_to_follow)
            if len(hit_list) > 0:
                for item in hit_list:
                    if self.player.is_attack_state:
                        if not isinstance(item, Fireball):
                            item.health -= 1.5
                    if isinstance(item, Executioner):
                        item.is_player_hit = True
                    if isinstance(item, Slime):
                        item.is_player_hit = True
                    if isinstance(item, Fireball):
                        item.is_wall_hit = True
                        item.is_player_hit = True
                    if isinstance(item, Boss):
                        if self.player.is_attack_state:
                            item.health -= 0.5
        # if the player is the user
        elif isinstance(self.player, Player):
            if self.player.health < 1:
                self.player.game_over()
            # --- Move sprite
            self.player.move_player(direction)
            # update x position
            self.player.center_x += self.player.change_x
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_x > 0:
                    for item in hit_list:
                        self.player.right = min(item.left,
                                                self.player.right) - 5
                        self.player.direction = None
                        return arcade.key.RIGHT
                elif self.player.change_x < 0:
                    for item in hit_list:
                        self.player.left = max(item.right,
                                               self.player.left) + 5
                        self.player.direction = None
                        return arcade.key.LEFT
            # update y position
            self.player.center_y += self.player.change_y
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_y > 0:
                    for item in hit_list:
                        self.player.top = min(item.bottom,
                                              self.player.top) - 5
                        self.player.direction = None
                        return arcade.key.UP
                elif self.player.change_y < 0:
                    for item in hit_list:
                        self.player.bottom = max(item.top,
                                                 self.player.bottom) + 5
                        self.player.direction = None
                        return arcade.key.DOWN
            # check for trap hit
            hit_list = \
                check_for_collision_with_list(self.player, self.traps)
            if len(hit_list) > 0:
                self.player.health -= 0.1
            self.player.change_x, self.player.change_y = 0, 0

        # if it isn't the player
        elif isinstance(self.player, Slime):
            # --- Move sprite
            self.player.follow(player_to_follow)
            # update x position
            self.player.center_x += self.player.change_x
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_x > 0:
                    for item in hit_list:
                        self.player.right = min(item.left,
                                                self.player.right) - 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True
                elif self.player.change_x < 0:
                    for item in hit_list:
                        self.player.left = max(item.right,
                                               self.player.left) + 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True

            # update y position
            self.player.center_y += self.player.change_y
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)
            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_y > 0:
                    for item in hit_list:
                        self.player.top = min(item.bottom,
                                              self.player.top) - 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True
                elif self.player.change_y < 0:
                    for item in hit_list:
                        self.player.bottom = max(item.top,
                                                 self.player.bottom) + 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True
                else:
                    print("Error, collision while enemy wasn't moving.")
            self.player.change_x, self.player.change_y = 0, 0
        elif isinstance(self.player, Minion):
            # --- Move sprite
            self.player.follow(player_to_follow)
            if arcade.check_for_collision(self.player, player_to_follow):
                self.player.is_player_hit = True
            # update x position
            self.player.center_x += self.player.change_x
            self.player.center_y += self.player.change_y

            # Check for wall hit
            if self.player.center_x > 890:
                self.player.center_x = 890
            if self.player.center_x < 20:
                self.player.center_x = 20
            if self.player.center_y > 890:
                self.player.center_y = 890
            if self.player.center_y < 20:
                self.player.center_y = 20
            self.player.change_x, self.player.change_y = 0, 0

        elif isinstance(self.player, Executioner):
            # --- Move sprite
            self.player.follow(player_to_follow)
            # update x position
            self.player.center_x += self.player.change_x
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_x > 0:
                    for item in hit_list:
                        self.player.right = min(item.left,
                                                self.player.right) - 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True
                elif self.player.change_x < 0:
                    for item in hit_list:
                        self.player.left = max(item.right,
                                               self.player.left) + 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True
                else:
                    print("Error, collision while enemy wasn't moving.")

            # update y position
            self.player.center_y += self.player.change_y
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)
            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_y > 0:
                    for item in hit_list:
                        self.player.top = min(item.bottom,
                                              self.player.top) - 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True
                elif self.player.change_y < 0:
                    for item in hit_list:
                        self.player.bottom = max(item.top,
                                                 self.player.bottom) + 5
                        self.player.direction = None
                        self.player.movement = not self.player.movement
                        self.player.hit = True
                else:
                    print("Error, collision while enemy wasn't moving.")

            self.player.change_x, self.player.change_y = 0, 0
        elif isinstance(self.player, Fireball):
            # --- Move sprite
            # update x position
            self.player.center_x += self.player.change_x
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)

            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_x > 0:
                    for item in hit_list:
                        self.player.right = min(item.left,
                                                self.player.right) - 5
                elif self.player.change_x < 0:
                    for item in hit_list:
                        self.player.left = max(item.right,
                                               self.player.left) + 5
                else:
                    print("Error, collision while enemy wasn't moving.")
                self.player.is_wall_hit = True
                self.player.reset = True
            # update y position
            self.player.center_y += self.player.change_y
            # Check for wall hit
            hit_list = \
                check_for_collision_with_list(self.player,
                                              self.walls)
            # If we hit a wall, move so the edges are at the same point
            if len(hit_list) > 0:
                if self.player.change_y > 0:
                    for item in hit_list:
                        self.player.top = min(item.bottom,
                                              self.player.top) - 5
                elif self.player.change_y < 0:
                    for item in hit_list:
                        self.player.bottom = max(item.top,
                                                 self.player.bottom) + 5
                else:
                    print("Error, collision while enemy wasn't moving.")
                self.player.is_wall_hit = True
                self.player.reset = True
        # elif isinstance(self.player, BossBullet):
        #     hit_list = \
        #         check_for_collision_with_list(self.player, self.walls)
        #     if len(hit_list) > 0:
        #         self.player.stop = True
        #     if arcade.geometry.check_for_collision(self.player, direction):
        #         self.player.stop = True
        #         direction.health -= 1
