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
from wizard import WizardTower, Fireball


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
        self.world = 1
        self.sound = None
        self.setup()

    def on_draw(self) -> None:
        """
        Holds all rendering code to screen
        :return: none, draws to the window
        """
        arcade.start_render()

        self.rooms[self.world].ground_list.draw()
        self.rooms[self.world].wall_list.draw()
        self.rooms[self.world].traps_list.draw()

        self.player.draw()
        self.enemies.draw()
        self.towers.draw()

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
            if tower.can_shoot:
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
        elif symbol == arcade.key.SPACE:
            self.player.attack()

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
            self.direction = None
        elif symbol == arcade.key.LEFT and self.direction == "LEFT":
            self.player.move_direction(self.direction)
            self.direction = None
        elif symbol == arcade.key.UP and self.direction == "UP":
            self.player.move_direction(self.direction)
            self.direction = None
        elif symbol == arcade.key.DOWN and self.direction == "DOWN":
            self.player.move_direction(self.direction)
            self.direction = None
        elif symbol == arcade.key.SPACE:
            if self.direction is None:
                self.player.move_direction("RIGHT")
            else:
                self.player.move_direction(self.direction)

    def create_enemies(self) -> None:
        """
        temporary testing function that creates enemies
        :return:
        """
        for x in range(0):
            self.enemies.append(Blob(400, 400))
            self.enemies.append(Goblin(400, 400, 3))
        for enemy in self.enemies:
            self.enemies_engine.append(CollisionDetection(enemy, self.rooms[self.world].wall_list))
        for x in range(0):
            self.towers.append(WizardTower(400, 50 + 75 * x, 48, 52))
        for tower in self.towers:
            self.towers_engine.append(CollisionDetection(tower.fireball, self.rooms[self.world].wall_list))
            self.enemies.append(tower.fireball)

    def setup(self):
        """
        Called once at the start
        :return: none
        """
        # open window
        arcade.open_window(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, "Main")
        arcade.schedule(self.on_update, 1 / 60)
        arcade.set_background_color(arcade.color.BLACK)
        # create character list
        self.enemies_engine = []
        self.towers_engine = []
        self.rooms = []
        self.enemies = Sprites()

        # setting up player
        self.player = Player(400, 75)

        # setting up rooms
        self.tile_map = TiledMap()

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

        # create engines
        self.player_engine = CollisionDetection(self.player, self.rooms[self.world].wall_list)
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
