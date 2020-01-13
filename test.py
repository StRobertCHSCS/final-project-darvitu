import arcade


class Fireball(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(center_x=x, center_y=y)

        self.texture = arcade.load_texture("images/fireball.png")


arcade.open_window(500, 500, "TEST")
arcade.start_render()
fireball = Fireball(200, 200)
fireball.draw()
arcade.finish_render()
arcade.run()
