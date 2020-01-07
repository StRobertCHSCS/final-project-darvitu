import arcade
class myGameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)


        self.ground_list = None

        self.setup()
        
    def setup(self):
        map = arcade.tilemap.read_tmx("Maps/test-map-6.tmx")
        self.ground_list = arcade.tilemap.process_layer(map, "Tile Layer 1", 1, "images")

    def on_draw(self):
        arcade.start_render()
        self.ground_list.draw()

    def on_update(self, delta_time):
        pass
        


myGameWindow(800,800,"Sprite Test")
arcade.run()