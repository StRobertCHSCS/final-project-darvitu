"""
-------------------------------------------------------------------------------
Name: master.py
Purpose: Combination of all code to form working game using all the .py files in this repository.

Author:	Wang.D

Created: 23/01/2020
-------------------------------------------------------------------------------
"""

import pytiled_parser
from arcade.tilemap import get_tilemap_layer, _process_tile_layer, _process_object_layer, _create_sprite_from_tile, \
    _get_tile_by_gid

import arcade, math, random
from player import Player
from arcade.draw_commands import rotate_point
from typing import Tuple


class Minion(arcade.AnimatedTimeSprite):
    def __init__(self, center_x: int, center_y: int, direction="DOWN", enemy_width=32,
                 enemy_height=48):
        """Constructor of the Player class, that is the entity that the user will be moving controlling.

                          :param direction: default direction of player
                          :param player_speed: speed of player
                          :param window_width: width of game window
                          :param window_heigth: height of game window
                          """
        super().__init__()
        # setting direction based on creation of Player object
        self.direction = direction
        self.previous_direction = None

        # change animation rate
        self.texture_change_frames = 30

        # setting position of Player
        self.center_x = center_x
        self.center_y = center_y

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
        self.textures_dead = []
        self.create_textures()
        # spawn facing forward
        self.face_direction(direction)
        self.is_player_hit_already = False
        self.is_player_hit = False
        self.stop = False
        self.health = 10

    # create textures
    def create_textures(self) -> None:
        """
        Creates textures for enemy. By default, all entities except player will face right.
        :return: none
        """
        # add textures to respective locations
        self.textures_right.append(arcade.load_texture("images/boss_sprite.png", mirrored=True, scale=0.1))
        self.textures_right.append(arcade.load_texture("images/boss_sprite_2.png", mirrored=True, scale=0.1))
        self.textures_left.append(arcade.load_texture("images/boss_sprite.png", scale=0.1))
        self.textures_left.append(arcade.load_texture("images/boss_sprite_2.png", scale=0.1))
        self.textures_dead.append(arcade.load_texture("images/boss_dead.png", scale=0.1))
        self.textures_dead.append(arcade.load_texture("images/boss_dead.png", scale=0.1))

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
        self.texture_change_frames = 30

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

        if player.health < 1:
            self.direction = None
            self.move_direction("RIGHT")
        if self.health < 1:
            self.direction = None
            self.textures = self.textures_dead

        if self.direction is not None:
            if self.direction == "RIGHT":
                self.change_x = 2
            if self.direction == "LEFT":
                self.change_x = -2
            if self.direction == "UP":
                self.change_y = 2
            if self.direction == "DOWN":
                self.change_y = -2

            # update direction of sprite
            if self.is_player_hit:
                self.is_player_hit_already = False

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
                                  self.center_y - self.enemy_height / 3,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x2, y2 = rotate_point(self.center_x + self.enemy_width / 4,
                                  self.center_y - self.enemy_height / 3,
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

    def update_animation(self, player: Player):
        """
        Logic for selecting the proper texture to use.
        """
        if self.frame % self.texture_change_frames == 0:
            if self.is_player_hit:
                if not self.is_player_hit_already:
                    player.health -= 0.5
                    self.is_player_hit_already = True
                    self.is_player_hit = False
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
            self.set_texture(self.cur_texture_index)
        self.frame += 1


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
        if speed is not 0:
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
                    player.health -= 5
                    self.take_damage = True
                    self.is_player_hit = False
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
            self.set_texture(self.cur_texture_index)
        self.frame += 1


class TiledMap(arcade.TiledMap):
    def __init__(self):
        super().__init__()

        self.ground_list = None
        self.wall_list = None
        self.traps_list = None

    def tutorial_world(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/tutorial-world.tmx")

        room.ground_list = self.process_layer(map, "ground", 1, "images")
        room.wall_list = self.process_layer(map, "walls", 1, "images")
        room.traps_list = self.process_layer(map, "traps", 1, "images")
        return room

    def stage_one(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stage1-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def stage_two(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stage2-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def stage_three(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stage3-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def boss_world(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stageBoss-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def process_layer(self, map_object: pytiled_parser.objects.TileMap,
                      layer_name: str,
                      scaling: float = 1,
                      base_directory: str = "") -> arcade.SpriteList:
        """
        This takes a map layer returned by the read_tmx function, and creates Sprites for it.

        :param map_object: The TileMap read in by read_tmx.
        :param layer_name: The name of the layer that we are creating sprites for.
        :param scaling: Scaling the layer up or down.
                        (Note, any number besides 1 can create a tearing effect,
                        if numbers don't evenly divide.)
        :param base_directory: Base directory of the file, that we start from to
                               load images.
        :returns: A SpriteList.

        """
        if len(base_directory) > 0 and not base_directory.endswith("/"):
            base_directory += "/"

        layer = get_tilemap_layer(map_object, layer_name)
        if layer is None:
            print(f"Warning, no layer named '{layer_name}'.")
            return arcade.SpriteList()

        if isinstance(layer, pytiled_parser.objects.TileLayer):
            return _process_tile_layer(map_object, layer, scaling, base_directory)

        elif isinstance(layer, pytiled_parser.objects.ObjectLayer):
            return _process_object_layer(map_object, layer, scaling, base_directory)

    def _process_tile_layer(map_object: pytiled_parser.objects.TileMap,
                            layer: pytiled_parser.objects.TileLayer,
                            scaling: float = 1,
                            base_directory: str = "") -> arcade.SpriteList:
        sprite_list = arcade.SpriteList()
        map_array = layer.data

        # Loop through the layer and add in the wall list
        for row_index, row in enumerate(map_array):
            for column_index, item in enumerate(row):
                # Check for empty square
                if item == 0:
                    continue

                tile = _get_tile_by_gid(map_object, item)
                if tile is None:
                    print(f"Warning, couldn't find tile for item {item} in layer "
                          f"'{layer.name}' in file '{map_object.tmx_file}'.")
                    continue

                my_sprite = _create_sprite_from_tile(map_object, tile, scaling=scaling,
                                                     base_directory=base_directory)

                my_sprite.right = column_index * (map_object.tile_size[0] * scaling)
                my_sprite.top = (map_object.map_size.height - row_index - 1) * (map_object.tile_size[1] * scaling)

                sprite_list.append(my_sprite)

        return sprite_list


class Sprites(arcade.SpriteList):
    def __init__(self):
        """
        Updated SpriteList class
        """
        super().__init__()

    def update_animation(self, player: Player):
        for sprite in self.sprite_list:
            sprite.update_animation(player)


class Sounds(arcade.PlaysoundException):
    def __init__(self):
        self.sounds = []
        self.add_sounds()

    def update(self, song: int) -> None:
        """
        Function to be called by on_update to play all sound needed
        :return: none
        """
        if 0 <= song < len(self.sounds):
            self.sounds[song].pause()
            self.sounds[song].play()

    def play_sound(self, sound) -> None:
        """
        Plays a sound with the specified name
        :param sound: sound name
        :return: none
        """

    def add_sounds(self) -> None:
        """
        loads all sounds from disk and adds them to self.sounds for later use
        :return: none
        """
        self.sounds.append(arcade.Sound("sounds/minecraft-theme.mp3"))
        self.sounds.append(arcade.Sound("sounds/starcraft-theme.mp3"))
        self.sounds.append(arcade.Sound("sounds/player_attack.mp3"))


class Player(arcade.AnimatedTimeSprite):
    def __init__(self, window_width: int, window_height: int, player_speed=250, direction="DOWN", player_width=32,
                 player_height=48):
        """Constructor of the Player class, that is the entity that the user will be moving controlling.

                :param direction: default direction of player
                :param player_speed: speed of player
                :param window_width: width of game window
                :param window_heigth: height of game window
                :param player_width: width of the player
                :param player_height: height of the player
                """
        super().__init__()

        # setting speed and direction based on creation of Player object
        self.player_speed = player_speed
        self.direction = direction
        self.last_direction = None

        # change animation rate
        self.texture_change_frames = 30
        # create textures
        self.textures_left = []
        self.textures_right = []
        self.textures_attack_left = []
        self.textures_attack_right = []
        self.create_textures()
        # if it is hitting an enemy
        self.is_attack_state = False

        # spawn facing forward
        self.move_direction(direction)

        # setting position of Player
        self.center_x = window_width
        self.center_y = window_height

        # setting up window size
        self.WINDOW_HEIGHT = window_height
        self.WINDOW_WIDTH = window_width

        # size of player
        self.player_width = player_width
        self.player_height = player_height

        # player health - if it reaches 0 then game over
        self.health = 100

    # load textures
    def create_textures(self) -> None:
        """
        loads textures
        :return: none
        """
        # add textures to respective locations
        self.textures_left.append(arcade.load_texture("images/player_phase_1.png", mirrored=True, scale=1))
        self.textures_left.append(arcade.load_texture("images/player_phase_2.png", mirrored=True, scale=1))
        self.textures_right.append(arcade.load_texture("images/player_phase_1.png", scale=1))
        self.textures_right.append(arcade.load_texture("images/player_phase_2.png", scale=1))
        self.textures_attack_right.append(arcade.load_texture("images/player_phase_1.png"))
        self.textures_attack_right.append(arcade.load_texture("images/player_attack_1.png", scale=1))
        self.textures_attack_right.append(arcade.load_texture("images/player_attack_2.png", scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/player_phase_1.png", mirrored=True, scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/player_attack_1.png", mirrored=True, scale=1))
        self.textures_attack_left.append(arcade.load_texture("images/player_attack_2.png", mirrored=True, scale=1))

    # animation and destruction of enemies
    def attack(self, towers) -> None:
        """
        Sets animations and destroys affected enemies
        :return: none
        """
        # Sounds().update(2)
        if self.textures == self.textures_left or self.textures == self.textures_attack_left:
            self.textures = self.textures_attack_left
        else:
            self.textures = self.textures_attack_right
        self.is_attack_state = True
        self.texture_change_frames = 10

        for tower in towers:
            if math.sqrt(math.pow(self.center_x - tower.fireball.center_x, 2) + math.pow(
                    self.center_y - tower.fireball.center_y,
                    2)) < 100:
                tower.fireball.is_wall_hit = True

    # animation for moving
    def move_direction(self, direction) -> None:
        """
        Sets animation to the direction of the player movement
        :param direction: direction of player movement
        :return: None
        """
        if direction == "DOWN" or direction == "RIGHT" or direction == "UP":
            if not self.is_attack_state:
                self.textures = self.textures_right
        elif direction == "LEFT":
            if not self.is_attack_state:
                self.textures = self.textures_left

    def move_player(self, direction):
        self.direction = direction
        if self.direction is not None and self.health > 0:
            if self.direction == "RIGHT":
                self.change_x = 5
            if self.direction == "LEFT":
                self.change_x = -5
            if self.direction == "UP":
                self.change_y = 5
            if self.direction == "DOWN":
                self.change_y = -5

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
            x1, y1 = rotate_point(self.center_x - self.player_width / 2,
                                  self.center_y - self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x2, y2 = rotate_point(self.center_x + self.player_width / 2,
                                  self.center_y - self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x3, y3 = rotate_point(self.center_x + self.player_width / 2,
                                  self.center_y + self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x4, y4 = rotate_point(self.center_x - self.player_width / 2,
                                  self.center_y + self.player_height / 2,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)

            self._point_list_cache = ((x1, y1), (x2, y2), (x3, y3), (x4, y4))
        return self._point_list_cache

    points = property(get_points, arcade.Sprite.set_points)

    def game_over(self) -> None:
        """
        Displays game over state of player
        :return: none
        """
        self.direction = None
        self.change_x = 0
        self.change_y = 0
        self.texture = arcade.load_texture("images/game_over.png", scale=0.1, mirrored=True)

    def update_animation(self):
        """
        Logic for selecting the proper texture to use.
        """
        if self.is_attack_state:
            self.frame = 0
            if self.textures == self.textures_attack_left or self.textures == self.textures_left:
                self.textures = self.textures_attack_left
            else:
                self.textures = self.textures_attack_right
        elif self.direction is not None:
            self.move_direction(self.direction)
        else:
            if self.last_direction is not None:
                self.move_direction(self.last_direction)
            else:
                self.textures = self.textures_right
        if self.frame % self.texture_change_frames == 0:
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
                self.texture_change_frames = 15
                self.is_attack_state = False
            self.set_texture(self.cur_texture_index)
        self.frame += 1


class Goblin(arcade.AnimatedTimeSprite):
    def __init__(self, center_x: int, center_y: int, health: int = 10, direction="DOWN",
                 enemy_width=32,
                 enemy_height=48):
        """Constructor of the Goblin class, that is one of the enemies.

                          :param direction: default direction of player
                          :param player_speed: speed of player
                          :param window_width: width of game window
                          :param window_heigth: height of game window
                          """
        super().__init__()
        # setting direction based on creation of Player object
        self.direction = direction
        self.previous_direction = None

        # change animation rate
        self.texture_change_frames = 30

        # setting position of Player
        self.center_x = center_x
        self.center_y = center_y

        # defining size of player for later use
        self.enemy_width = enemy_width
        self.enemy_height = enemy_height
        self.movement = True
        self.count = 0
        self.hit = False
        self.time = None
        self.is_player_hit_already = True

        # create textures for animations
        self.textures_left = []
        self.textures_right = []
        self.textures_attack_left = []
        self.textures_attack_right = []
        self.textures_dead = []
        self.create_textures()
        # spawn facing forward
        self.face_direction(direction)
        # goblin health
        self.health = health
        # if goblin hits player
        self.is_player_hit = False
        self.stop = False

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
        self.textures_dead.append(arcade.load_texture("images/blob_dead.png", scale=1.1))
        self.textures_dead.append(arcade.load_texture("images/blob_dead.png", scale=1.1))

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
        if self.direction == "RIGHT" or self.direction == "UP" or self.direction == "DOWN":
            self.textures = self.textures_attack_right
        else:
            self.textures = self.textures_attack_left

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

    def follow(self, player: Player) -> None:
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
        if player.health < 1:
            self.direction = None
            self.move_direction("RIGHT")
        if self.health < 1:
            self.direction = None
            self.textures = self.textures_dead
        if self.direction is not None:
            if self.direction == "RIGHT":
                self.change_x = 1.5
            if self.direction == "LEFT":
                self.change_x = -1.5
            if self.direction == "UP":
                self.change_y = 1.5
            if self.direction == "DOWN":
                self.change_y = -1.5

            # update direction of sprite
            if self.is_player_hit:
                self.attack()
                self.is_player_hit = False
                self.is_player_hit_already = False
            else:
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

    def update_animation(self, player: Player):
        """
        Logic for selecting the proper texture to use.
        """

        if self.frame % self.texture_change_frames == 0:
            if self.textures == self.textures_attack_left or self.textures == self.textures_attack_right:
                if not self.is_player_hit_already:
                    player.health -= 3
                    self.is_player_hit_already = True
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
            self.set_texture(self.cur_texture_index)
        self.frame += 1


class Blob(arcade.AnimatedTimeSprite):
    def __init__(self, center_x: int, center_y: int, direction="DOWN", enemy_width=32,
                 enemy_height=48):
        """Constructor of the Player class, that is the entity that the user will be moving controlling.

                          :param direction: default direction of player
                          :param player_speed: speed of player
                          :param window_width: width of game window
                          :param window_heigth: height of game window
                          """
        super().__init__()
        # setting direction based on creation of Player object
        self.direction = direction
        self.previous_direction = None

        # change animation rate
        self.texture_change_frames = 30

        # setting position of Player
        self.center_x = center_x
        self.center_y = center_y

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
        self.textures_dead = []
        self.create_textures()
        # spawn facing forward
        self.face_direction(direction)
        self.is_player_hit_already = False
        self.is_player_hit = False
        self.stop = False
        self.health = 3

    # create textures
    def create_textures(self) -> None:
        """
        Creates textures for enemy. By default, all entities except player will face right.
        :return: none
        """
        # add textures to respective locations
        self.textures_left.append(arcade.load_texture("images/blob_phase_1.png", mirrored=True, scale=1.1))
        self.textures_left.append(arcade.load_texture("images/blob_phase_2.png", mirrored=True, scale=1.1))
        self.textures_right.append(arcade.load_texture("images/blob_phase_1.png", scale=1.1))
        self.textures_right.append(arcade.load_texture("images/blob_phase_2.png", scale=1.1))
        self.textures_dead.append(arcade.load_texture("images/blob_dead.png", scale=1.1))
        self.textures_dead.append(arcade.load_texture("images/blob_dead.png", scale=1.1))

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

        if player.health < 1:
            self.direction = None
            self.move_direction("RIGHT")
        if self.health < 1:
            self.direction = None
            self.textures = self.textures_dead

        if self.direction is not None:
            if self.direction == "RIGHT":
                self.change_x = 4
            if self.direction == "LEFT":
                self.change_x = -4
            if self.direction == "UP":
                self.change_y = 4
            if self.direction == "DOWN":
                self.change_y = -4

            # update direction of sprite
            if self.is_player_hit:
                self.is_player_hit_already = False

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
                                  self.center_y - self.enemy_height / 3,
                                  self.center_x,
                                  self.center_y,
                                  self.angle)
            x2, y2 = rotate_point(self.center_x + self.enemy_width / 4,
                                  self.center_y - self.enemy_height / 3,
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

    def update_animation(self, player: Player):
        """
        Logic for selecting the proper texture to use.
        """
        if self.frame % self.texture_change_frames == 0:
            if self.is_player_hit:
                if not self.is_player_hit_already:
                    player.health -= 1
                    self.is_player_hit_already = True
                    self.is_player_hit = False
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.textures):
                self.cur_texture_index = 0
            self.set_texture(self.cur_texture_index)
        self.frame += 1


import math

import arcade
import time
import random

from boss import Boss
from player import Player
from tiledmap import TiledMap
from blob import Blob
from collision import CollisionDetection
from sounds import Sounds
from goblin import Goblin
from spritelist import Sprites
from wizard import WizardTower, Fireball
from minion import Minion


class Main():

    def __init__(self):

        self.direction = None
        self.player = None
        self.enemies = None
        self.player_engine = None
        self.enemies_engine = None
        self.towers_engine = None
        self.towers = None
        self.tile_map = None
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.time = 0
        self.world = 0
        self.sound = None
        self.obstacles = None
        self.enemy_count = 0
        self.start_attack_time = 0
        self.is_game_active = False
        self.rooms = []
        self.transition = None
        self.setup()
        self.level_finish_time = 0
        self.game_over = False

    def on_draw(self) -> None:
        """
        Holds all rendering code to screen
        :return: none, draws to the window
        """
        arcade.start_render()
        if self.transition is not None:
            arcade.draw_texture_rectangle(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2, 800, 800,
                                          self.transition)
            arcade.draw_text("<PRESS ENTER>", 300, 40, arcade.color.WHITE, 24)
        if self.is_game_active:
            self.rooms[self.world].ground_list.draw()
            self.rooms[self.world].wall_list.draw()
            self.rooms[self.world].traps_list.draw()

            self.enemies.draw()
            self.towers.draw()
            self.player.draw()

            # draw health bar
            self.draw_health_bar(self.player.health)
            # if self.world == 4:
            for item in self.enemies:
                if isinstance(item, Boss):
                    self.draw_health_bar_boss(item.health, item)

    def draw_health_bar_boss(self, health: int, boss: Boss) -> None:
        """
        Draws health bar to screen
        :param health: health of player
        :return: none
        """
        # draw background of health bar
        arcade.draw_texture_rectangle(boss.center_x, boss.center_y + 100, 52, 7,
                                      arcade.load_texture("images/health_bar_1.png"))
        arcade.draw_texture_rectangle(boss.center_x, boss.center_y + 100, 50, 5,
                                      arcade.load_texture("images/health_bar_2.png"))
        if health >= 80:
            arcade.draw_texture_rectangle(boss.center_x - 25 + (health / 4), boss.center_y + 100,
                                          health / 2,
                                          5,
                                          arcade.load_texture("images/health_bar_green.png"))
        elif health >= 40:
            arcade.draw_texture_rectangle(boss.center_x - 25 + (health / 4), boss.center_y + 100,
                                          health / 2,
                                          5,
                                          arcade.load_texture("images/health_bar_orange.png"))
        elif health > 0:
            arcade.draw_texture_rectangle(boss.center_x - 25 + (health / 4), boss.center_y + 100,
                                          health / 2,
                                          5,
                                          arcade.load_texture("images/health_bar_red.png"))

    def move_player(self) -> None:
        """
        Moves the player
        :return:
        """
        output = self.player_engine.update(self.direction)
        if output is not None:
            self.on_key_release(output, None)

    def move_enemy(self) -> None:
        """
        Moves enemies based on the position of the player
        :return: none
        """
        for item in self.enemies:
            if isinstance(item, Boss):
                item.point_towards(self.player)

        for enemy in self.enemies_engine:
            if math.sqrt(
                    math.pow(self.player.center_x - enemy.player.center_x, 2) + math.pow(
                        self.player.center_y - enemy.player.center_y,
                        2)) < 500:
                enemy.update(enemy, self.player)
        for tower in self.towers:
            if tower.can_shoot and self.time % 500 == 0:
                tower.shoot(self.player)
            tower.point_towards(self.player)
        for tower in self.towers_engine:
            tower.update()

    def on_update(self, delta_time) -> None:
        """
        Update function called periodically
        :param delta_time: time of execution
        :return: none
        """
        if self.is_game_active:
            # updates the animation state of the player sprite
            self.enemies.update_animation(self.player)

            self.player.update_animation()
            # move player
            self.move_player()
            # move enemies
            self.move_enemy()
            # check player and enemy collision
            self.player_engine.update(player_to_follow=self.enemies)
            # remove dead sprites
            self.enemy_count = 0
            for item in self.enemies:
                if not isinstance(item, Fireball):
                    if item.health < 1:
                        self.enemy_count += 1
            if self.enemy_count == len(self.enemies_engine):
                if self.level_finish_time == 0:
                    self.level_finish_time = self.time
                if self.time - self.level_finish_time >= 100:  # increase this value to increase transition delay
                    self.is_game_active = False
                    self.level_finish_time = 0
                    self.enemy_count = 0
                    self.world += 1
                    if self.world == 1:
                        self.stage_one()
                    elif self.world == 2:
                        self.stage_two()
                    elif self.world == 3:
                        self.stage_three()
                    elif self.world == 4:
                        self.stage_boss()
                    elif self.world == 5:
                        self.win_stage()
                        self.is_game_active = False
                        self.game_over = True
            if self.player.health < 1:
                self.lose_stage()
                self.is_game_active = False
                self.game_over = True
            # add minions
            # if self.time % 1000 == 0:
            #     if self.world == 4:
            #         for item in self.enemies:
            #             item.health = 10

            self.time += 1

    def draw_health_bar(self, health: int) -> None:
        """
        Draws health bar to screen
        :param health: health of player
        :return: none
        """
        # draw background of health bar
        arcade.draw_texture_rectangle(self.player.center_x, self.player.center_y + 30, 52, 7,
                                      arcade.load_texture("images/health_bar_1.png"))
        arcade.draw_texture_rectangle(self.player.center_x, self.player.center_y + 30, 50, 5,
                                      arcade.load_texture("images/health_bar_2.png"))
        if health >= 80:
            arcade.draw_texture_rectangle(self.player.center_x - 25 + (health / 4), self.player.center_y + 30,
                                          health / 2,
                                          5,
                                          arcade.load_texture("images/health_bar_green.png"))
        elif health >= 40:
            arcade.draw_texture_rectangle(self.player.center_x - 25 + (health / 4), self.player.center_y + 30,
                                          health / 2,
                                          5,
                                          arcade.load_texture("images/health_bar_orange.png"))
        elif health > 0:
            arcade.draw_texture_rectangle(self.player.center_x - 25 + (health / 4), self.player.center_y + 30,
                                          health / 2,
                                          5,
                                          arcade.load_texture("images/health_bar_red.png"))

    def on_key_press(self, symbol, modifiers) -> None:
        '''
        Moving the player based on the key pressed
        :param symbol: keypressed
        :param modifiers: Unused parameter
        :return: none
        '''

        # player movement
        if symbol == arcade.key.RIGHT:
            self.direction = "RIGHT"
            self.player.move_direction(self.direction)
        elif symbol == arcade.key.LEFT:
            self.direction = "LEFT"
            self.player.move_direction(self.direction)
        elif symbol == arcade.key.UP:
            self.direction = "UP"
            self.player.move_direction(self.direction)
        elif symbol == arcade.key.DOWN:
            self.direction = "DOWN"
            self.player.move_direction(self.direction)
        elif symbol == arcade.key.SPACE:
            if self.player.health > 0:
                if self.start_attack_time == 0 and not self.player.is_attack_state:
                    self.start_attack_time = self.time
                    self.player.attack(self.towers)
                    self.on_key_release(arcade.key.SPACE, None)
                elif self.time - self.start_attack_time > 6 and not self.player.is_attack_state:
                    self.start_attack_time = self.time
                    self.player.attack(self.towers)
                    self.on_key_release(arcade.key.SPACE, None)
        elif symbol == arcade.key.ENTER:
            if not self.game_over:
                self.is_game_active = True
            else:
                self.restart_game()
                self.game_over = False
                self.is_game_active = True
        elif symbol == arcade.key.DELETE:
            arcade.get_window().close()
        elif symbol == arcade.key.P:
            self.is_game_active = not self.is_game_active

    def on_key_release(self, symbol, modifiers) -> None:
        """
        Handling when user releases keys (stops moving)
        :param symbol: key released
        :param modifiers: unused
        :return: none
        """
        # sets key direction back to None after key release, starts standing animation
        if symbol == arcade.key.RIGHT and self.direction == "RIGHT":
            self.player.move_direction(self.direction)
            self.player.last_direction = self.direction
            self.direction = None
        elif symbol == arcade.key.LEFT and self.direction == "LEFT":
            self.player.move_direction(self.direction)
            self.player.last_direction = self.direction
            self.direction = None
        elif symbol == arcade.key.UP and self.direction == "UP":
            self.player.move_direction(self.direction)
            self.player.last_direction = self.direction
            self.direction = None
        elif symbol == arcade.key.DOWN and self.direction == "DOWN":
            self.player.move_direction(self.direction)
            self.player.last_direction = self.direction
            self.direction = None
        elif symbol == arcade.key.SPACE:
            if self.direction is None:
                self.player.move_direction(self.player.last_direction)
            else:
                self.player.move_direction(self.direction)

    def room_tutorial(self) -> None:
        """
        loads room tutorial
        :return: none
        """
        # setting up player
        self.player = Player(50, 50)
        # setting up enemies
        self.enemies_engine = []
        self.towers_engine = []
        self.enemies = Sprites()
        self.towers = Sprites()
        self.obstacles = arcade.SpriteList()
        self.enemies.append(Blob(750, 750))
        self.enemies.append(Blob(750, 50))
        self.enemies.append(Blob(50, 750))
        self.enemies.append(Goblin(750, 750, 3))
        self.enemies.append(Goblin(750, 50, 3))
        self.enemies.append(Goblin(50, 750, 3))
        self.enemies.append(Blob(400, 400))
        self.enemies.append(Goblin(400, 400, 3))
        for enemy in self.enemies:
            self.enemies_engine.append(
                CollisionDetection(enemy, self.obstacles))
        self.towers.append(WizardTower(400, 400, 48, 52))
        for tower in self.towers:
            self.towers_engine.append(
                CollisionDetection(tower.fireball, self.rooms[self.world].wall_list))
            self.enemies.append(tower.fireball)
        for item in self.rooms[self.world].wall_list:
            self.obstacles.append(item)
        for item in self.rooms[self.world].traps_list:
            self.obstacles.append(item)
        # create engines
        self.player_engine = CollisionDetection(self.player, self.rooms[self.world].wall_list,
                                                self.rooms[self.world].traps_list)

    def stage_one(self) -> None:
        """
        Sets up stage one
        :return: none
        """
        # transition
        self.transition = arcade.load_texture("images/level_1_screen.png")
        # setting up player
        self.player = Player(50, 50)
        # setting up enemies
        self.enemies_engine = []
        self.towers_engine = []
        self.enemies = Sprites()
        self.towers = Sprites()
        self.obstacles = arcade.SpriteList()
        self.enemies.append(Blob(750, 750))
        self.enemies.append(Blob(750, 50))
        self.enemies.append(Blob(50, 750))
        self.enemies.append(Goblin(750, 750, 3))
        self.enemies.append(Goblin(750, 50, 3))
        self.enemies.append(Goblin(50, 750, 3))
        self.enemies.append(Blob(400, 400))
        self.enemies.append(Goblin(400, 400, 3))

        for enemy in self.enemies:
            self.enemies_engine.append(
                CollisionDetection(enemy, self.obstacles))
        self.towers.append(WizardTower(400, 400, 48, 52))
        for tower in self.towers:
            self.towers_engine.append(
                CollisionDetection(tower.fireball, self.rooms[self.world].wall_list))
            self.enemies.append(tower.fireball)
        for item in self.rooms[self.world].wall_list:
            self.obstacles.append(item)
        for item in self.rooms[self.world].traps_list:
            self.obstacles.append(item)
        # create engines
        self.player_engine = CollisionDetection(self.player, self.rooms[self.world].wall_list,
                                                self.rooms[self.world].traps_list)

    def stage_two(self) -> None:
        """
        Sets up stage two
        :return: none
        """
        # transition
        self.transition = arcade.load_texture("images/level_2_screen.png")
        # setting up player
        self.player = Player(50, 50)
        # setting up enemies
        self.enemies_engine = []
        self.towers_engine = []
        self.enemies = Sprites()
        self.towers = Sprites()
        self.obstacles = arcade.SpriteList()
        self.enemies.append(Blob(400, 50))
        self.enemies.append(Goblin(400, 50, 3))
        self.enemies.append(Blob(400, 50))
        self.enemies.append(Goblin(400, 50, 3))

        for enemy in self.enemies:
            self.enemies_engine.append(
                CollisionDetection(enemy, self.obstacles))
        self.towers.append(WizardTower(400, 700, 48, 52))
        for tower in self.towers:
            self.towers_engine.append(
                CollisionDetection(tower.fireball, self.rooms[self.world].wall_list))
            self.enemies.append(tower.fireball)
        for item in self.rooms[self.world].wall_list:
            self.obstacles.append(item)
        for item in self.rooms[self.world].traps_list:
            self.obstacles.append(item)
        # create engines
        self.player_engine = CollisionDetection(self.player, self.rooms[self.world].wall_list,
                                                self.rooms[self.world].traps_list)

    def stage_three(self) -> None:
        """
        Sets up stage two
        :return: none
        """
        # transition
        self.transition = arcade.load_texture("images/level_3_screen.png")
        # setting up player
        self.player = Player(50, 50)
        # setting up enemies
        self.enemies_engine = []
        self.towers_engine = []
        self.enemies = Sprites()
        self.towers = Sprites()
        self.obstacles = arcade.SpriteList()
        self.enemies.append(Blob(400, 150))
        self.enemies.append(Goblin(400, 150, 3))
        self.enemies.append(Blob(400, 150))
        self.enemies.append(Goblin(400, 150, 3))

        for enemy in self.enemies:
            self.enemies_engine.append(
                CollisionDetection(enemy, self.obstacles))
        self.towers.append(WizardTower(400, 700, 48, 52))
        for tower in self.towers:
            self.towers_engine.append(
                CollisionDetection(tower.fireball, self.rooms[self.world].wall_list))
            self.enemies.append(tower.fireball)
        for item in self.rooms[self.world].wall_list:
            self.obstacles.append(item)
        for item in self.rooms[self.world].traps_list:
            self.obstacles.append(item)
        # create engines
        self.player_engine = CollisionDetection(self.player, self.rooms[self.world].wall_list,
                                                self.rooms[self.world].traps_list)

    def stage_boss(self) -> None:
        """
        Sets up stage two
        :return: none
        """
        # transition
        self.transition = arcade.load_texture("images/boss_screen.png")
        # setting up player
        self.player = Player(400, 50)
        # setting up enemies
        self.enemies_engine = []
        self.towers_engine = []
        self.enemies = Sprites()
        self.towers = Sprites()
        self.obstacles = arcade.SpriteList()
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Minion(400, 400))
        self.enemies.append(Boss(400, 400))
        for enemy in self.enemies:
            self.enemies_engine.append(
                CollisionDetection(enemy, self.obstacles))
        self.towers.append(WizardTower(50, 50, 48, 52))
        self.towers.append(WizardTower(750, 50, 48, 52))
        self.towers.append(WizardTower(50, 750, 48, 52))
        self.towers.append(WizardTower(750, 750, 48, 52))
        for tower in self.towers:
            self.towers_engine.append(
                CollisionDetection(tower.fireball, self.rooms[self.world].wall_list))
            self.enemies.append(tower.fireball)
        for item in self.rooms[self.world].wall_list:
            self.obstacles.append(item)
        for item in self.rooms[self.world].traps_list:
            self.obstacles.append(item)
        # create engines
        self.player_engine = CollisionDetection(self.player, self.rooms[self.world].wall_list,
                                                self.rooms[self.world].traps_list)

    def win_stage(self) -> None:
        """
        Loads end screen if you win
        :return: none
        """
        self.transition = arcade.load_texture("images/win_screen.png")

    def lose_stage(self) -> None:
        """
        Loads end screen if you win
        :return: none
        """
        self.transition = arcade.load_texture("images/lose_screen.png")

    def restart_game(self) -> None:
        """
        Resets the game
        :return:
        """
        self.world = 0
        self.room_tutorial()

    def setup(self):
        """
        Called once at the start
        :return: none
        """
        # open window
        arcade.open_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Main")
        arcade.schedule(self.on_update, 1 / 60)
        arcade.set_background_color(arcade.color.BLACK)

        # setting up rooms
        self.tile_map = TiledMap()
        self.rooms = []
        room = self.tile_map.tutorial_world()
        self.rooms.append(room)

        room = self.tile_map.stage_one()
        self.rooms.append(room)

        room = self.tile_map.stage_two()
        self.rooms.append(room)

        room = self.tile_map.stage_three()
        self.rooms.append(room)

        room = self.tile_map.boss_world()
        self.rooms.append(room)
        self.room_tutorial()
        # add start screen
        self.transition = arcade.load_texture("images/start_screen.png")
        # add sounds
        self.sound = Sounds()
        # self.sound.update(1)
        # override arcade methods
        self.level_finish_time = 0
        self.game_over = False
        window = arcade.get_window()
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_draw = self.on_draw
        arcade.finish_render()
        arcade.run()


Main()
