import arcade

arcade.open_window(500, 500, "TEST")

health = 100


def draw_health_bar(health: int) -> None:
    """
    Draws healthbar to screen
    :param health: health of player
    :return: none
    """

    # draw background of health bar
    arcade.start_render()
    arcade.draw_texture_rectangle(410, 485, 100, 10, arcade.load_texture("images/health_bar_2.png"))
    if health >= 80:
        arcade.draw_texture_rectangle(360 + (health/2), 485, health, 10, arcade.load_texture("images/health_bar_green.png"))
    elif health >= 40:
        arcade.draw_texture_rectangle(360 + (health/2), 485, health, 10, arcade.load_texture("images/health_bar_orange.png"))
    else:
        arcade.draw_texture_rectangle(360 + (health/2), 485, health, 10, arcade.load_texture("images/health_bar_red.png"))



def on_update(delta_time):
    global health
    draw_health_bar(health)
    health -= 1


arcade.finish_render()
arcade.schedule(on_update, 1 / 10)
arcade.run()
