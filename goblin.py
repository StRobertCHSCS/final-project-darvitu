import arcade, math, random
from player import Player
from arcade.draw_commands import rotate_point
from typing import Tuple


class Goblin(arcade.AnimatedTimeSprite):
    def __init__(self, window_width: int, window_heigth: int, player_speed=250, direction="DOWN", enemy_width=32,
                 enemy_height=48):
        """Constructor of the Player class, that is the entity that the user will be moving controlling.

                          :param direction: default direction of player
                          :param player_speed: speed of player
                          :param window_width: width of game window
                          :param window_heigth: height of game window
                          """
        super().__init__()
        # setting speed and direction based on creation of Player object
        self.player_speed = player_speed
        self.direction = direction
        self.previous_direction = None

        # change animation rate
        self.texture_change_frames = 30

        # setting position of Player
        self.center_x = window_width // 2
        self.center_y = window_heigth // 2

        # defining size of player for later use
        self.enemy_width = enemy_width
        self.enemy_height = enemy_height
        self.movement = True
        self.count = 0
        self.hit = False
        self.time = None

        # create textures for animations
        self.textures_left = []
        self.textures_right = []
        self.textures_attack_left = []
        self.textures_attack_right = []
        self.create_textures()
        # spawn facing forward
        self.face_direction(direction)

    # create textures
    def create_textures(self) -> None:
        """
        Creates textures for enemy. By default, all entities except player will face right.
        :return: none
        """
        # add textures to respective locations
        self.textures_left.append(arcade.load_texture("images/goblin_phase_1.png", mirrored=True, scale=1))
        self.textures_left.append(arcade.load_texture("images/goblin_phase_2.png", mirrored=True, scale=1))
        self.textures_right.append(arcade.load_texture("images/goblin_phase_1.png", scale=1))
        self.textures_right.append(arcade.load_texture("images/goblin_phase_2.png", scale=1))
        self.textures_attack_right.append(arcade.load_texture("images/goblin_attack_1.png", scale=1))
        self.textures_attack_right.append(arcade.load_texture("images/goblin_attack_2.png", scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/goblin_attack_1.png", mirrored=True, scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/goblin_attack_2.png", mirrored=True, scale=1))

    # animation for the player to face when it is not moving
    def face_direction(self, direction) -> None:
        """
        Faces the character animation based on the direction.
        :param direction: direction for the character to face
        :return: None
        """
        if direction == "LEFT":
            self.textures = self.textures_left
        elif direction == "RIGHT":
            self.textures = self.textures_right
        elif direction == "UP" or direction == "DOWN":
            self.textures = self.textures_right
        else:
            print("Invalid direction to face")

    def attack(self) -> None:
        """
        Loads the current animation to the attack frames
        :return:none
        """
        if self.direction == "RIGHT"


    # animation for moving
    def move_direction(self, direction) -> None:
        """
        Sets animation to the direction of the player movement
        :param direction: direction of player movement
        :return: None
        """
        if direction == "LEFT":
            self.textures = self.textures_left
        elif direction == "RIGHT":
            self.textures = self.textures_right
        elif direction == "UP" or direction == "DOWN":
            self.textures = self.textures_right
        else:
            print("Direction not valid to move")

    def follow(self, player: Player, delta_time=1 / 60) -> None:
        """
        Makes enemy follow the player, engine that will run all moving sprites
        Method that is called in the main.py file on_update()
        :param delta_time: time of rate of execution
        :param player: the player to follow
        :return: none
        """
        self.texture_change_frames = 15
        wait = random.randint(10, 30)
        if self.movement:
            self.count += 1
            if abs(self.center_x - player.center_x) > 5:
                if self.center_x < player.center_x:
                    self.direction = "RIGHT"
                if self.center_x > player.center_x:
                    self.direction = "LEFT"
            else:
                self.count = wait
        else:
            self.count += 1
            if abs(self.center_y - player.center_y) > 5:
                if self.center_y < player.center_y:
                    self.direction = "UP"
                if self.center_y > player.center_y:
                    self.direction = "DOWN"
            else:
                self.count = wait

        # changing the direction (up/down to left/right) every 25 loops
        if self.count == wait:
            self.movement = not self.movement
            self.count = 0
        # if enemy hits a wall
        if self.hit:
            if self.previous_direction is not None and self.previous_direction is not self.direction:
                self.hit = False
            self.previous_direction = self.direction
            self.direction = None

        if self.direction is not None:
            if self.direction == "RIGHT":
                self.change_x = 4.5
            if self.direction == "LEFT":
                self.change_x = -4.5
            if self.direction == "UP":
                self.change_y = 4.5
            if self.direction == "DOWN":
                self.change_y = -4.5

            # update direction of sprite
            self.move_direction(self.direction)
        else:
            # update to standing animation
            self.texture_change_frames = 30

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
            x1, y1 = rotate_point(self.center_x - self.enemy_width / 4,
                                  self.center_y - self.enemy_height / 4,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x2, y2 = rotate_point(self.center_x + self.enemy_width / 4,
                                  self.center_y - self.enemy_height / 4,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x3, y3 = rotate_point(self.center_x + self.enemy_width / 4,
                                  self.center_y + self.enemy_height / 4,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x4, y4 = rotate_point(self.center_x - self.enemy_width / 4,
                                  self.center_y + self.enemy_height / 4,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)

            self._point_list_cache = ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
        return self._point_list_cache

    points = property(get_points, arcade.Sprite.set_points)
