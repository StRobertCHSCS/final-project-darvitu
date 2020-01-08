import arcade
import random
from player import Player
from tiledmap import TiledMap
from enemy import Enemy


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
            self.enemies.append(Enemy(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, random.randint(125, 200)))
        for enemy in self.enemies:
            self.character_list.append(enemy)

def main():
    global player, character_list, physics_engine, tile_map
    # open window
    arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Main")
    arcade.schedule(on_update, 1 / 100)
    arcade.set_background_color(arcade.color.BLACK)

    # create character list
    character_list = arcade.SpriteList()

    # setting up player
    player = Player(WINDOW_WIDTH, WINDOW_HEIGHT)

    # add player to the list of characters
    character_list.append(player)
    
    # Override arcade methods
    physics_engine = None
    tile_map = TiledMap()
    window = arcade.get_window()
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_draw = on_draw
    arcade.run()


Main()
