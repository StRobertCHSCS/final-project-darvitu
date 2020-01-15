import arcade

arcade.open_window(500, 500, "TEST")

health = 100


def draw_health_bar(health: int) -> None:
    """
    Draws healthbar to screen
    :param health: health of player
    :return: none
    """

    num_of_bars = health // 1
    # draw background of healthbar
    arcade.draw_texture_rectangle(410, 485, 100, 10, arcade.load_texture("images/health_bar_2.png"))
    for x in range(num_of_bars):
        if num_of_bars <= 20:
            arcade.draw_texture_rectangle(361 + x, 485, 1, 10, arcade.load_texture("images/health_bar_red.png"))
        elif num_of_bars <= 60:
            arcade.draw_texture_rectangle(361 + x, 485, 1, 10,
                                          arcade.load_texture("images/health_bar_orange.png"))
        else:
            arcade.draw_texture_rectangle(361 + x, 485, 1, 10, arcade.load_texture("images/health_bar_green.png"))



def on_update(delta_time):
    global health
    draw_health_bar(health)
    health -= 1

arcade.finish_render()
arcade.schedule(on_update, 1 / 10)
arcade.run()
