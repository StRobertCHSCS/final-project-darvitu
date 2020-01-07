import arcade
from player import Player

direction = None
player = None
character_list = None
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500


def on_draw() -> None:
    """
    Holds all rendering code to screen
    :return: none, draws to the window
    """
    global character_list
    arcade.start_render()
    character_list.draw()


def on_update(delta_time) -> None:
    """
    Update function called periodically
    :param delta_time: time of execution
    :return: none
    """
    global direction, player, character_list
    # updates the animation state of the player sprite
    character_list.update_animation()
    # changing location of player
    if direction is not None:
        if direction == "RIGHT":
            player.center_x += player.player_speed * delta_time
            if player.center_x > WINDOW_WIDTH - 25:
                player.center_x = WINDOW_WIDTH - 25
                on_key_release(arcade.key.RIGHT, None)
                direction = None
        if direction == "LEFT":
            player.center_x -= player.player_speed * delta_time
            if player.center_x < 25:
                player.center_x = 25
                on_key_release(arcade.key.LEFT, None)
                direction = None
        if direction == "UP":
            player.center_y += player.player_speed * delta_time
            if player.center_y > WINDOW_HEIGHT - 25:
                player.center_y = WINDOW_HEIGHT - 25
                on_key_release(arcade.key.UP, None)
                direction = None
        if direction == "DOWN":
            player.center_y -= player.player_speed * delta_time
            if player.center_y < 25:
                player.center_y = 25
                on_key_release(arcade.key.DOWN, None)
                direction = None


def on_key_press(symbol, modifiers) -> None:
    '''
    Moving the player based on the key pressed
    :param symbol: keypressed
    :param modifiers: Unused parameter
    :return: none
    '''
    global direction, player
    # increase frame rate to show animation
    player.texture_change_frames = 5

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
    if symbol == arcade.key.RIGHT:
        player.face_direction(direction)
        direction = None
    elif symbol == arcade.key.LEFT:
        player.face_direction(direction)
        direction = None
    elif symbol == arcade.key.UP:
        player.face_direction(direction)
        direction = None
    elif symbol == arcade.key.DOWN:
        player.face_direction(direction)
        direction = None
    else:
        print("invalid key release")


def main():
    global player, character_list
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
    window = arcade.get_window()
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release
    window.on_draw = on_draw
    arcade.run()


main()
