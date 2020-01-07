import arcade

class TiledMap(arcade.TiledMap):
    def __init__(self):
        super().__init__()

        map = arcade.tilemap.read_tmx("Maps/test-map-5.tmx")
        self.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")


