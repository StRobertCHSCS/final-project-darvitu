import arcade
import time
import random
from player import Player
from tiledmap import TiledMap
from blob import Blob
from collision import CollisionDetection
from sounds import Sounds
from goblin import Goblin
from spritelist import Sprites
from wizard import WizardTower


class Main():

    def __init__(self):

        self.direction = None
        self.player = None
        self.enemies = None
        self.player_engine = None
        self.enemies_engine = None
        self.towers = None
        self.tile_map = None
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800
        self.time = 0
        self.sound = None
        self.main()

    def on_draw(self) -> None:
        """
        Holds all rendering code to screen
        :return: none, draws to the window
        """
        arcade.start_render()
        self.tile_map.ground_list.draw()
        self.tile_map.wall_list.draw()
        self.tile_map.traps_list.draw()
        self.player.draw()
        self.enemies.draw()
        self.towers.draw()
        self.towers.fireball.draw()

    def move_player(self) -> None:
        """
        Moves the player
        :param delta_time: execution time
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
        for enemy in self.enemies_engine:
            enemy.update(enemy, self.player)
        for tower in self.towers:
            tower.point_towards(self.player)
            tower.shoot(self.player)

    def on_update(self, delta_time) -> None:
        """
        Update function called periodically
        :param delta_time: time of execution
        :return: none
        """
        # updates the animation state of the player sprite
        self.enemies.update_animation(self.player)
        self.player.update_animation()
        # move player
        self.move_player()
        # move enemies
        self.move_enemy()
        # check player and enemy collision
        self.player_engine.update(player_to_follow=self.enemies)
        self.time += 1 / 60

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

    def create_enemies(self) -> None:
        """
        temporary testing function that creates enemies
        :return:
        """
        for x in range(0):
            self.enemies.append(Blob(self.WINDOW_WIDTH + 400, self.WINDOW_HEIGHT + 300))
            self.enemies.append(Goblin(self.WINDOW_WIDTH + 400, self.WINDOW_HEIGHT + 300, 3))
        for enemy in self.enemies:
            self.enemies_engine.append(CollisionDetection(enemy, self.tile_map.wall_list))
        self.towers.append(WizardTower(200, 200, 48, 52))

    def main(self):
        # open window
        arcade.open_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Main")
        arcade.schedule(self.on_update, 1 / 60)
        arcade.set_background_color(arcade.color.BLACK)
        # create character list
        self.enemies_engine = []
        self.enemies = Sprites()
        # setting up player
        self.player = Player(100, 100)

        # add player to the list of characters
        self.tile_map = TiledMap()
        self.tile_map.tutorial_world()
        # create player engine
        self.player_engine = CollisionDetection(self.player, self.tile_map.wall_list)
        self.towers = Sprites()
        self.create_enemies()

        # add sounds
        self.sound = Sounds()
        # self.sound.update(0)
        # override arcade methods
        window = arcade.get_window()
        window.on_key_press = self.on_key_press
        window.on_key_release = self.on_key_release
        window.on_draw = self.on_draw
        arcade.run()


Main()
