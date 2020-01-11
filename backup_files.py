import arcade
import random
from player import Player
from tiledmap import TiledMap
from blob import Blob


class Main():

    def __init__(self):

        self.direction = None
        self.player = None
        self.enemies = []
        self.character_list = None
        self.physics_engine = None
        self.tile_map = None
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.main()

    def on_draw(self) -> None:
        """
        Holds all rendering code to screen
        :return: none, draws to the window
        """
        arcade.start_render()
        self.tile_map.ground_list.draw()
        self.tile_map.wall_list.draw()
        self.character_list.draw()

    def move_player(self, delta_time) -> None:
        """
        Moves the player
        :param delta_time: execution time
        :return:
        """
        output = self.player.move_player(delta_time, self.direction)
        if output is not None:
            self.on_key_release(output, None)

    def move_enemy(self, delta_time) -> None:
        """
        Moves enemies based on the position of the player
        :param delta_time:
        :return:
        """
        for enemy in self.enemies:
            enemy.follow(self.player, delta_time)

    def on_update(self, delta_time) -> None:
        """
        Update function called periodically
        :param delta_time: time of execution
        :return: none
        """
        # updates the animation state of the player sprite
        self.character_list.update_animation()
        # move player
        self.move_player(delta_time)
        # move enemies
        self.move_enemy(delta_time)

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
        else:
            print("invalid key press")

    def on_key_release(self, symbol, modifiers) -> None:
        """
        Handling when user releases keys (stops moving)
        :param symbol: key released
        :param modifiers: unused
        :return: none
        """
        # sets key direction back to None after key release, starts standing animation
        if symbol == arcade.key.RIGHT and self.direction == "RIGHT":
            self.player.face_direction(self.direction)
            self.direction = None
        elif symbol == arcade.key.LEFT and self.direction == "LEFT":
            self.player.face_direction(self.direction)
            self.direction = None
        elif symbol == arcade.key.UP and self.direction == "UP":
            self.player.face_direction(self.direction)
            self.direction = None
        elif symbol == arcade.key.DOWN and self.direction == "DOWN":
            self.player.face_direction(self.direction)
            self.direction = None
        else:
            print("invalid key release")

    def create_enemies(self) -> None:
        """
        temporary testing function that creates enemies
        :return:
        """
        for x in range(10):
            self.enemies.append(Blob(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, random.randint(75, 150)))
        for enemy in self.enemies:
            self.character_list.append(enemy)

    def main(self):
        # open window
        arcade.open_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Main")
        arcade.schedule(self.on_update, 1 / 60)
        arcade.set_background_color(arcade.color.BLACK)
        # create character list
        self.character_list = arcade.SpriteList()
        # setting up player
        self.player = Player(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.create_enemies()
        # add player to the list of characters
        self.character_list.append(self.player)
        # Override arcade methods
        self.physics_engine = None
        self.tile_map = TiledMap()
        window = arcade.get_window()
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_draw = self.on_draw
        arcade.run()


Main()

"""------------------------------------------------------------------------"""
import arcade


class Player(arcade.AnimatedTimeSprite):
    def __init__(self, window_width: int, window_height: int, player_speed=250, direction="DOWN"):
        super().__init__()

        """Constructor of the Player class, that is the entity that the user will be moving controlling.

        :param direction: default direction of player
        :param player_speed: speed of player
        :param window_width: width of game window
        :param window_heigth: height of game window
        """
        # setting speed and direction based on creation of Player object
        self.player_speed = player_speed
        self.direction = direction

        # change animation rate
        self.texture_change_frames = 30

        # spawn facing forward
        self.face_direction(direction)

        # setting position of Player
        self.center_x = window_width // 2
        self.center_y = window_height // 2

        # defining size of player for later use
        self.width = None
        self.height = None
        # setting up window size
        self.WINDOW_HEIGHT = window_height
        self.WINDOW_WIDTH = window_width

    # animation for the player to face when it is not moving
    def face_direction(self, direction) -> None:
        """
        Faces the character animation based on the direction.
        :param direction: direction for the character to face
        :return: None
        """
        if direction == "LEFT":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=104, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=312, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(1):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=208, width=96, height=104,
                                        scale=0.5))
        elif direction == "DOWN":
            self.textures = []
            for i in range(3):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=0, width=96, height=104, scale=0.5))

        else:
            print("Invalid direction to face")

    # animation for moving
    def move_direction(self, direction) -> None:
        """
        Sets animation to the direction of the player movement
        :param direction: direction of player movement
        :return: None
        """
        if direction == "DOWN":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=416, width=96, height=104,
                                        scale=0.5))
        elif direction == "LEFT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=520, width=96, height=104,
                                        scale=0.5))
        elif direction == "UP":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=624, width=96, height=104,
                                        scale=0.5))
        elif direction == "RIGHT":
            self.textures = []
            for i in range(10):
                self.textures.append(
                    arcade.load_texture("images/player.png", x=i * 96, y=728, width=96, height=104,
                                        scale=0.5))
        else:
            print("Direction not valid to move")

    def move_player(self, delta_time, direction):
        self.direction = direction
        if self.direction is not None:
            self.texture_change_frames = 2.5
            if self.direction == "RIGHT":
                self.center_x += self.player_speed * delta_time
                if self.center_x > self.WINDOW_WIDTH - 25:
                    self.center_x = self.WINDOW_WIDTH - 25
                    self.direction = None
                    return arcade.key.RIGHT
            if self.direction == "LEFT":
                self.center_x -= self.player_speed * delta_time
                if self.center_x < 25:
                    self.center_x = 25
                    self.direction = None
                    return arcade.key.LEFT
            if self.direction == "UP":
                self.center_y += self.player_speed * delta_time
                if self.center_y > self.WINDOW_HEIGHT - 25:
                    self.center_y = self.WINDOW_HEIGHT - 25
                    self.direction = None
                    return arcade.key.UP
            if self.direction == "DOWN":
                self.center_y -= self.player_speed * delta_time
                if self.center_y < 25:
                    self.center_y = 25
                    self.direction = None
                    return arcade.key.DOWN
        else:
            self.texture_change_frames = 30
"""-----------------------------------------------------------------------------------------"""