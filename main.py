import arcade
import random
from player import Player
from tiledmap import TiledMap
from enemy import Enemy

direction = None
player = None
enemies = []
character_list = None
physics_engine = None
tile_map = None
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800


def on_draw() -> None:
    """
    Holds all rendering code to screen
    :return: none, draws to the window
    """
    global character_list, tile_map
    arcade.start_render()
    tile_map.ground_list.draw()
    tile_map.wall_list.draw()
    character_list.draw()


def move_player(delta_time) -> None:
    """
    Moves the player
    :param delta_time: execution time
    :return:
    """
    global direction, player
    output = player.move_player(delta_time, direction)
    if output is not None:
        on_key_release(output, None)


def move_enemy(delta_time) -> None:
    """
    Moves enemies based on the position of the player
    :param delta_time:
    :return:
    """
    global enemies, player
    for enemy in enemies:
        enemy.texture_change_frames = 2.5
        wait = random.randint(25, 100)
        enemy.follow(player, wait)
        if enemy.direction is not None:
            if enemy.direction == "RIGHT":
                enemy.center_x += enemy.player_speed * delta_time
            if enemy.direction == "LEFT":
                enemy.center_x -= enemy.player_speed * delta_time
            if enemy.direction == "UP":
                enemy.center_y += enemy.player_speed * delta_time
            if enemy.direction == "DOWN":
                enemy.center_y -= enemy.player_speed * delta_time


def on_update(delta_time) -> None:
    """
    Update function called periodically
    :param delta_time: time of execution
    :return: none
    """
    # updates the animation state of the player sprite
    character_list.update_animation()
    # move player
    move_player(delta_time)
    # move enemies
    move_enemy(delta_time)


def on_key_press(symbol, modifiers) -> None:
    '''
    Moving the player based on the key pressed
    :param symbol: keypressed
    :param modifiers: Unused parameter
    :return: none
    '''
    global direction, player
    # increase frame rate to show animation
    player.texture_change_frames = 2.5

    # player movement
    if symbol == arcade.key.RIGHT:
        direction = "RIGHT"
        player.move_direction(direction)
    elif symbol == arcade.key.LEFT:
        direction = "LEFT"
        player.move_direction(direction)
    elif symbol == arcade.key.UP:
        direction = "UP"
        player.move_direction(direction)
    elif symbol == arcade.key.DOWN:
        direction = "DOWN"
        player.move_direction(direction)
    else:
        print("invalid key press")


def on_key_release(symbol, modifiers) -> None:
    """
    Handling when user releases keys (stops moving)
    :param symbol: key released
    :param modifiers: unused
    :return: none
    """
    global player, direction
    # sets animation to lower refresh rate
    player.texture_change_frames = 30

    # sets key direction back to None after key release, starts standing animation
    if symbol == arcade.key.RIGHT and direction == "RIGHT":
        player.face_direction(direction)
        direction = None
    elif symbol == arcade.key.LEFT and direction == "LEFT":
        player.face_direction(direction)
        direction = None
    elif symbol == arcade.key.UP and direction == "UP":
        player.face_direction(direction)
        direction = None
    elif symbol == arcade.key.DOWN and direction == "DOWN":
        player.face_direction(direction)
        direction = None
    else:
        print("invalid key release")


def create_enemies():
    """
    temporary testing function
    :return:
    """
    global enemies, character_list
    for x in range(10):
        enemies.append(Enemy(WINDOW_WIDTH, WINDOW_HEIGHT, random.randint(150, 235)))
    for enemy in enemies:
        character_list.append(enemy)

def main():
    global player, character_list, physics_engine, tile_map, enemies
    # open window
    arcade.open_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Main")
    arcade.schedule(on_update, 1 / 60)
    arcade.set_background_color(arcade.color.BLACK)
    # create character list
    character_list = arcade.SpriteList()
    # setting up player
    player = Player(WINDOW_WIDTH, WINDOW_HEIGHT)
    create_enemies()
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


main()
