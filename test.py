import arcade


class myGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)


        # creates wall and ground sprite list
        self.ground_list = None
        self.wall_list = None
        self.physics_engine = None

        self.setup()


    def setup(self):

        # loads tiled map
        my_map = arcade.tilemap.read_tmx("Maps/test-map-4.tmx")
        self.ground_list = arcade.tilemap.process_layer(my_map, "ground", 1, "images")

        # loads walls in tiled map
        self.wall_list = arcade.tilemap.process_layer(my_map, "walls", 1, "images")

        # inits physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

    def on_draw(self):
        arcade.start_render()
        # self.ground_list.draw()
        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        # updates the animation state of the player sprite
        self.physics_engine.update()
        self.player_list.update_animation()
        # checks the bools to see which key is being pressed and direction of movement
        if self.right:
            self.player.center_x += self.player_speed * delta_time
        if self.left:
            self.player.center_x -= self.player_speed * delta_time
        if self.up:
            self.player.center_y += self.player_speed * delta_time
        if self.down:
            self.player.center_y -= self.player_speed * delta_time

    def on_key_press(self, symbol, modifiers):
        # sets animation refresh to faster rate for more noticeable movement
        self.player.texture_change_frames = 5

        # checks for arrow key press, runs animation of walking
        if symbol == arcade.key.RIGHT:
            self.right = True
            self.move_right()
        if symbol == arcade.key.LEFT:
            self.left = True
            self.move_left()
        if symbol == arcade.key.UP:
            self.up = True
            self.move_up()
        if symbol == arcade.key.DOWN:
            self.down = True
            self.move_down()

    def on_key_release(self, symbol, modifiers):
        # sets animation to lower refresh rate
        self.player.texture_change_frames = 30

        # sets key bools back to false after key release, starts standing animation
        if symbol == arcade.key.RIGHT:
            self.right = False
            self.face_right()
        if symbol == arcade.key.LEFT:
            self.left = False
            self.face_left()
        if symbol == arcade.key.UP:
            self.up = False
            self.face_up()
        if symbol == arcade.key.DOWN:
            self.down = False
            self.face_forward()


myGameWindow(800, 800, "Sprite Test")
arcade.run()
