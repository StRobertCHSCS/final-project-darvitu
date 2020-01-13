import arcade


class TiledMap(arcade.TiledMap):
    def __init__(self):
        super().__init__()


    def tutorial_world(self):
        map = arcade.tilemap.read_tmx("Maps/tutorial-world.tmx")
        self.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        self.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        self.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")
    
    def stage_one(self):
        map = arcade.tilemap.read_tmx("Maps/stage1-world.tmx")
        self.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        self.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        self.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")
    
    


