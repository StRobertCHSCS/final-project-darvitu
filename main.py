import arcade
from game_window import GameWindow

direction = None


def on_update(delta_time):
    global direction
    if direction != None:
        print(direction)


def on_key_press(symbol, modifiers):
    global direction
    if symbol == arcade.key.RIGHT:
        direction = "RIGHT"
    if symbol == arcade.key.LEFT:
        direction = "LEFT"
    if symbol == arcade.key.UP:
        direction = "UP"
    if symbol == arcade.key.DOWN:
        direction = "DOWN"


def main():
    arcade.open_window(1280, 720, "Main")
    arcade.start_render()
    arcade.schedule(on_update, 1 / 60)
    arcade.set_background_color(arcade.color.BLACK)
    # Override arcade methods
    window = arcade.get_window()
    window.on_key_press = on_key_press
    arcade.finish_render()
    arcade.run()


main()
