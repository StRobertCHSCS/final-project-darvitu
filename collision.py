import arcade
from player import Player
from tiledmap import TiledMap
from arcade.geometry import check_for_collision_with_list
from blob import Blob


class CollisionDetection(arcade.PhysicsEngineSimple):
    def __init__(self, player: Player, walls) -> None:
        """
        Class in charge of monitoring collisions between player, walls, enemies, and other sprites
        :param player: user
        :param walls: list of walls
        """
        super().__init__(player, walls)
        # initiate class variables
        self.player = player
        self.walls = walls

    def update(self, direction, player_to_follow=None) -> arcade.key:
        """
        Move everything and resolve collisions
        :return: none
        """
        # if the player is the user
        if isinstance(self.player, Player):
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
                else:
                    print("Error, collision while player wasn't moving.")

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
                else:
                    print("Error, collision while player wasn't moving.")
            self.player.change_x, self.player.change_y = 0, 0
        # if it isn't the player
        elif isinstance(self.player, Blob):
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
        elif isinstance(self.player, arcade.SpriteList):
            # checks for player and other entity collisions
            pass
