import math

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
        if self.is_game_active:
            self.rooms[self.world].ground_list.draw()
            self.rooms[self.world].wall_list.draw()
            self.rooms[self.world].traps_list.draw()

            self.player.draw()
            self.enemies.draw()
            self.towers.draw()
            # draw health bar
            self.draw_health_bar(self.player.health)

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
        for enemy in self.enemies_engine:
            if math.sqrt(
                    math.pow(self.player.center_x - enemy.player.center_x, 2) + math.pow(
                        self.player.center_y - enemy.player.center_y,
                        2)) < 500:
                enemy.update(enemy, self.player)
        for tower in self.towers:
            if tower.can_shoot and self.time % 50 == 0:
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
                if self.time - self.level_finish_time >= 50:
                    self.is_game_active = False
                    self.level_finish_time = 0
                    self.enemy_count = 0
                    self.world += 1
                    print(self.world)
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
        elif symbol == arcade.key.DELETE:
            arcade.get_window().close()

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
        arcade.set_background_color(arcade.color.WHITE)

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
        # self.sound.update(0)
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
