import arcade


class TiledMap(arcade.TiledMap):
    def __init__(self):
        super().__init__()

        self.ground_list = None
        self.wall_list = None
        self.traps_list = None

    def tutorial_world(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/tutorial-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def stage_one(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stage1-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def stage_two(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stage2-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def stage_three(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stage3-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room

    def boss_world(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/stageBoss-world.tmx")

        room.ground_list = arcade.tilemap.process_layer(map, "ground", 1, "images")
        room.wall_list = arcade.tilemap.process_layer(map, "walls", 1, "images")
        room.traps_list = arcade.tilemap.process_layer(map, "traps", 1, "images")

        return room
