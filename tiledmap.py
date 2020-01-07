import arcade

class TiledMap(arcade.TiledMap):
    def __init__(self):
        super().__init__()

        map = arcade.tilemap.read_tmx("Maps/test-map-6.tmx")
        self.ground_list = arcade.tilemap.process_layer(map, "Tile Layer 1", 1, "images")
        self.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")


