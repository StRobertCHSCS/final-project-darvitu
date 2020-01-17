import arcade
import pytiled_parser
from arcade.tilemap import get_tilemap_layer, _process_tile_layer, _process_object_layer


class TiledMap(arcade.TiledMap):
    def __init__(self):
        super().__init__()

        self.ground_list = None
        self.wall_list = None
        self.traps_list = None

    def tutorial_world(self):
        room = TiledMap()
        map = arcade.tilemap.read_tmx("Maps/tutorial-world.tmx")

        room.ground_list = self.process_layer(map, "ground", 1, "images")
        room.wall_list = self.process_layer(map, "walls", 1, "images")
        room.traps_list = self.process_layer(map, "traps", 1, "images")
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

    def process_layer(self,map_object: pytiled_parser.objects.TileMap,
                      layer_name: str,
                      scaling: float = 1,
                      base_directory: str = "") -> arcade.SpriteList:
        """
        This takes a map layer returned by the read_tmx function, and creates Sprites for it.

        :param map_object: The TileMap read in by read_tmx.
        :param layer_name: The name of the layer that we are creating sprites for.
        :param scaling: Scaling the layer up or down.
                        (Note, any number besides 1 can create a tearing effect,
                        if numbers don't evenly divide.)
        :param base_directory: Base directory of the file, that we start from to
                               load images.
        :returns: A SpriteList.

        """

        if len(base_directory) > 0 and not base_directory.endswith("/"):
            base_directory += "/"

        layer = get_tilemap_layer(map_object, layer_name)
        if layer is None:
            print(f"Warning, no layer named '{layer_name}'.")
            return arcade.SpriteList()

        if isinstance(layer, pytiled_parser.objects.TileLayer):
            return _process_tile_layer(map_object, layer, scaling, base_directory)

        elif isinstance(layer, pytiled_parser.objects.ObjectLayer):
            return _process_object_layer(map_object, layer, scaling, base_directory)
